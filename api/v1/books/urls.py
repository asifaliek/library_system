from django.urls import path
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
import datetime

from core.pagination import StandardResultsSetPagination
from books.models import Book,BookTracking
from .srializers import BookSerializer,BookTrackingSerializer
from . import views

app_name = "books"

urlpatterns = [
    path(
        "",
        ListAPIView.as_view(
            queryset=Book.objects.filter(is_in_library=True),
            serializer_class=BookSerializer,
            pagination_class=StandardResultsSetPagination,
            permission_classes=[AllowAny],
        ),
    ),
    path(
        "view/<str:pk>/",
        RetrieveAPIView.as_view(
            queryset=Book.objects.filter(is_in_library=True),
            serializer_class=BookSerializer,
            permission_classes=[AllowAny],
        ),
    ),
    path(
        "tracking/",
        ListAPIView.as_view(
            queryset=BookTracking.objects.all(),
            serializer_class=BookTrackingSerializer,
            pagination_class=StandardResultsSetPagination,
            permission_classes=[AllowAny],
        ),
    ),
    path(
        "tracking/<str:pk>/",
        RetrieveAPIView.as_view(
            queryset=BookTracking.objects.all(),
            serializer_class=BookTrackingSerializer,
            permission_classes=[AllowAny],
        ),
    ),
    path(
        "due-books/",
        ListAPIView.as_view(
            queryset=BookTracking.objects.filter(end_date__lte=datetime.date.today()),
            serializer_class=BookTrackingSerializer,
            pagination_class=StandardResultsSetPagination,
            permission_classes=[IsAuthenticated],
        ),
    ),
    path("book-filter/", views.BookFilterView.as_view()),
    path("tracking-filter/", views.BookTrackingFilterView.as_view()),

    path("mark-as-borrowed/", views.MarkAsBorrowed.as_view(), name="mark_as_borrowed"),
    path("mark-as-returned/", views.mark_as_returned, name="mark_as_returned"),

]
