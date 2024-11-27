from django.db import models
from articles.models import Article
from profiles.models import Profile


# Create your models here.
class Notification(models.Model):

    REASON_FOR_REJECTION_MAX_LENGTH = 500
    REASON_FOR_REJECTION_HELP_TEXT = 'Enter a reason for why the article is rejected.'

    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    time_of_review = models.DateTimeField(
        auto_now_add=True,
    )

    reviewer = models.ForeignKey(
        to=Profile,
        related_name='notification_reviews',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    viewed = models.BooleanField(
        default=False,
    )

    is_positive_review = models.BooleanField(
        default=True,
    )

    reason_for_rejection = models.TextField(
        help_text=REASON_FOR_REJECTION_HELP_TEXT,
        max_length=REASON_FOR_REJECTION_MAX_LENGTH,
    )

    article_title = models.CharField(
        max_length=Article.TITLE_MAX_LENGTH,
    )

    article_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Notification for {self.profile} - {'Approved' if self.is_positive_review else 'Rejected'}"