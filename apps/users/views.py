from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import Client
from apps.users.serializers import ClientReadSerializer, ClientWriteSerializer


class ClientsView(generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    """
    A class-based view for handling client-related operations in a Django REST framework.

    Inherits from ListAPIView, CreateAPIView, RetrieveAPIView, and DestroyAPIView.

    Attributes:
        queryset (QuerySet): The list of clients to be used in the views.
        serializer_class (Serializer): The serializer class to be used for serializing and deserializing client data.

    Example Usage:
        # Create an instance of the `ClientsView` class
        clients_view = ClientsView()

        # List all clients
        response = clients_view.list(request)

        # Create a new client
        response = clients_view.create(request)

        # Retrieve a specific client
        response = clients_view.retrieve(request, pk)

        # Update a specific client
        response = clients_view.update(request, pk)

        # Delete a specific client
        response = clients_view.destroy(request, pk)
    """

    queryset = Client.objects.all()
    serializer_class = ClientReadSerializer

    def get_serializer_class(self):
        """
        Determines the serializer class to be used based on the request method.

        Returns:
            Serializer: The appropriate serializer class based on the request method.
        """
        if self.request.method == "GET":
            return ClientReadSerializer
        return ClientWriteSerializer

    def list(self, request, *args, **kwargs):
        """
        Handles GET requests to list all clients or retrieve a specific client.

        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data or the retrieved client object.
        """
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
        """
        Handles POST requests to create a new client.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The serialized data of the created client object.
        """
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        """
        Handles PUT requests to update a specific client.

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the client object to be updated.

        Returns:
            Response: The serialized data of the updated client object.
        """
        client = get_object_or_404(Client, pk=pk)
        serializer = self.get_serializer_class()(client, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Handles DELETE requests to delete a specific client.

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the client object to be deleted.

        Returns:
            Response: The HTTP response with no content.
        """
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
