from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from partstock.services.stock_movement_service import StockMovementService
from partstock.models import StockMovement
from partstock.serializers import (
    StockMovementSerializer, StockMovementUpdateSerializer
)
from partstock.permissions import IsAdminUserOrReadOnly
from rest_framework.permissions import IsAuthenticated


class ListAndCreateStockMovement(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    def get(self, request, format=None):
        queryset = StockMovementService.get_all_movements() 

        serializer = StockMovementSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StockMovementSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                new_movement = StockMovementService.create_new_movement(
                    validated_data=serializer.validated_data
                )
                response_serializer = StockMovementSerializer(new_movement) 

                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(
                {'detail': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class StockMovementDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            movement = StockMovementService.get_by_id(pk)
            serializer = StockMovementSerializer(movement)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StockMovement.DoesNotExist as e:
            return Response(
                {'detail': str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, pk, format=None):
        try:
            serializer = StockMovementUpdateSerializer(
                data=request.data, partial=True
                )
            if serializer.is_valid(raise_exception=True):
                updated_movement = StockMovementService.update_movement(
                    pk=pk,
                    validated_data=serializer.validated_data
                )
                response_serializer = StockMovementSerializer(updated_movement)

                return Response(response_serializer.data, status=status.HTTP_200_OK)
        except StockMovement.DoesNotExist as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, format=None):
        try:
            StockMovementService.delete_movement(pk=pk)
            return Response(status=status.HTTP_204_NO_CONTENT) 
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
