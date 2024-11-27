from django.db import models

class ArticleManager(models.Manager):


    def active_articles(self):
        return self.all().filter(deleted_at__isnull=True, is_approved=True)
    

    def articles_that_need_approval(self):
        return self.all().filter(deleted_at__isnull=True, is_approved=False)
    

    def soft_deleted_articles(self):
        return self.all().filter(deleted_at__isnull=False)