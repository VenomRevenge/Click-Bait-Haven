
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.forms import ProfileEditForm
from profiles.helpers import staff_or_superuser
from profiles.models import Profile

class ProfileDetails(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile.html'
    context_object_name = 'profile'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['buttons'] = user.profile.pk == self.object.pk or staff_or_superuser(user)
        return context
    

def profile_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    user = request.user

    if not (user.profile.pk == profile.pk or staff_or_superuser(user)):
        return redirect('index')
    
    form = ProfileEditForm(request.POST or None,request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile_details', profile.pk)
    context = {'form': form, 'profile': profile}
    
    return render(request, 'profiles/profile-edit.html', context)