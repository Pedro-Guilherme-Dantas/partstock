from celery import shared_task
from django.utils import timezone
from .services.sheet_upload_service import PartImporterService

@shared_task
def import_parts_task(task_id):
    PartImporterService.process_csv_file(task_id)
