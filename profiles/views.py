
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.models import Profile

class ProfileDetails(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile.html'
    context_object_name = 'profile'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['buttons'] = self.request.user.profile.pk == self.object.pk
        return context