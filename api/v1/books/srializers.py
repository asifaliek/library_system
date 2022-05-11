from rest_framework import serializers

from books.models import Book,BookTracking


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "pk",
            "date_of_publication",
            "author",
            "name",
            'is_in_library'
        )

class BookTrackingSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    book = serializers.SerializerMethodField()
    class Meta:
        model = BookTracking
        fields = (
            "pk",
            "book",
            "customer",
            "start_date",
            "end_date",
        )

    def get_customer(self, obj):
        return obj.customer.username

    def get_book(self, obj):
        return obj.book.name