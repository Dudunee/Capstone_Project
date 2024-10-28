from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """
    Model for storing movie reviews.
    Each review is associated with a user who created it.
    """

    movie_title = models.CharField(max_length=255)
    review_content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the review, useful for debugging.
        """
        return f"{self.movie_title} ({self.rating}/5)"
