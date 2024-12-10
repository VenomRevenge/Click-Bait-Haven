from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from articles.models import Article
from django.core.paginator import Paginator
from moderation_system.models import Notification
from profiles.helpers import check_for_mod_or_admin_permissions
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages


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
    message = 'You have succesfully approved this article'

    # in case mod tries to approve a rejected article
    if article.deleted_at and not user.is_superuser:
        raise Http404
    # in case mod or admin tries to approve an already approved article so notif doesnt get created
    elif article.is_approved and not article.deleted_at:
        messages.error(request, 'That article is already approved!')
        return redirect('article', pk)

    article.is_approved = True
    article.approved_at = timezone.now()
    article.approved_by = user.profile

    # superusers can re-approve rejected articles if they so want
    if user.is_superuser and article.deleted_at:
        message = 'You have successfully re-instated the article!'
        article.deleted_at = None

    article.save()

    Notification.objects.create(
        profile=article.author,
        reviewer=user.profile,
        is_positive_review=True,
        article_title=article.title,
        article_id=article.id,
    )
    messages.success(request, message)

    return redirect('review_page')


@login_required
@check_for_mod_or_admin_permissions
def reject_article(request, pk):

    user = request.user
    article = get_object_or_404(Article, pk=pk)
    reason = request.POST.get('reason_for_rejection', None)
    message = 'You have successfully rejected the article.'

    # only superusers can actually delete articles but they need to be soft deleted first
    # also there doesnt need to be a new notification for actual deletion
    if article.deleted_at and user.is_superuser:
        article.delete()
        messages.success(request, 'You have successfully deleted the article')
        return redirect('deleted_articles')
    
    # is this check passes then a non-superuser moderator is trying to delete a soft deleted article
    elif article.deleted_at and not user.is_superuser:
        raise Http404

    # in case a mod/admin tries to reject an already approved article
    if article.is_approved:
        messages.success(request, 'That article is already approved!')
        return redirect('article', pk)
    # if the request is not POST or there is no reason given then redirect back to article page
    elif request.method != 'POST' or not reason or len(reason) == 0:
        messages.error(request, 'Please enter a reason for rejection!')
        return redirect('article', pk)
    elif len(reason) > 500:
        messages.error(request, 'The reson must be within 500 charactes in length')
    
    
    article.soft_delete()
    
    Notification.objects.create(
        profile=article.author,
        reviewer=user.profile,
        is_positive_review=False,
        reason_for_rejection=reason,
        article_title=article.title,
        article_id=article.id,
    )
    messages.success(request, message)

    return redirect('review_page')
    