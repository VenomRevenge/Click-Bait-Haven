from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from articles.forms import ArticleCreateForm
from articles.models import Article
from profiles.helpers import has_confirmed_journalist_perms


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