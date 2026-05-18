"""
Клиент для работы с Ollama API
"""
import ollama
import json
import logging
from typing import Dict, Optional
from config import config

logger = logging.getLogger(__name__)


class OllamaClient:
    """Клиент для общения с Ollama"""
    
    def __init__(
        self, 
        base_url: str = None, 
        model: str = None,
        timeout: int = None
    ):
        self.base_url = base_url or config.ollama_url
        self.model = model or config.ollama_model
        self.timeout = timeout or config.ollama_timeout
        
        # Создаем клиент
        try:
            self.client = ollama.Client(host=self.base_url)
            logger.info(f"✓ Ollama клиент создан (модель: {self.model})")
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к Ollama: {e}")
            raise
    
    def check_connection(self) -> bool:
        """Проверить подключение к Ollama"""
        try:
            models = self.client.list()
            logger.info(f"✓ Ollama доступен. Модели: {[m['name'] for m in models['models']]}")
            
            # Проверить что нужная модель установлена
            model_names = [m['name'] for m in models['models']]
            if not any(self.model in name for name in model_names):
                logger.warning(
                    f"⚠️ Модель {self.model} не найдена. "
                    f"Установите: ollama pull {self.model}"
                )
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Ollama недоступен: {e}")
            return False
    
    def chat(
        self, 
        messages: list,
        json_mode: bool = True,
        temperature: float = 0.1,
        stream: bool = False
    ) -> Optional[Dict]:
        """
        Отправить запрос в Ollama chat
        
        Args:
            messages: Список сообщений [{"role": "user", "content": "..."}]
            json_mode: Форсировать JSON ответ
            temperature: Температура генерации (0-2)
            stream: Стриминг ответа
        
        Returns:
            Ответ от модели или None при ошибке
        """
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                format="json" if json_mode else None,
                options={
                    "temperature": temperature,
                    "top_p": 0.9,
                    "num_ctx": 8192,  # Контекстное окно
                },
                stream=stream
            )
            
            if stream:
                return response  # Iterator для стриминга
            else:
                return response
                
        except Exception as e:
            logger.error(f"❌ Ошибка при запросе к Ollama: {e}")
            return None
    
    def generate_json(
        self, 
        system_prompt: str, 
        user_prompt: str,
        temperature: float = 0.1
    ) -> Optional[Dict]:
        """
        Генерация JSON ответа
        
        Args:
            system_prompt: Системный промпт
            user_prompt: Промпт пользователя
            temperature: Температура
        
        Returns:
            Распарсенный JSON или None
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.chat(
            messages=messages,
            json_mode=True,
            temperature=temperature
        )
        
        if not response:
            return None
        
        try:
            # Извлекаем content из ответа
            content = response['message']['content']
            
            # Парсим JSON
            result = json.loads(content)
            return result
            
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"❌ Ошибка парсинга JSON ответа: {e}")
            logger.debug(f"Raw response: {response}")
            return None
