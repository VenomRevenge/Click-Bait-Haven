from django.contrib import admin
from unfold.admin import ModelAdmin
from profiles.field_choices import Roles
from profiles.models import Profile
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Permission

user = get_user_model()

admin.site.unregister(Group)
admin.site.unregister(user)

@admin.register(Group)
class GroupAdmin(GroupAdmin, ModelAdmin):
    pass


@admin.register(user)
class UserAdmin(UserAdmin, ModelAdmin):

    list_display = [
        'username', 
        'email', 
        'is_staff', 
        'is_active', 
        'date_joined',
    ]

    search_fields = [
        'username',
        'email',
    ]

    list_filter = [
        'is_superuser' 
        ,'is_staff', 
        'is_active', 
        'date_joined',
    ]

    ordering = ['-date_joined']
    actions = [
        'deactivate_users', 
        'make_confirmed_journalist', 
        'make_moderator',
        'remove_all_permissions',
    ]

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"

    def make_confirmed_journalist(self, request, queryset):
        permission = Permission.objects.get(codename='confirmed_journalist')
        for user in queryset:
            user.user_permissions.clear()
            user.user_permissions.add(permission)
            user.profile.role = Roles.CONFIRMED_JOURNALIST
            user.profile.save()
            
    make_confirmed_journalist.short_description = 'Make users confirmed journalists'

    def make_moderator(self, request, queryset):
        permission = Permission.objects.get(codename='moderator')
        for user in queryset:
            user.user_permissions.clear()
            user.user_permissions.add(permission)
            user.profile.role = Roles.MODERATOR
            user.profile.save()

    make_moderator.short_description = 'Give users moderation permissions'

    def remove_all_permissions(self, request, queryset):
        for user in queryset:
            user.user_permissions.clear()
            user.profile.role = Roles.CITIZEN_JOURNALIST
            user.profile.save()
        self.message_user(request, "All permissions have been removed for the selected users.")
    remove_all_permissions.short_description = "Remove all permissions for selected users"

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):

    list_display = [
        'user', 
        'gender', 
        'role', 
        'date_of_birth', 
        'bio',
    ]
    search_fields = [
        'user__username',
        'bio',
    ]

    list_filter = [
        'gender', 
        'role',
    ]
    ordering = ['-date_of_birth']
