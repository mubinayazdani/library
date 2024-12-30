import uuid

from django.db import models

from users.models import User


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_time"]


class Author(BaseModel):
    name = models.CharField(max_length=150)
    biography = models.TextField()
    email = models.EmailField()

    class Meta:
        db_table = 'Author'
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def __str__(self):
        return f'{self.name}'


class Genre(BaseModel):
    genre = models.CharField(max_length=150)

    class Meta:
        db_table = 'Genre'
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return f'{self.genre}'


class Book(BaseModel):
    title = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre, related_name='books')
    picture = models.ImageField(upload_to='bookimgs/')
    author_uuid = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now=True)
    publisher = models.CharField(max_length=150)
    isbn = models.IntegerField()
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    file = models.FileField()

    class Meta:
        db_table = 'Book'
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        return f'{self.title}'


class Comment(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f'{self.uuid}'


class Borrow(BaseModel):
    user_uuid = models.ForeignKey(User, on_delete=models.CASCADE)
    book_uuid = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now=True)
    return_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Borrow'
        verbose_name = 'borrow'
        verbose_name_plural = 'borrows'

    def __str__(self):
        return f'Borrowed {self.book_uuid.title}'


class ReadingList(BaseModel):
    Borrowed = 1
    Reading = 2
    Finished = 3
    Dropped = 4

    STATUS_CHOICES = (
        (Borrowed, 'Borrowed'),
        (Reading, 'Reading'),
        (Finished, 'Finished'),
        (Dropped, 'Dropped')
    )
    user_uuid = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_lists')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=Borrowed)

    def __str__(self):
        return f"{self.user_uuid.username} - {self.book_id.title}"


class Review(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()

    def __str__(self):
        return f'{self.book}'


class ReadingProgress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    pages_read = models.IntegerField()
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.book}'


class SearchQuery(models.Model):
    query = models.CharField(max_length=255)
    results = models.TextField()
