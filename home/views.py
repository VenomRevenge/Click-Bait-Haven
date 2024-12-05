from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from articles.models import Article
from home.forms import RegisterForm, SignInForm
from home.helpers import get_featured_articles, get_random_article_pk, get_recent_articles
from moderation_system.models import Notification
from profiles.helpers import is_admin_staff_mod


def index(request):
    featured_articles = get_featured_articles()
    recent_articles = get_recent_articles()

    context = {
        'featured_articles': featured_articles,
        'recent_articles': recent_articles,
    }
    return render(request, 'home/index.html', context)

def random_article(request):
    article_pk = get_random_article_pk()

    if not article_pk:
        return redirect('home')
    
    return redirect('article', pk=article_pk)

class Register(FormView):
    template_name = 'home/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')


    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)


    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(*args, **kwargs)
    

class SignIn(LoginView):
    template_name = 'home/sign-in.html'
    form_class = SignInForm
    redirect_authenticated_user = True

    def get_redirect_url(self):
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url
        return reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["message"] = True
        return context
    

def sign_out(request): 
    if request.method == "POST":
        logout(request)

    return redirect('index')

@login_required
def my_notifications(request):

    user = request.user
    profile = request.user.profile 
    is_mod_or_admin = is_admin_staff_mod(user)

    # when page is opened mark all notifications as viewed
    profile.notifications.filter(viewed=False).update(viewed=True)

    notifications = (
        profile.notifications
        .select_related('reviewer__user')
        .only(
            'time_of_review',
            'is_positive_review',
            'reason_for_rejection',
            'article_title',
            'reviewer_id', 
            'reviewer__user__username'
        )
        .order_by('-time_of_review')
    )
    num_notifications = notifications.count()

    paginator = Paginator(notifications, 3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    
    context = {
        'page_number': page_number,
        'is_only_1_page': num_notifications <= 3,
        'is_moderator_or_admin': is_mod_or_admin,
        'notifications': page_obj,
        'num_notifications': num_notifications,
    }
    
    # mods and admin notifications also should consist of articles that havent been approved
    if is_mod_or_admin:
        num_unnaproved_articles = Article.objects.articles_that_need_approval().count()
        context['num_unnaproved_articles'] = num_unnaproved_articles
        context['num_notifications'] += num_unnaproved_articles

    return render(request,'home/my-notifications.html', context)


@login_required
def delete_notification(request, pk):

    referer_url = request.META.get("HTTP_REFERER", None)

    if request.method != 'POST' or not referer_url:
        return redirect('my_notifications')
    
    user = request.user
    profile = user.profile
    
    notification = get_object_or_404(Notification, pk=pk, profile=profile)
    notification.delete()

    return redirect(referer_url)