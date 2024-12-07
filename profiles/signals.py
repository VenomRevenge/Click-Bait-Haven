from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.field_choices import Roles
from profiles.models import Profile

UserModel = get_user_model()

CONFIRMED_JOURNALIST = 'profiles.confirmed_journalist'
MODERATOR = 'profiles.moderator'

@receiver(post_save, sender=UserModel)
def create_profile_and_update_perms(sender, instance, created, **kwargs):

    if created:
        Profile(user=instance).save()

    if instance.is_active and hasattr(instance, 'profile'):
        profile = instance.profile

        if instance.is_superuser:
            profile.role = Roles.ADMIN
        elif instance.is_staff:
            profile.role = Roles.MODERATOR
        elif instance.has_perm(MODERATOR):
            profile.role = Roles.MODERATOR
        elif instance.has_perm(CONFIRMED_JOURNALIST):
            profile.role = Roles.CONFIRMED_JOURNALIST
        else:
            profile.role = Roles.CITIZEN_JOURNALIST

        profile.save()