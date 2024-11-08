from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from home.forms import RegisterForm, SignInForm


def index(request):
    return render(request, 'home/index.html')


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
