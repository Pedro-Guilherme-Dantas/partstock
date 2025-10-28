from celery import shared_task
from django.utils import timezone
from .services.sheet_upload_service import PartImporterService
from .services.part_service import PartService

@shared_task
def import_parts_task(task_id):
    PartImporterService.process_csv_file(task_id)

@shared_task
def replenish_stock_task():
    try:
        updated_count = PartService.replenish_stock()
        return f"Replacement completed. {updated_count} parts fitted."
    except Exception as e:
        raise