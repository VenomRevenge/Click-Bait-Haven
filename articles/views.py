from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from articles.forms import ArticleCreateForm, ArticleSearchForm
from articles.models import Article, Tag
from profiles.helpers import has_confirmed_journalist_perms, is_admin_staff_mod, is_profile_owner_or_permission


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'articles/article-create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = self.request.user
        profile = user.profile

        article = form.save(commit=False)
        article.author = profile
        if has_confirmed_journalist_perms(user):
            article.is_approved = True
        article.save()
        form.save_m2m()

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perms'] = has_confirmed_journalist_perms(self.request.user)
        return context
    

def article_view(request, pk):

    user = request.user
    article = get_object_or_404(Article, pk=pk)
    author = article.author
    tags = article.tags.all()
    approval_phase = False

    # only superusers can view soft-deleted articles
    if article.deleted_at and not user.is_superuser:
        raise Http404
    
    # if user doesn't have perms then he cant view article under approval
    elif not article.is_approved and not is_admin_staff_mod(user):
        raise PermissionDenied
    
    # if this is true then the article is in approval phase and the user has permissions
    elif not article.is_approved:
        approval_phase = True


    context = {
        'author': author,
        'article': article,
        'tags': tags,
        'approval_phase': approval_phase,
        'edit_button': is_profile_owner_or_permission(user, author)
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