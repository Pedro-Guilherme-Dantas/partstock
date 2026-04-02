from partstock.models import MovementItem, StockMovement
from django.db import transaction


class StockMovementService:
    @staticmethod
    def get_all_movements():
        return StockMovement.objects.all()

    @staticmethod
    def get_by_id(pk: int) -> StockMovement:
        try:
            return StockMovement.objects.get(pk=pk)
        except StockMovement.DoesNotExist:
            raise StockMovement.DoesNotExist(
                f'movement with id {pk} not found'
                )

    @staticmethod
    @transaction.atomic
    def create_new_movement(validated_data: dict) -> StockMovement:
        if validated_data['movement_type'] not in dict(
            StockMovement.MOVEMENT_TYPES
        ):
            raise ValueError('Invalid Movement Type')

        new_movement = StockMovement.objects.create(**validated_data)
        return new_movement

    @staticmethod
    @transaction.atomic
    def update_movement(pk: int, validated_data: dict) -> StockMovement:
        movement = StockMovementService.get_by_id(pk)
        movement.notes = validated_data.get('notes', movement.notes)
        movement.save()
        return movement

    @staticmethod
    @transaction.atomic
    def delete_movement(pk: int) -> None:
        movement = StockMovementService.get_by_id(pk)
        if MovementItem.objects.filter(part=pk).count() > 0:
            raise ValueError(
                'Unable to delete the item. There is a movement item history'
                )
        movement.delete()
