from django.contrib import admin
from .models import Author, Genre, Book, Comment, Borrow, ReadingList, Review, ReadingProgress


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']
    ordering = ['-created_time']


admin.site.register(Author, AuthorAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre']
    ordering = ['-created_time']


admin.site.register(Genre, GenreAdmin)


class ShowCommentInLine(admin.TabularInline):
    fields = ['comment']
    model = Comment
    extra = 0


admin.site.register(Comment)


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_uuid', 'published_date', 'publisher']
    list_filter = ['genre', 'published_date']
    ordering = ['-created_time']
    filter_horizontal = ['genre']
    inlines = [ShowCommentInLine]


admin.site.register(Book, BookAdmin)


class BorrowAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'book_uuid', 'user_uuid', ]
    ordering = ['-created_time']


admin.site.register(Borrow, BorrowAdmin)


class ReadingListAdmin(admin.ModelAdmin):
    list_display = ['user_uuid', 'user_uuid', 'status']
    ordering = ['user_uuid']


admin.site.register(ReadingList, ReadingListAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating']
    ordering = ['book']


admin.site.register(Review, ReviewAdmin)


class ReadingProgressAdmin(admin.ModelAdmin):

    list_display = ['user']
    ordering = ['user']


admin.site.register(ReadingProgress, ReadingProgressAdmin)