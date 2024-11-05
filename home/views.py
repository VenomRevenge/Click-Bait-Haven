from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView
from home.forms import RegisterForm
from profiles.models import Profile


def index(request):
    return render(request, 'home/index.html')


class Register(FormView):
    template_name = 'profiles/register.html'
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