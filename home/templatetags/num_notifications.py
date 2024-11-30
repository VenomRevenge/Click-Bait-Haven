from django import template

from articles.models import Article
from profiles.helpers import is_admin_staff_mod

register = template.Library()

@register.simple_tag
def get_user_notifications_count(user):
    """
    Returns the number of unread notifications for the user, including articles
    that need approval if the user is a moderator or admin.
    """

    user_notifications = user.profile.notifications.filter(viewed=False).count()

    if is_admin_staff_mod(user):
        user_notifications += Article.objects.articles_that_need_approval().count()

    return user_notifications if user_notifications < 100 else '+99'