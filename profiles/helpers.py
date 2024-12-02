from django.core.exceptions import PermissionDenied
from functools import wraps

CONFIRMED_JOURNALIST = 'profiles.confirmed_journalist'
MODERATOR = 'profiles.moderator'


def is_profile_owner_or_permission(user, profile) -> bool:
    """
    Checks if the given user is the owner of a given profile or if the
    user is a staff or superuser. Returns boolean based on the check.
    """

    if not user.is_authenticated:
        return False
    
    return user.profile.pk == profile.pk or user.is_staff or user.is_superuser


def has_confirmed_journalist_perms(user) -> bool:
    """
    Checks if the given user is a staff, superuser or has 
    confirmed journalist or moderator permissions. Returns boolean based on the check.
    """
    return user.has_perm(CONFIRMED_JOURNALIST) or user.has_perm(MODERATOR) or user.is_staff or user.is_superuser


def is_admin_staff_mod(user):
    """
    Checks if the given user is a staff, superuser or has 
    moderator permissions. Returns boolean based on the check.
    """
    return user.is_staff or user.is_superuser or user.has_perm(MODERATOR)


def check_for_mod_or_admin_permissions(view):
    """
    Decorates a FBV
    Checks for mod or admin permissions before executing a FBV.
    Raises 403 if user doesn't meet conditions.
    """

    @wraps(view)
    def wrapper(request, *args, **kwargs):

        user = request.user
        if not is_admin_staff_mod(user):
            raise PermissionDenied
        
        return view(request, *args, **kwargs)
    
    return wrapper