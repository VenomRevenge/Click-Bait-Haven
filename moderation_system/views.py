from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from articles.models import Article
from django.core.paginator import Paginator
from profiles.helpers import check_for_mod_or_admin_permissions
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


@login_required
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
        'review_page': True,
    }

    if request.user.is_superuser:
        context['num_deleted_articles'] = Article.objects.soft_deleted_articles().count()
        context['superuser_info_deleted'] = True

    return render(request, 'moderation_system/article-review.html', context)

@login_required
def deleted_articles(request):

    if not request.user.is_superuser:
        raise PermissionDenied
    
    articles =( 
        Article.objects
        .soft_deleted_articles()
        .select_related('author__user')
        .only(
                'id',
                'author__id',
                'author__user__username', 
                'picture', 
                'title', 
                'deleted_at',
            )
        .order_by('-deleted_at')
    )

    num_articles = articles.count()
    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'num_articles': num_articles,
        'articles': page_obj,
        'page_number': page_number,
        'review_page': False,
    }

    return render(request, 'moderation_system/article-review.html', context)


@login_required
@check_for_mod_or_admin_permissions
def approve_article(request, pk):


    user = request.user
    article = get_object_or_404(Article, pk=pk)
    if article.deleted_at and not user.is_superuser:
        raise Http404

    article.is_approved = True
    article.approved_at = timezone.now()
    article.approved_by = user.profile
    article.save()

    ## TODO: notify user of approved article


    return redirect('review_page')