from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, DetailView, edit
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password, make_password
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
        context['is_owner'] = profile.user == user
        context['is_admin_or_staff'] = user.is_staff or user.is_superuser
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


class ProfileDeleteOrBan(LoginRequiredMixin, View):
    template_name = 'profiles/profile-delete-ban.html'

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        user = request.user

        # Permission checks
        if not is_profile_owner_or_permission(user, profile):
            raise PermissionDenied

        context = self.get_context_data(user, profile)
        return render(request, self.template_name, context)

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        user = request.user

        if not is_profile_owner_or_permission(user, profile):
            raise PermissionDenied

        is_owner = profile.user == user

        # if the user is deleting their own profile
        if is_owner:
            password = request.POST.get('password', None)
            if not password or not check_password(password, user.password):
                context = self.get_context_data(user, profile)
                context['error'] = "Invalid password. Please try again."
                return render(request, self.template_name, context)

        # deactivate the user and make their password unusable
        profile.user.is_active = False
        profile.user.password = make_password(None)
        profile.user.save()
        profile.delete()

        # logout the user if they deleted their own profile
        if is_owner:
            logout(request)

        return redirect('index')

    def get_context_data(self, user, profile):
        context = {
            'is_owner': profile.user == user,
            'is_admin_or_staff': user.is_staff or user.is_superuser,
            'profile': profile
        }

        return context
