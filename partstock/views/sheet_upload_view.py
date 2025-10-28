# seuapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from partstock.serializers import SheetUploadSerializer, TaskStatusSerializer
from partstock.tasks import import_parts_task
from partstock.models import UploadTask


class PartUpload(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SheetUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']

        upload_task = UploadTask.objects.create(
            file_name=file.name,
            uploaded_file=file,
            status='PENDING'
        )
        task = import_parts_task.delay(upload_task.id)

        upload_task.celery_task_id = task.id
        upload_task.save()

        return Response(
            {
                'message': 'Import started successfully.',
                'task_id': upload_task.id
            },
            status=status.HTTP_202_ACCEPTED
        )


class TaskDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            upload_task = UploadTask.objects.get(pk=pk)
        except UploadTask.DoesNotExist:
            return Response(
                {"detail": "Task ID not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskStatusSerializer(upload_task)

        return Response(serializer.data, status=status.HTTP_200_OK)
