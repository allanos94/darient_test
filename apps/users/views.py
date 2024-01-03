from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import Client
from apps.users.serializers import ClientReadSerializer, ClientWriteSerializer


class ClientsView(generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientReadSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClientReadSerializer
        return ClientWriteSerializer

    def list(self, request, *args, **kwargs):
        client_pk = self.kwargs.get("pk")
        if client_pk:
            return self.retrieve(request, *args, **kwargs)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer_class()(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        serializer = self.get_serializer_class()(client, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
