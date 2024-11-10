from django.db import models

class ArticleManager(models.Manager):

    def active_articles(self):
        return self.all().filter(deleted_at__isnull=True)
    