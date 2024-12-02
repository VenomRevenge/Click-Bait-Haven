from django.db import models

class ReactionChoices(models.TextChoices):
    LIKE = ('Like', 'Like')
    DISLIKE = ('Dislike', 'Dislike')