from datetime import timezone
from django.db import models
from django.core.validators import MinLengthValidator
from articles.managers import ArticleManager
from profiles.models import Profile
from profiles.validators import validate_image_size
from PIL import Image


class Tag(models.Model):
    NAME_MAX_LENGTH = 20

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                limit_value=3
            ),
        ],
        unique=True,
    )


class Article(models.Model):
    TITLE_MAX_LENGTH = 50
    TITLE_MIN_LENGTH = 10
    CONTENT_MAX_LENGTH = 15_000
    CONTENT_MIN_LENGTH = 500
    PICTURE_HELP_TEXT = "The article picture will be automatically resized to 1920x1080px"
    PICTURE_WIDTH = 1920
    PICTURE_HEIGHT = 1080

    author = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='articles',
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                limit_value=TITLE_MIN_LENGTH,
            ),
        ],
        unique=True,
    )

    content = models.TextField(
        max_length=CONTENT_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                limit_value=CONTENT_MIN_LENGTH,
            ),
        ],
    )

    picture = models.ImageField(
        blank=True,
        null=True,
        upload_to='article_pictures',
        validators=[validate_image_size],
        help_text=PICTURE_HELP_TEXT,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    tags = models.ManyToManyField(
        to=Tag,
    )

    is_approved = models.BooleanField(
        default=False,
    )

    approved_by = models.ForeignKey(
        to=Profile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_articles',
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )


    objects = ArticleManager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()


    def resize_image(self):
        """Resizes the article picture to 1920wx1080l"""
        if self.picture:
            img = Image.open(self.picture.path)

            if img.width != Article.PICTURE_WIDTH or img.height != Article.PICTURE_HEIGHT:
                img = img.resize(
                    (Article.PICTURE_WIDTH, Article.PICTURE_HEIGHT),
                    Image.LANCZOS,
                )
                img.save(self.picture.path)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.picture:
            self.resize_image()

    def __str__(self):
        return self.title