
from rest_framework.permissions import IsAuthenticated,AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from books.models import Book,BookTracking
from .srializers import BookSerializer,BookTrackingSerializer
from core.pagination import StandardResultsSetPagination
import datetime
from .utils import EmailThread

class BookFilterView(ListAPIView):
    """
    fetching list of Book using filters
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ("name", "author", "date_of_publication")
    ordering_fields = ("name", "author", "date_of_publication")
    search_fields = ("name", "author", "date_of_publication")


class BookTrackingFilterView(ListAPIView):
    """
    fetching list of BookTracking using filters
    """
    queryset = BookTracking.objects.all()
    serializer_class = BookTrackingSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ("book", "customer", "end_date")
    ordering_fields = ("book", "customer", "end_date")
    search_fields = ("book", "customer", "end_date")



class MarkAsBorrowed(APIView):
    """
    * mark status  of book
    * Method: POST Only
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = BookTrackingSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            book = serializer.validated_data["book"]
            customer = serializer.validated_data["customer"]
            data = Book.objects.get(pk=book)
            data.is_in_library=False
            data.save()
            serializer.save(creator=user)

            email_data = {
                "subject": "Successfully Borrowed.",
                "recipient": customer.email,
                "username": customer.username,
            }
            """The e-mail will be send in a separate thread"""
            EmailThread(email_data).start()

            response_data = {"status": True, "data": serializer.data}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_as_returned(request, pk):
    """
    * mark return of borrowed books
    * Method: POST Only
    """
    borrowed_item = BookTracking.objects.get(pk=pk)
    user = borrowed_item.customer
    book = borrowed_item.book
    book.is_in_library = True
    book.save()
    borrowed_item.is_returned = True
    borrowed_item.save()

    email_data = {
        "subject": "Successfully returned.",
        "recipient": user.email,
        "username": user.username,
    }
    """The e-mail will be send in a separate thread"""
    EmailThread(email_data).start()

    response_data = {"status": True, "data": "successfully marked as returned."}
    return Response(response_data, status=status.HTTP_201_CREATED)
