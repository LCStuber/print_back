from typing import Optional
from src.shared.domain.entities.notification import Notification
from src.shared.domain.repositories.notification_repository_interface import INotificationRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class UpdateNotificationUsecase:

    def __init__(self, repo: INotificationRepository):
        self.repo = repo
    
    def __call__(self, notification_id: str, title: Optional[str] = None, description: Optional[str] = None, creation_date: Optional[str] = None, has_seen: Optional[list] = None):
        
        if not self.repo.get_notification(notification_id):
            raise NoItemsFound("Notification")
        
        return self.repo.update_notification(notification_id, title, description, creation_date, has_seen)