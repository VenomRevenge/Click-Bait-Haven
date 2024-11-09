def staff_or_superuser(user):
    return user.is_staff or user.is_superuser