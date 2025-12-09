import schedule
import time
from datetime import datetime
from threading import Thread

from todolist.core.repositories.task_repository import TaskRepository
from todolist.core.services.task_service import TaskService
from todolist.core.domain.status import TaskStatus

class SchedulerService:
    """Service to manage scheduled tasks"""
    
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo
        self._scheduler_thread = None
    
    def close_overdue_tasks(self):
        """Close tasks that are not done and have passed their deadline."""
        try:
            # Get all tasks
            all_tasks = self.task_repo.list_all_tasks()
            
            now = datetime.now().date()
            
            for task in all_tasks:
                # Check if task is not done AND has a deadline AND deadline has passed
                if (task.status != TaskStatus.DONE and 
                    task.deadline is not None and 
                    task.deadline < now):
                    
                    #update task fields
                    task.status = TaskStatus.DONE
                    task.closed_at = now
                    self.task_repo.update(task)
                    print(f"Closed overdue task: {task.name}")
        
        except Exception as e:
            print(f"Error in scheduler: {e}")
    
    def start(self):
        """Start the scheduler in a background thread."""
        # Schedule the job to run every hour
        schedule.every(30).seconds.do(self.close_overdue_tasks)
        
        # Run scheduler in background thread
        self._scheduler_thread = Thread(target=self._run_scheduler, daemon=True)
        self._scheduler_thread.start()
        print("Scheduler started")
    
    def _run_scheduler(self):
        """Run the scheduler loop."""
        while True:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
    
    def stop(self):
        """Stop the scheduler."""
        if self._scheduler_thread:
            print("Scheduler stopped")