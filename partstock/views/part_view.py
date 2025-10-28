from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from partstock.services.part_service import PartService
from partstock.models import Part
from partstock.serializers import PartSerializer, PartUpdateSerializer
from partstock.permissions import IsAdminUserOrReadOnly
from rest_framework.permissions import IsAuthenticated


class ListAndCreatePart(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    def get(self, request, format=None):
        queryset = PartService.get_all_parts() 

        serializer = PartSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PartSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                new_part = PartService.create_new_part(
                    validated_data=serializer.validated_data
                )
                response_serializer = PartSerializer(new_part) 

                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(
                {'detail': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class PartDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    def get(self, request, pk, format=None):
        part = PartService.get_by_id(pk)
        serializer = PartSerializer(part)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        serializer = PartUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            updated_part = PartService.update_part(
                part_id=pk,
                validated_data=serializer.validated_data
            )
            response_serializer = PartSerializer(updated_part)

            return Response(response_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        PartService.delete_part(part_id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT) 
