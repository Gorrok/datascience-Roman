"""
Детектор вакансий - определяет является ли сообщение вакансией
"""
import re
from typing import List


class VacancyDetector:
    """Определяет является ли текст вакансией"""
    
    # Ключевые слова которые указывают на вакансию
    VACANCY_KEYWORDS = [
        # Русские
        r'\bвакансия\b',
        r'\bработа\b',
        r'\bтребуется\b',
        r'\bищем\b',
        r'\bнабор\b',
        r'\bнаём\b',
        r'\bзарплата\b',
        r'\bоклад\b',
        r'\bопыт работы\b',
        r'\bрезюме\b',
        r'\bоткрыта вакансия\b',
        r'\bсрочно требуется\b',
        
        # Английские
        r'\bjob\b',
        r'\bvacancy\b',
        r'\bhiring\b',
        r'\bopening\b',
        r'\bposition\b',
        r'\bwe are looking\b',
        r'\bremote\b',
        r'\bfull-time\b',
        r'\bpart-time\b',
        r'\bsalary\b',
        r'\bexperience\b',
        r'\bresume\b',
        r'\bcv\b',
    ]
    
    # Технические термины
    TECH_KEYWORDS = [
        r'\bpython\b',
        r'\bdjango\b',
        r'\bfastapi\b',
        r'\bflask\b',
        r'\bpostgresql\b',
        r'\bmongodb\b',
        r'\bredis\b',
        r'\bdocker\b',
        r'\bkubernetes\b',
        r'\baws\b',
        r'\bgcp\b',
        r'\breact\b',
        r'\bvue\b',
        r'\bjavascript\b',
        r'\btypescript\b',
        r'\bapi\b',
        r'\bbackend\b',
        r'\bfrontend\b',
        r'\bfullstack\b',
        r'\bdevops\b',
        r'\bмашинное обучение\b',
        r'\bmachine learning\b',
        r'\bml\b',
        r'\bai\b',
    ]
    
    # Должности
    POSITION_KEYWORDS = [
        r'\bразработчик\b',
        r'\bпrogrammer\b',
        r'\bdeveloper\b',
        r'\bengineer\b',
        r'\bинженер\b',
        r'\bаналитик\b',
        r'\banalyst\b',
        r'\bтимлид\b',
        r'\bteam lead\b',
        r'\bтехлид\b',
        r'\btech lead\b',
        r'\bсеньор\b',
        r'\bsenior\b',
        r'\bмидл\b',
        r'\bmiddle\b',
        r'\bджун\b',
        r'\bjunior\b',
    ]
    
    # Стоп-слова (если они есть, скорее всего НЕ вакансия)
    STOP_WORDS = [
        r'\bкурс\b',
        r'\bобучение\b',
        r'\bвебинар\b',
        r'\bконференция\b',
        r'\bподкаст\b',
        r'\bстатья\b',
        r'\bновость\b',
        r'\bреклама\b',
        r'\bскидка\b',
        r'\bпромокод\b',
    ]
    
    def __init__(self):
        # Компилируем регулярки один раз
        self.vacancy_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.VACANCY_KEYWORDS
        ]
        self.tech_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.TECH_KEYWORDS
        ]
        self.position_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.POSITION_KEYWORDS
        ]
        self.stop_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.STOP_WORDS
        ]
    
    def is_vacancy(self, text: str) -> bool:
        """
        Определяет является ли текст вакансией
        
        Логика:
        - Должно быть хотя бы одно vacancy keyword
        - Должно быть хотя бы одно tech/position keyword
        - Не должно быть stop words
        - Текст должен быть достаточно длинным (>100 символов)
        
        Args:
            text: Текст сообщения
        
        Returns:
            True если это вакансия
        """
        if not text or len(text) < 100:
            return False
        
        text_lower = text.lower()
        
        # Проверка стоп-слов
        for pattern in self.stop_patterns:
            if pattern.search(text_lower):
                return False
        
        # Проверка ключевых слов вакансии
        has_vacancy_keyword = any(
            pattern.search(text_lower) 
            for pattern in self.vacancy_patterns
        )
        
        # Проверка технических терминов или должностей
        has_tech_keyword = any(
            pattern.search(text_lower) 
            for pattern in self.tech_patterns
        )
        
        has_position_keyword = any(
            pattern.search(text_lower) 
            for pattern in self.position_patterns
        )
        
        # Вакансия = (vacancy_keyword) AND (tech_keyword OR position_keyword)
        is_vacancy = has_vacancy_keyword and (has_tech_keyword or has_position_keyword)
        
        return is_vacancy
    
    def extract_keywords(self, text: str) -> dict:
        """
        Извлекает ключевые слова из текста
        
        Returns:
            Словарь с найденными ключевыми словами
        """
        text_lower = text.lower()
        
        return {
            'vacancy_keywords': [
                pattern.pattern 
                for pattern in self.vacancy_patterns 
                if pattern.search(text_lower)
            ],
            'tech_keywords': [
                pattern.pattern 
                for pattern in self.tech_patterns 
                if pattern.search(text_lower)
            ],
            'position_keywords': [
                pattern.pattern 
                for pattern in self.position_patterns 
                if pattern.search(text_lower)
            ],
        }


# Глобальный экземпляр детектора
detector = VacancyDetector()
