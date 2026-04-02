from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from partstock.services.movement_item_service import MovementItemService
from partstock.serializers import MovementItemSerializer
from partstock.permissions import IsAdminUserOrReadOnly
from rest_framework.permissions import IsAuthenticated


class ListAndCreateMovementItem(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    def get(self, request, format=None):
        queryset = MovementItemService.get_all_movements()

        serializer = MovementItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MovementItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_movement = MovementItemService.create_new_movement(
                validated_data=serializer.validated_data
            )
            response_serializer = MovementItemSerializer(new_movement)

            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
                )


class MovementItemDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    def get(self, request, pk, format=None):
        movement = MovementItemService.get_by_id(pk)
        serializer = MovementItemSerializer(movement)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        MovementItemService.delete_movement(pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
