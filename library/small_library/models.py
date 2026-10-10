from django.db import models

class Author(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    is_available=models.BooleanField(default=True)
    author=models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
            return self.title
    