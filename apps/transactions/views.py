from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.transactions.models import Transaction
from apps.transactions.serializers import TransactionReadSerializer, ValidateSerializer


class TransactionsView(ListAPIView, RetrieveAPIView, DestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionReadSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TransactionReadSerializer
        return TransactionReadSerializer

    def list(self, request, *args, **kwargs):
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
    serializer_class = ValidateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer.failed(details=serializer.errors, data=request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
