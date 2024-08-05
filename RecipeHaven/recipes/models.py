from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ("vegetarian", "Vegetarian"),
        ("non-vegetarian", "Non-Vegetarian"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=70)
    description = models.TextField(max_length=220)
    ingredients = models.TextField(max_length=350)
    steps_to_cook = models.TextField(max_length=700)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="vegetarian"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title[:10]}"


class Review(models.Model):
    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)
    comment = models.TextField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("recipe", "user")

    def __str__(self):
        return f"Rating{self.rating} by {self.user.username} for {self.recipe.title}"


# chat features


class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return str(self.room)
