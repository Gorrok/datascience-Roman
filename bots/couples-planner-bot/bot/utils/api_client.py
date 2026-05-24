import aiohttp
from typing import Optional, List, Dict
from loguru import logger

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def init_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close_session(self):
        if self.session:
            await self.session.close()
    
    async def get_plans(self, user_id: int, include_completed: bool = False) -> List[Dict]:
        """Получить планы пользователя"""
        try:
            async with self.session.get(
                f"{self.base_url}/api/plans/",
                params={"user_id": user_id, "include_completed": include_completed}
            ) as response:
                if response.status == 200:
                    return await response.json()
                logger.error(f"Failed to get plans: {response.status}")
                return []
        except Exception as e:
            logger.error(f"Error getting plans: {e}")
            return []
    
    async def get_invites(self, user_id: int, status: Optional[str] = None) -> List[Dict]:
        """Получить инвайты пользователя"""
        try:
            params = {"user_id": user_id}
            if status:
                params["status"] = status
            
            async with self.session.get(
                f"{self.base_url}/api/plans/invites/{user_id}",
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                logger.error(f"Failed to get invites: {response.status}")
                return []
        except Exception as e:
            logger.error(f"Error getting invites: {e}")
            return []
    
    async def respond_to_invite(self, invite_id: int, status: str) -> bool:
        """Ответить на инвайт"""
        try:
            async with self.session.patch(
                f"{self.base_url}/api/plans/invites/{invite_id}/respond",
                params={"status": status}
            ) as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"Error responding to invite: {e}")
            return False
    
    async def complete_plan(self, plan_id: int) -> bool:
        """Отметить план как выполненный"""
        try:
            async with self.session.patch(
                f"{self.base_url}/api/plans/{plan_id}",
                json={"is_completed": True}
            ) as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"Error completing plan: {e}")
            return False
