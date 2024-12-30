from datetime import date

from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BookDetailSerializer, BookListSerializer, CommentSerializer, GenreSerializer, BorrowSerializer, ReadingListSerializer, ReviewSerializer, BookProgressSerializer

from .models import Book, Comment, Genre, Borrow, ReadingList, Review, ReadingProgress


class BookListView(APIView):

    def get(self, request):
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)


class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        try:
            book = Book.objects.get(uuid=uuid.__str__())
        except Book.DoesNotExist:
            return Response(status=404)

        serializer = BookDetailSerializer(book, context={'request': request})
        return Response(serializer.data)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_uuid):
        try:
            book = Book.objects.get(uuid=book_uuid)
        except Book.DoesNotExist:
            return Response(status=404)

        comment = Comment(book=book, comment=request.data['text'])
        comment.save()
        return Response({'message': 'Comment created successfully'}, status=201)


class CommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, book_uuid):
        try:
            book = Book.objects.get(uuid=book_uuid)
        except Book.DoesNotExist:
            return Response(status=404)

        comments = Comment.objects.filter(book=book)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True, context={'request': request})
        return Response(serializer.data)


class BorrowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        borrowed_books = Borrow.objects.all()
        serializer = BorrowSerializer(borrowed_books, many=True)
        return Response(serializer.data)

    def post(self, request):
        title = request.data.get('title')
        try:
            book_uuid = Book.objects.get(title=title)
        except Book.DoesNotExist:
            return Response({'message': 'Book not found'}, status=404)
        user_uuid = User.objects.get(username=request.data.get('username'))
        borrowed_book = Borrow(book_uuid=book_uuid, user_uuid=user_uuid, borrow_date=date.today())
        borrowed_book.save()
        return Response({'message': 'Book borrowed successfully'}, status=201)

    def delete(self, request, uuid):
        borrowed_book = Borrow.objects.get(uuid=uuid)
        borrowed_book.delete()
        return Response(status=204)


class ReadingListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user_reading_lists = ReadingList.objects.filter(user_uuid=request.user)
        serializer = ReadingListSerializer(user_reading_lists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReadingListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_uuid=request.user)  # Automatically associate with the logged-in user
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SearchView(APIView):
    def get(self, request):
        q = request.query_params.get('q')
        if q:
            books = Book.objects.filter(title__icontains=q)
            print(books.query)

        else:
            books = Book.objects.all()
        serializer = BookDetailSerializer(books, many=True)
        return Response(serializer.data, status=200)


class ReviewListView(APIView):

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ReviewDetailView(APIView):
    def get(self, request, uuid):
        review = Review.objects.get(uuid=uuid.__str__())
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def patch(self, request, uuid):
        review = Review.objects.get(uuid=uuid.__str__())
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, uuid):
        review = Review.objects.get(uuid=uuid.__str__())
        review.delete()
        return Response(status=204)


class ReadingListDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ReadingList.objects.get(pk=pk, user_uuid=self.request.user)
        except ReadingList.DoesNotExist:
            return None

    def get(self, request, pk):
        """Retrieve a specific reading list item."""
        reading_list_entry = self.get_object(pk)
        if reading_list_entry is None:
            return Response(status=404)

        serializer = ReadingListSerializer(reading_list_entry)
        return Response(serializer.data)

    def put(self, request, pk):
        """Update a reading list item."""
        reading_list_entry = self.get_object(pk)
        if reading_list_entry is None:
            return Response(status=404)

        serializer = ReadingListSerializer(reading_list_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        """Delete a reading list item."""
        reading_list_entry = self.get_object(pk)
        if reading_list_entry is None:
            return Response(status=404)

        reading_list_entry.delete()
        return Response(status=204)


class BookProgressList(APIView):
    def get(self, request):
        book_progresses = ReadingProgress.objects.all()
        serializer = BookProgressSerializer(book_progresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookProgressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BookProgressDetail(APIView):
    def get(self, request, pk):
        book_progress = ReadingProgress.objects.get(pk=pk)
        serializer = BookProgressSerializer(book_progress)
        return Response(serializer.data)

    def patch(self, request, pk):
        book_progress = ReadingProgress.objects.get(pk=pk)
        serializer = BookProgressSerializer(book_progress, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        book_progress = ReadingProgress.objects.get(pk=pk)
        book_progress.delete()
        return Response(status=204)