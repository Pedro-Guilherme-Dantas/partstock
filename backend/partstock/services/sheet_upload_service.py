import csv
from django.utils import timezone
from partstock.models import UploadTask
from .part_service import PartService
from django.db import transaction


class PartImporterService:
    @staticmethod
    @transaction.atomic
    def process_csv_file(task_id):
        upload_task = UploadTask.objects.get(pk=task_id)
        file_path = upload_task.uploaded_file.path

        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for i, row in enumerate(reader):
                    cost = float(row['Custo por unidade'])
                    initial_stock = int(row['Quantidade inicial'])
                    current_price = float(row['Preço'])

                    part_data = {
                        'name': row['Nome'],
                        'description': row['Descrição'],
                        'current_price': current_price,
                        'current_stock': initial_stock,
                        'cost': cost,
                    }

                    PartService.create_new_part(part_data)

            upload_task.status = 'COMPLETED'

        except Exception as e:
            error_msg = (
                f"Fatal import error (All transactions rolled back): {e}"
            )

            upload_task.status = 'FAILED'
            upload_task.error_message = error_msg

        finally:
            upload_task.finished_at = timezone.now()
            upload_task.save()
