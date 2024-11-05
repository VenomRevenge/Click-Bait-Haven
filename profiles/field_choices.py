from django.db import models

class GenderChoices(models.TextChoices):
    MALE = ("Male", "Male")
    FEMALE = ("Female", "Female")
    UNSPECIFIED = ("Unspecified", "Unspecified")


class Roles(models.TextChoices):
    CITIZEN_JOURNALIST = ("Citizen Journalist", "Citizen Journalist")
    CONFIRMED_JOURNALIST = ("Confirmed Journalist", "Confirmed Journalist")
    MODERATOR = ("Moderator", "Moderator")
    ADMIN = ("Admin", "Admin")