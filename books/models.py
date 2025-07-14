from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD", "Hard"
        SOFT = "SOFT", "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=10,
        choices=CoverChoices.choices,
    )
    inventory = models.PositiveIntegerField(default=0)
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "book"
        verbose_name_plural = "books"
        ordering = ("title", "author")
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author", "cover"],
                name="unique_title_and_author_cover",
            )
        ]

    def __str__(self):
        return f"{self.title} (author: {self.author})"
