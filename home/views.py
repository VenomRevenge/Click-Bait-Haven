from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from home.forms import RegisterForm, SignInForm
from profiles.models import Profile


def index(request):
    return render(request, 'home/index.html')


class Register(FormView):
    template_name = 'home/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')


    def form_valid(self, form):
        user = form.save()   
        Profile.objects.create(user=user)
        login(self.request, user)
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
        return reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["message"] = True
        return context