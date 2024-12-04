import random
from django.db.models import Count, Q, F, FloatField, ExpressionWrapper
from django.db.models.functions import Coalesce, NullIf
from articles.models import Article

def get_featured_articles():
    """
    Returns the top 3 featured articles based on certain citeria:
        1. Takes their likes and dislikes and annotates them
        2. Annotates another field (score) so it can get a like/dislike ratio
        3. orders them by their score then likes then created at date
        4. Returns only the fields that matter for the front page
        5. Limits the query to only 3 results
    """

    articles = (
        Article.objects.active_articles()
            .annotate(
                likes=Count('reactions', filter=Q(reactions__reaction_type='Like')),
                dislikes=Count('reactions', filter=Q(reactions__reaction_type='Dislike')),
                score=ExpressionWrapper(
                F('likes') / NullIf(Coalesce(F('dislikes'), 0), 0),
                output_field=FloatField()
            )
            )
            .order_by('-score', '-likes', '-created_at')
            .values(
                'id',
                'title',
                'picture',
                'created_at',
                'author__user__username'
        )[:3]
    )
    return articles


def get_recent_articles():
    """
    Return the 9 most recent approved articles,
    only the fields that matter for the front-page 
    """
    
    articles = (
        Article.objects.active_articles()
            .order_by('-created_at')
            .values(
                'id',
                'title',
                'created_at',
                'author__user__username'
            )[:9]
    )
    return articles


def get_random_article_pk():
    """
    Returns the ID of a random active article from the database.
    """
    article_ids = list(Article.objects.active_articles().values_list('id', flat=True))

    if not article_ids:
        return False
    
    random_id = random.choice(article_ids)

    return random_id

                    