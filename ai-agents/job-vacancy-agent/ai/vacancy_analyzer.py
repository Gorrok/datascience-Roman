"""
Анализатор вакансий с помощью Hermes AI через Ollama
"""
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

from ai.ollama_client import OllamaClient
from config import config
from database.models import Vacancy
from database import AsyncSessionLocal
from sqlalchemy import select

logger = logging.getLogger(__name__)


class VacancyAnalyzer:
    """Анализирует вакансии с помощью Ollama + Hermes AI"""
    
    SYSTEM_PROMPT = """Ты эксперт по анализу IT вакансий. Твоя задача - извлечь ключевую информацию из текста вакансии.

Извлекай следующие данные в формате JSON:
- job_title: название должности (строка)
- required_skills: список обязательных технических навыков (массив строк)
- nice_to_have_skills: список желательных навыков (массив строк)
- experience_years: требуемый опыт работы в годах (число или null)
- salary_min: минимальная зарплата (число или null)
- salary_max: максимальная зарплата (число или null)
- salary_currency: валюта зарплаты (RUB/USD/EUR или null)
- location: локация работы (строка)
- work_mode: формат работы (remote/office/hybrid или null)
- seniority_level: уровень (junior/middle/senior/lead или null)
- employment_type: тип занятости (full-time/part-time/contract или null)
- company: название компании (строка или null)
- description: краткое описание вакансии (1-2 предложения)

Отвечай ТОЛЬКО валидным JSON без дополнительных комментариев.
Если какая-то информация не указана явно, ставь null."""
    
    def __init__(self, ollama_client: OllamaClient = None):
        self.client = ollama_client or OllamaClient()
    
    def analyze_vacancy_text(self, vacancy_text: str) -> Optional[Dict]:
        """
        Анализирует текст вакансии и извлекает структурированные данные
        
        Args:
            vacancy_text: Текст вакансии
        
        Returns:
            Словарь с извлеченными данными или None при ошибке
        """
        user_prompt = f"""Проанализируй следующую вакансию и извлеки все данные:

{vacancy_text}

Верни результат в формате JSON."""
        
        logger.info("🤖 Анализирую вакансию через Ollama...")
        
        result = self.client.generate_json(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.1  # Низкая для консистентности
        )
        
        if result:
            logger.info(f"✓ Вакансия проанализирована: {result.get('job_title', 'Unknown')}")
        else:
            logger.error("❌ Не удалось проанализировать вакансию")
        
        return result
    
    def calculate_relevance_score(
        self, 
        vacancy_data: Dict
    ) -> Dict:
        """
        Вычисляет релевантность вакансии на основе профиля пользователя
        
        Args:
            vacancy_data: Данные вакансии от Ollama
        
        Returns:
            Словарь с оценкой релевантности и причинами
        """
        score = 0.0
        max_score = 0.0
        reasons = []
        
        # 1. Проверка навыков (вес: 40%)
        weight_skills = 0.4
        max_score += weight_skills
        
        required_skills = set(
            skill.lower() 
            for skill in vacancy_data.get('required_skills', [])
        )
        user_skills = set(skill.lower() for skill in config.user_skills)
        
        if required_skills:
            matching_skills = required_skills.intersection(user_skills)
            skills_match_ratio = len(matching_skills) / len(required_skills)
            score += skills_match_ratio * weight_skills
            
            if matching_skills:
                reasons.append(f"✓ Совпадение навыков: {', '.join(matching_skills)}")
            
            missing_skills = required_skills - user_skills
            if missing_skills:
                reasons.append(f"✗ Отсутствуют навыки: {', '.join(missing_skills)}")
        else:
            # Если требования не указаны, считаем что подходит
            score += weight_skills * 0.5
        
        # 2. Проверка опыта (вес: 20%)
        weight_experience = 0.2
        max_score += weight_experience
        
        required_exp = vacancy_data.get('experience_years')
        if required_exp is not None:
            if required_exp <= config.user_experience_years:
                score += weight_experience
                reasons.append(f"✓ Опыт подходит: требуется {required_exp}, есть {config.user_experience_years}")
            else:
                reasons.append(f"✗ Недостаточно опыта: требуется {required_exp}, есть {config.user_experience_years}")
        else:
            score += weight_experience * 0.5
        
        # 3. Проверка зарплаты (вес: 25%)
        weight_salary = 0.25
        max_score += weight_salary
        
        salary_max = vacancy_data.get('salary_max')
        if salary_max is not None and salary_max > 0:
            if salary_max >= config.user_min_salary:
                score += weight_salary
                reasons.append(f"✓ Зарплата подходит: до {salary_max}")
            else:
                reasons.append(f"✗ Зарплата ниже желаемой: {salary_max} < {config.user_min_salary}")
        else:
            # Зарплата не указана - нейтрально
            score += weight_salary * 0.3
            reasons.append("⚠️ Зарплата не указана")
        
        # 4. Проверка локации (вес: 15%)
        weight_location = 0.15
        max_score += weight_location
        
        location = vacancy_data.get('location', '').lower()
        work_mode = vacancy_data.get('work_mode', '').lower()
        
        if any(
            pref.lower() in location or pref.lower() in work_mode
            for pref in config.user_preferred_locations
        ):
            score += weight_location
            reasons.append(f"✓ Локация/режим подходит: {location or work_mode}")
        else:
            reasons.append(f"⚠️ Локация: {location or work_mode or 'не указана'}")
        
        # 5. Проверка исключающих слов
        exclude_found = []
        vacancy_text = json.dumps(vacancy_data, ensure_ascii=False).lower()
        
        for keyword in config.exclude_keywords:
            if keyword.lower() in vacancy_text:
                exclude_found.append(keyword)
        
        if exclude_found:
            score *= 0.5  # Сильно снижаем оценку
            reasons.append(f"⚠️ Найдены исключающие слова: {', '.join(exclude_found)}")
        
        # Нормализуем score к диапазону 0-1
        final_score = score / max_score if max_score > 0 else 0
        
        is_relevant = final_score >= config.min_relevance_score
        
        return {
            'relevance_score': round(final_score, 3),
            'is_relevant': is_relevant,
            'reasons': reasons,
            'threshold': config.min_relevance_score
        }
    
    async def analyze_and_update_vacancy(self, vacancy: Vacancy) -> bool:
        """
        Анализирует вакансию и обновляет её в БД
        
        Args:
            vacancy: Объект вакансии из БД
        
        Returns:
            True если успешно проанализирована и обновлена
        """
        try:
            # Анализ текста вакансии
            vacancy_data = self.analyze_vacancy_text(vacancy.raw_text)
            
            if not vacancy_data:
                logger.warning(f"Не удалось проанализировать вакансию ID {vacancy.id}")
                return False
            
            # Вычисление релевантности
            relevance_result = self.calculate_relevance_score(vacancy_data)
            
            # Обновляем вакансию
            async with AsyncSessionLocal() as session:
                # Перезагружаем объект в текущей сессии
                result = await session.execute(
                    select(Vacancy).where(Vacancy.id == vacancy.id)
                )
                db_vacancy = result.scalar_one()
                
                # Обновляем поля
                db_vacancy.title = vacancy_data.get('job_title')
                db_vacancy.description = vacancy_data.get('description')
                db_vacancy.requirements = json.dumps(
                    vacancy_data.get('required_skills', []), 
                    ensure_ascii=False
                )
                db_vacancy.salary = f"{vacancy_data.get('salary_min', '')}-{vacancy_data.get('salary_max', '')} {vacancy_data.get('salary_currency', '')}"
                db_vacancy.location = vacancy_data.get('location')
                db_vacancy.company = vacancy_data.get('company')
                db_vacancy.work_mode = vacancy_data.get('work_mode')
                
                db_vacancy.relevance_score = relevance_result['relevance_score']
                db_vacancy.is_relevant = relevance_result['is_relevant']
                db_vacancy.match_reason = '\n'.join(relevance_result['reasons'])
                
                await session.commit()
                
                logger.info(
                    f"✓ Вакансия ID {vacancy.id} обновлена: "
                    f"score={relevance_result['relevance_score']:.2f}, "
                    f"relevant={relevance_result['is_relevant']}"
                )
                
                return True
                
        except Exception as e:
            logger.error(f"❌ Ошибка при анализе вакансии ID {vacancy.id}: {e}")
            return False
    
    async def analyze_all_unanalyzed(self) -> Dict:
        """
        Анализирует все вакансии которые еще не были проанализированы
        
        Returns:
            Статистика анализа
        """
        logger.info("🚀 Начинаем анализ непроанализированных вакансий...")
        
        async with AsyncSessionLocal() as session:
            # Найти вакансии где relevance_score = 0 (еще не анализировались)
            result = await session.execute(
                select(Vacancy).where(Vacancy.relevance_score == 0.0)
            )
            vacancies = result.scalars().all()
        
        total = len(vacancies)
        analyzed = 0
        relevant = 0
        
        logger.info(f"📊 Найдено {total} вакансий для анализа")
        
        for i, vacancy in enumerate(vacancies, 1):
            logger.info(f"[{i}/{total}] Анализирую вакансию ID {vacancy.id}...")
            
            success = await self.analyze_and_update_vacancy(vacancy)
            
            if success:
                analyzed += 1
                if vacancy.is_relevant:
                    relevant += 1
        
        logger.info(
            f"✅ Анализ завершен: {analyzed}/{total} проанализировано, "
            f"{relevant} релевантных"
        )
        
        return {
            'total': total,
            'analyzed': analyzed,
            'relevant': relevant
        }
