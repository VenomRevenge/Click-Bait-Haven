from django.shortcuts import render
from articles.models import Article
from django.core.paginator import Paginator
from profiles.helpers import check_for_mod_or_admin_permissions


@check_for_mod_or_admin_permissions
def article_review(request):
    articles =( 
        Article.objects
        .articles_that_need_approval()
        .select_related('author__user')
        .only(
                'id',
                'author__id',
                'author__user__username', 
                'picture', 
                'title', 
                'created_at',
            )
        .order_by('created_at')
    )

    num_articles = articles.count()
    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'num_articles': num_articles,
        'articles': page_obj,
        'page_number': page_number,
    }

    return render(request, 'moderation_system/article-review.html', context)