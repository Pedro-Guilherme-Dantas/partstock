from partstock.models import MovementItem, Part, StockMovement
from django.db import transaction

class MovementItemService:
    @staticmethod
    def get_all_movements():
        return MovementItem.objects.all()

    @staticmethod
    def get_by_id(pk: int) -> MovementItem:
        try:
            return MovementItem.objects.get(pk=pk)
        except MovementItem.DoesNotExist:
            raise MovementItem.DoesNotExist(
                f'movement item with id {pk} not found'
                )

    @staticmethod
    @transaction.atomic
    def create_new_movement(validated_data: dict) -> MovementItem:
        try:
            part = validated_data['part']
            stock_movement = validated_data['movement']
            quantity = validated_data.get('quantity', 0)

            if quantity == 0:
                raise ValueError('zero value in quantity is not valid')
            if stock_movement.movement_type == 'OUT' and quantity > part.current_stock:
                raise ValueError(
                    'The value of output items cannot be greater than the stock'
                    )
        except Part.DoesNotExist as e:
            raise e
        except StockMovement.DoesNotExist as e:
            raise e

        unit_price = validated_data.get('unit_price_at_transaction')
        unit_cost = validated_data.get('unit_cost_at_transaction')

        if not unit_price:
            validated_data['unit_price_at_transaction'] = part.current_price
        if not unit_cost:
            validated_data['unit_cost_at_transaction']  = part.cost

        new_movement_item = MovementItem.objects.create(**validated_data)

        return new_movement_item

    @staticmethod
    @transaction.atomic
    def delete_movement(pk: int) -> None:
        movement = MovementItemService.get_by_id(pk)
        movement.delete()
