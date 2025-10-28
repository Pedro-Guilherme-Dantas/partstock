from rest_framework import serializers
from .models import MovementItem, Part, StockMovement, UploadTask


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = [
            'id',
            'name',
            'description',
            'cost',
            'current_price',
            'current_stock',
            'created_at',
            'updated_at',
            'is_active',
            ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'current_stock']


class PartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = [
            'id',
            'name',
            'description',
            'cost',
            'current_price',
            'is_active',
            ]
        read_only_fields = ['id', 'current_stock', 'created_at', 'updated_at']


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = [
            'id',
            'movement_type',
            'date_recorded',
            'notes',
        ]
        read_only_fields = ['id', 'date_recorded']


class StockMovementUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = [
            'id',
            'notes',
        ]
        read_only_fields = ['id', 'date_recorded', 'movement_type']


class MovementItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementItem
        fields = [
            'id',
            'movement',
            'part',
            'quantity',
            'unit_price_at_transaction',
            'unit_cost_at_transaction'
        ]
        read_only_fields = ['id']


class SheetUploadSerializer(serializers.Serializer):
    file = serializers.FileField() 

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("The file must be in CSV format.")
        return value


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadTask
        fields = ['id', 'status', 'error_message', 'file_name', 'started_at', 'finished_at']
        read_only_fields = fields
