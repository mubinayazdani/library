from django.urls import path
from .views import (BookListView, BookDetailView,
                    CommentView,
                    GenreListView, BorrowView,
                    SearchView,
                    ReadingListView, ReadingListDetailView,
                    ReviewListView, ReviewDetailView)

urlpatterns = [

    path('books/', BookListView.as_view(), name='book list'),
    path('books/<str:uuid>/', BookDetailView.as_view(), name='book detail'),

    path('comments/', CommentView.as_view(), name='comment-list'),
    path('comments/<uuid:book_uuid>/', CommentView.as_view(), name='comment-create'),


    path('genres/', GenreListView.as_view(), name='genre list'),

    path('borrow/', BorrowView.as_view(), name='borrow'),

    path('reading-list/', ReadingListView.as_view(), name='reading_list'),
    path('readinglist/<int:pk>/', ReadingListDetailView.as_view(), name='reading_list_detail'),


    path('search/', SearchView.as_view(), name='search'),

    path('reviews/', ReviewListView.as_view()),
    path('reviews/<str:uuid>/', ReviewDetailView.as_view()),
]