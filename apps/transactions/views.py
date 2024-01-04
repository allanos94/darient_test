from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.transactions.models import Transaction
from apps.transactions.serializers import TransactionReadSerializer, ValidateSerializer


class TransactionsView(ListAPIView, RetrieveAPIView, DestroyAPIView):
    """
    A view for handling HTTP requests related to transactions.

    Inherits from ListAPIView, RetrieveAPIView, and DestroyAPIView.

    Example Usage:
    ```python
    # Create an instance of TransactionsView
    view = TransactionsView()
    # Handle a GET request to retrieve a list of transactions
    response = view.list(request)
    # Handle a GET request to retrieve a single transaction
    response = view.retrieve(request, pk)
    ```

    Inputs:
    - request: The HTTP request object containing the data for the request.
    - pk: The primary key of the transaction to retrieve (for `TransactionsView`).

    Outputs:
    - response: The HTTP response object containing the serialized data and status code.
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionReadSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TransactionReadSerializer
        return TransactionReadSerializer

    def list(self, request, *args, **kwargs):
        """
        Handles GET requests for retrieving a list of transactions or a single transaction.

        If a `pk` parameter is provided, it calls the `retrieve` method to retrieve a single transaction.
        Otherwise, it retrieves a list of transactions from the database and returns the serialized data.

        Inputs:
        - request: The HTTP request object containing the data for the request.
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.

        Outputs:
        - response: The HTTP response object containing the serialized data and status code.
        """
        transaction_pk = self.kwargs.get("pk")
        if transaction_pk:
            return self.retrieve(request, *args, **kwargs)
        transactions = self.get_queryset()
        page = self.paginate_queryset(transactions)
        if page is not None:
            serializer = self.get_serializer_class()(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer_class()(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ValidateView(APIView):
    """
    A view for handling POST requests to validate and create a new transaction.

    Example Usage:
    ```python
    # Create an instance of ValidateView
    view = ValidateView()
    # Handle a POST request to validate and create a new transaction
    response = view.post(request)
    ```

    Inputs:
    - request: The HTTP request object containing the data for the request.

    Outputs:
    - response: The HTTP response object containing the serialized data and status code.
    """

    serializer_class = ValidateSerializer

    def post(self, request):
        """
        Handles POST requests to validate and create a new transaction.

        Creates an instance of the `ValidateSerializer` and passes the request data to it.
        If the serializer is valid, it saves the data and returns the serialized data with a status code of 201.
        If the serializer is not valid, it calls the `failed` method of the serializer to handle the failed transaction
        and returns the serializer errors with a status code of 400.

        Inputs:
        - request: The HTTP request object containing the data for the request.

        Outputs:
        - response: The HTTP response object containing the serialized data and status code.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer.failed(details=serializer.errors, data=request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
