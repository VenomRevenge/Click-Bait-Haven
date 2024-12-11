from django.test import TestCase
from django.urls import reverse
from profiles.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = self.user.profile
        self.profile.bio = "This is a test bio."
        self.profile.save()


    def test_profile_details_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile_details', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertContains(response, self.profile.bio)

    def test_profile_edit_view_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile_edit', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile-edit.html')

    def test_profile_edit_view_post(self):
        self.client.login(username='testuser', password='password123')
        post_payload = {
            'bio': 'Updated bio',
            'gender': self.profile.gender,
            'date_of_birth': '',
        }
        response = self.client.post(reverse('profile_edit', kwargs={'pk': self.profile.pk}), post_payload)
        self.assertRedirects(response, reverse('profile_details', kwargs={'pk': self.profile.pk}))
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')

    def test_profile_delete_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('profile_delete', kwargs={'pk': self.profile.pk}), {'password': 'password123'})
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(Profile.objects.filter(pk=self.profile.pk).exists())
