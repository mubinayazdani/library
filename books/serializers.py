from rest_framework import serializers

from .models import Author, Book, Comment, Genre, Borrow, ReadingList, Review, ReadingProgress
from django.contrib.auth.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['uuid', 'genre']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'email']


class BookListSerializer(serializers.ModelSerializer):
    author_uuid = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['uuid', 'title', 'publisher', 'author_uuid', 'author_uuid']


class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    author_uuid = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['uuid', 'title', 'genre', 'picture', 'file','author_uuid', 'author_uuid', 'publisher', 'is_available']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['uuid', 'book', 'comment']


class BorrowSerializer(serializers.ModelSerializer):
    book_uuid = BookDetailSerializer()

    class Meta:
        model = Borrow
        fields = ['user_uuid', 'book_uuid', 'book_uuid', 'borrow_date', 'return_date']


class ReadingListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='book_id.title')
    username = serializers.CharField(source='user_uuid.username')

    class Meta:
        model = ReadingList
        fields = ['user_uuid', 'book_id', 'status', 'title']  # Add 'title' here

    def create(self, validated_data):

        title = validated_data.pop('book_title')
        username = validated_data.pop('user')['username']

        try:
            # Retrieve the book instance based on the title
            book = Book.objects.get(title=title)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book with the given title does not exist.")

        try:
            # Retrieve the user instance based on the username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with the given username does not exist.")

        # Create the Review instance
        validated_data['book'] = book
        validated_data['user'] = user
        return super().create(validated_data)








class ReviewSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(write_only=True)  # Accept book title
    username = serializers.CharField(source='user.username', write_only=True)  # Accept username

    class Meta:
        model = Review
        fields = ['book_title', 'username', 'rating', 'review_text']

    def create(self, validated_data):
        # Extract the username and book title from the request data
        book_title = validated_data.pop('book_title')
        username = validated_data.pop('user')['username']

        try:
            # Retrieve the book instance based on the title
            book = Book.objects.get(title=book_title)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book with the given title does not exist.")

        try:
            # Retrieve the user instance based on the username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with the given username does not exist.")

        # Create the Review instance
        validated_data['book'] = book
        validated_data['user'] = user
        return super().create(validated_data)


class BookProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingProgress
        fields = ['book', 'pages_read', 'completed', 'started_at', 'finished_at']