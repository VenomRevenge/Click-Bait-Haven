
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, edit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from profiles.forms import ProfileEditForm
from profiles.helpers import is_profile_owner_or_permission
from profiles.models import Profile


class ProfileDetails(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile.html'
    context_object_name = 'profile'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = self.object
        context['buttons'] = is_profile_owner_or_permission(user, profile)
        return context


class ProfileEdit(LoginRequiredMixin, edit.UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'profiles/profile-edit.html'


    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        user = self.request.user

        if not is_profile_owner_or_permission(user, profile):
            raise PermissionDenied
        
        return profile


    def form_valid(self, form):
        super().form_valid(form)
        return redirect('profile_details', self.object.pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context


    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.object.pk})
