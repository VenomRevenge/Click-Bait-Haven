from django.db import models
from django.contrib.auth import get_user_model
from profiles.field_choices import GenderChoices, Roles
from profiles.validators import validate_image_size
from PIL import Image


# Create your models here.
user = get_user_model()

# Extending through OneToOne cause I wont use this data much
class Profile(models.Model):

    GENDER_MAX_LENGTH = 15
    BIO_MAX_LENGTH = 200
    PROFILE_PIC_WIDTH = 500
    PROFILE_PIC_HEIGHT = 500
    PROFILE_PIC_HELP_TEXT = "Your profile picture will be automatically resized to 500x500px"
    MAX_ROLE_LENGTH = 30

    user = models.OneToOneField(
        to=user,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        unique=True,
    )

    gender = models.CharField(
        max_length=GENDER_MAX_LENGTH,
        choices=GenderChoices.choices,
        default=GenderChoices.UNSPECIFIED,
    )

    bio = models.TextField(
        max_length=BIO_MAX_LENGTH,
        blank=True,
        null=True,
    )

    profile_picture = models.ImageField(
        blank=True,
        null=True,
        validators=[validate_image_size],
        upload_to='profile_pictures',
    )

    # TODO: Make this assign automatically on user and profile change
    role = models.CharField(
        max_length=MAX_ROLE_LENGTH,
        choices=Roles.choices,
        default=Roles.CITIZEN_JOURNALIST,
    )


    def resize_image(self):
        """Resizes the profile picture to 500wx500l"""
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)

            if img.width != Profile.PROFILE_PIC_WIDTH or img.height != Profile.PROFILE_PIC_HEIGHT:
                img = img.resize(
                    (Profile.PROFILE_PIC_WIDTH, Profile.PROFILE_PIC_HEIGHT),
                    Image.LANCZOS,
                )
                img.save(self.profile_picture.path)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_picture:
            self.resize_image()


    def __str__(self):
        return self.user.username
    

    class Meta: 
        permissions = [
            ("confirmed_journalist", "Automatically approve all posts by this user"),
            ("moderator", "This user has moderation permissions"),
        ]