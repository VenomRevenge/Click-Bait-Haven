from django.core.exceptions import PermissionDenied
from functools import wraps

CONFIRMED_JOURNALIST = 'profiles.confirmed_journalist'
MODERATOR = 'profiles.moderator'
def is_profile_owner_or_permission(user, profile) -> bool:

    if not user.is_authenticated:
        return False
    
    return user.profile.pk == profile.pk or user.is_staff or user.is_superuser


def has_confirmed_journalist_perms(user) -> bool:
    return user.has_perm(CONFIRMED_JOURNALIST) or user.has_perm(MODERATOR) or user.is_staff or user.is_superuser


def is_admin_staff_mod(user):
    return user.is_staff or user.is_superuser or user.has_perm(MODERATOR)


def check_for_mod_or_admin_permissions(view):
    """
    Checks mod or admin permissions before executing a FBV.
    Raises 403 if user doesn't meet conditions.
    """

    @wraps(view)
    def wrapper(request, *args, **kwargs):

        user = request.user
        if not is_admin_staff_mod(user):
            raise PermissionDenied
        
        return view(request, *args, **kwargs)
    
    return wrapper