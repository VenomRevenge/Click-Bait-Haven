from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.http import Http404
from django.db.models import Prefetch
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from articles.field_choices import ReactionChoices
from articles.forms import ArticleCreateForm, ArticleEditForm, ArticleSearchForm, CommentEditForm
from articles.models import Article, ArticleReaction, Comment, CommentReaction
from profiles.helpers import has_confirmed_journalist_perms, is_admin_staff_mod, is_profile_owner_or_permission


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'articles/article-create.html'
    success_url = reverse_lazy('index')
    DEFAULT_SUCCESS_MESSAGE = 'Your article has been published for review!'

    def form_valid(self, form):
        user = self.request.user
        profile = user.profile

        article = form.save(commit=False)
        article.author = profile
        if has_confirmed_journalist_perms(user):
            self.DEFAULT_SUCCESS_MESSAGE = 'Your article has been published!'
            article.is_approved = True
        article.save()
        form.save_m2m()
        messages.success(self.request, self.DEFAULT_SUCCESS_MESSAGE)
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perms'] = has_confirmed_journalist_perms(self.request.user)
        return context
    

@login_required
def article_edit(request, pk):

    article = get_object_or_404(Article, pk=pk)
    user = request.user
    default_success_message = 'The article has been successfully edited!'

    # only superusers can view and edit deleted articles
    if article.deleted_at and not user.is_superuser:
        raise Http404
    # if its not the article's author or a superuser raise error    
    if not user.is_superuser and not user.profile == article.author:
        raise PermissionDenied
    # only superusers can edit unapproved or rejected articles
    if not article.is_approved and not user.is_superuser:
        raise PermissionDenied
    
    form = ArticleEditForm(request.POST or None, request.FILES or None, instance=article)

    if request.method == 'POST' and form.is_valid():
        article = form.save(commit=False)
        # If the user editind the article lacks perms, then article needs to be
        # reapproved
        if not has_confirmed_journalist_perms(request.user):
            article.is_approved = False
            default_success_message = 'Your article has been successfully edited and resubmitted for review.'

        article.save()
        form.save_m2m()
        url = reverse("index")

        if not article.is_approved and user.is_superuser:
            url = reverse('article', kwargs={'pk': article.pk})

        messages.success(request, default_success_message)
        return redirect(url)
    
    context = {
        'warning_message': not has_confirmed_journalist_perms(request.user),
        'form': form,
        'article': article,
    }
    return render(request, 'articles/article-edit.html', context)



@login_required
def article_delete(request, pk):
    user = request.user
    article = get_object_or_404(Article, pk=pk)

    if article.deleted_at and not user.is_superuser:
        raise Http404
    if not user.is_superuser and not user.profile == article.author:
        raise PermissionDenied
    if not article.is_approved and not user.is_superuser:
        raise PermissionDenied
    
    if request.method == 'POST':
        messages.success(request, 'Article deleted successfully!')
        # if passed all checks above and this its implied a superuser
        # is trying to hard delete a soft deleted article
        if article.deleted_at:
            article.delete()
            return redirect('deleted_articles')
        else:
            article.soft_delete()
            return redirect('index')
    # if deletion doesn't happen then just return to the article edit
    return redirect(reverse('article_edit', kwargs={'pk': article.pk}))


def article_view(request, pk):

    user = request.user
    # im not gonna lie its 2 AM im trying to optimize queries and this way less queries appear on the log
    # so im probably doing something right
    article_query = Article.objects.prefetch_related(
        Prefetch(
            'comments',
            queryset=Comment.objects.select_related('author').prefetch_related(
                Prefetch(
                    'reactions',
                    queryset=CommentReaction.objects.filter(profile=user.profile) if user.is_authenticated else CommentReaction.objects.none(),
                    to_attr='user_reactions'
                )
            ),
            to_attr='prefetched_comments'
        ),
        'tags'
    ).select_related('author').filter(pk=pk)

    if not article_query:
        raise Http404
    
    article = article_query[0]
    author = article.author
    tags = article.tags.all()
    approval_phase = False
    is_deleted_article = False
    user_reaction = None

    # only superusers can view soft-deleted articles
    if article.deleted_at and not user.is_superuser:
        raise Http404
    
    # if the article is deleted and user is admin then he can view it in full
    elif article.deleted_at and user.is_superuser:
        is_deleted_article = True

    # if user doesn't have perms then he cant view article under approval
    elif not article.is_approved and not is_admin_staff_mod(user):
        raise PermissionDenied
    
    # if this is true then the article is in approval phase and the user has permissions
    elif not article.is_approved:
        approval_phase = True

    # this returns Like or Dislike or None 
    if user.is_authenticated:
        user_reaction = article.reactions.filter(profile=user.profile).first()

    comments = article.prefetched_comments

    for comment in comments:
        comment.is_author_or_has_perms = is_profile_owner_or_permission(user, comment.author)
        comment.user_reaction = comment.user_reactions[0] if comment.user_reactions else None

    context = {
        'author': author,
        'article': article,
        'tags': tags,
        'approval_phase': approval_phase,
        'is_deleted_article': is_deleted_article,
        'edit_button': user.is_superuser or user.profile == article.author if user.is_authenticated else False,
        'user_reaction': user_reaction,
        'comments': comments,
    }
    return render(request, 'articles/article.html', context)


def article_search(request):
    form = ArticleSearchForm(request.GET or None)

    articles = (
        Article.objects
            .active_articles()
            .select_related('author__user')
            .prefetch_related('tags')
            .only(
                'id',
                'author__id',
                'author__user__username', 
                'picture', 
                'title', 
                'created_at',
            )
    )
    title_to_search = request.GET.get('title', None)
    author_to_search = request.GET.get('username', None)
    tags_to_search = request.GET.getlist('tag', None)
    ordering = request.GET.get('order_by', '-created_at')

    if title_to_search:
        articles = articles.filter(title__icontains=title_to_search)
    if author_to_search:
        articles = articles.filter(author__user__username__icontains=author_to_search)
    if tags_to_search:
        for tag in tags_to_search:
            articles = articles.filter(tags__name=tag)
    
    articles = articles.order_by(ordering)

    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_number': page_number,
        'articles': page_obj,
        'form': form,
    }
    return render(request, 'articles/article-search.html', context)

@login_required
def react_to_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    profile = request.user.profile
    url = f"{reverse('article', kwargs={'pk':pk})}#reactions"
    reaction_type = request.POST.get('reaction_type', None)

    # soft-deleted articles cannot be reacted on 
    if article.deleted_at:
        raise Http404
    
    # non-approved or rejected articles cannot be reacted on 
    elif not article.is_approved:
        raise PermissionDenied
    
    # if any of these checks passes then either someone tried to enter the
    # form action url without a post request or tampering with the payload
    # to see for potential bugs, Im just redirecting him back to the article, lol 
    elif not reaction_type or request.method != 'POST':
        return redirect(url)
    elif reaction_type not in [choice[0] for choice in ReactionChoices.choices]:
        return redirect(url)

    reaction, is_created = ArticleReaction.objects.get_or_create(profile=profile, article=article)

    # if the same reaction exists then remove it
    if not is_created and reaction.reaction_type == reaction_type:
        reaction.delete()
    # if this passes then either user wants to change his reaction or
    # its the first time hes reacting to the article 
    else:
        reaction.reaction_type = reaction_type
        reaction.save()

    return redirect(url)


@login_required
def react_to_comment(request, pk, comment_pk):
    article = get_object_or_404(Article, pk=pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    profile = request.user.profile
    url = f"{reverse('article', kwargs={'pk':pk})}#comment{comment_pk}"
    reaction_type = request.POST.get('reaction_type', None)

    # soft-deleted articles' comments cannot be reacted on 
    if article.deleted_at:
        raise Http404
    # non-approved or rejected articles' comments cannot be reacted on 
    elif not article.is_approved:
        raise PermissionDenied
    
    # if any of these checks passes then either someone tried to enter the
    # form action url without a post request or tampering with the payload
    # to see for potential bugs, Im just redirecting him back to the article, lol 
    elif not reaction_type or request.method != 'POST':
        return redirect(url)
    elif reaction_type not in [choice[0] for choice in ReactionChoices.choices]:
        return redirect(url)

    reaction, is_created = CommentReaction.objects.get_or_create(profile=profile, comment=comment)

    # if the same reaction exists then remove it
    if not is_created and reaction.reaction_type == reaction_type:
        reaction.delete()
    # if this passes then either user wants to change his reaction or
    # its the first time hes reacting to the article 
    else:
        reaction.reaction_type = reaction_type
        reaction.save()

    return redirect(url)


@login_required
def post_comment(request, pk):

    article = get_object_or_404(Article, pk=pk)
    user = request.user
    profile = user.profile

    # This is for some better UX
    url = f"{reverse('article', kwargs={'pk':pk})}#comments"

    content = request.POST.get('content')

    if request.method != 'POST':
        return redirect(url)
    
    # soft deleted and unapproved articles cannot be commented on
    if article.deleted_at or not article.is_approved:
        raise PermissionDenied

    # checking if the content is between the allowed length
    if content and (Comment.CONTENT_MIN_LENGTH <= len(content) <= Comment.CONTENT_MAX_LENGTH):
        Comment.objects.create(article=article, author=profile, content=content)
    else:
        messages.error(request, "Comment must be between 1 and 500 characters long")
    
    return redirect(url)


@login_required
def delete_comment(request, pk,  comment_pk):

    article = get_object_or_404(Article, pk=pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    comment_author_profile = comment.author
    user = request.user
    url = f"{reverse('article', kwargs={'pk':pk})}#comments"

    # raise 404 here cause only superusers can delete soft-deleted article's comments
    if article.deleted_at and not user.is_superuser:
        raise Http404
    
    # raising error if its not the author of the comment or no perms to delete
    if not is_profile_owner_or_permission(user, comment_author_profile):
        raise PermissionDenied
    
    # only delete on a POST request 
    if request.method == 'POST':
        comment.delete()
    
    return redirect(url)

@login_required
def edit_comment(request, pk, comment_pk):

    article = get_object_or_404(Article, pk=pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    form = CommentEditForm(request.POST or None, instance=comment)

    comment_author_profile = comment.author
    user = request.user
    url = f"{reverse('article', kwargs={'pk':pk})}#comments"

    # comments on soft-deleted articles cannot be edited
    if article.deleted_at:
        raise Http404

    # only superusers and staff can edit another user's comment
    if not is_profile_owner_or_permission(user, comment_author_profile):
        raise PermissionDenied

    if form.is_valid():
        form.save()
        return redirect(url)
    
    context = {
        'article': article,
        'comment': comment,
        'form': form,
    }
    return render(request, 'articles/edit-comment.html', context)