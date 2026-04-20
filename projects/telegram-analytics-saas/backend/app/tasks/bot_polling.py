"""
Celery задачи для управления ботами
"""
from app.tasks.celery_app import celery_app
from loguru import logger
import subprocess
import signal
import os

# Словарь для хранения PID процессов ботов
bot_processes = {}


@celery_app.task(name="start_bot_task")
def start_bot_task(bot_id: int):
    """Запускает бота в отдельном процессе"""
    logger.info(f"Запуск бота {bot_id}")
    
    try:
        # Запускаем bot_worker в отдельном процессе
        process = subprocess.Popen(
            ["python", "bot_worker/bot_worker.py", str(bot_id)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        
        bot_processes[bot_id] = process.pid
        logger.info(f"Бот {bot_id} запущен с PID {process.pid}")
        
        return {"bot_id": bot_id, "status": "started", "pid": process.pid}
    
    except Exception as e:
        logger.error(f"Ошибка запуска бота {bot_id}: {e}")
        return {"bot_id": bot_id, "status": "error", "error": str(e)}


@celery_app.task(name="stop_bot_task")
def stop_bot_task(bot_id: int):
    """Останавливает бота"""
    logger.info(f"Остановка бота {bot_id}")
    
    try:
        pid = bot_processes.get(bot_id)
        
        if pid:
            try:
                os.killpg(os.getpgid(pid), signal.SIGTERM)
                logger.info(f"Бот {bot_id} остановлен (PID {pid})")
                del bot_processes[bot_id]
            except ProcessLookupError:
                logger.warning(f"Процесс {pid} для бота {bot_id} не найден")
                del bot_processes[bot_id]
        else:
            logger.warning(f"PID для бота {bot_id} не найден в памяти")
        
        return {"bot_id": bot_id, "status": "stopped"}
    
    except Exception as e:
        logger.error(f"Ошибка остановки бота {bot_id}: {e}")
        return {"bot_id": bot_id, "status": "error", "error": str(e)}
