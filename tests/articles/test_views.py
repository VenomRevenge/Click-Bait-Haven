from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from articles.models import Article
from profiles.models import Profile


class ArticleViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = self.user.profile
        self.article = Article.objects.create(author=self.profile, title='Test Article', content='Test content' * 10, is_approved=True)

    def test_article_create_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('article_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article-create.html')

    def test_article_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('article', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article.html')
        self.assertContains(response, self.article.title)

    def test_article_edit_view(self):
        self.client.login(username='testuser', password='password123')

        # Include all required fields in the POST data
        response = self.client.post(
            reverse('article_edit', kwargs={'pk': self.article.pk}),
            {
                'title': 'Updated Title',
                'content': 'Updated content with enough length to pass validation.' * 10,
                'tags': [],
            }
        )

        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Title')
        self.assertEqual(self.article.content, 'Updated content with enough length to pass validation.' * 10)

    def test_article_delete_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('article_delete', kwargs={'pk': self.article.pk}))
        self.assertRedirects(response, reverse('index'))
        self.article.refresh_from_db()
        self.assertIsNotNone(self.article.deleted_at)

    def test_article_search_view(self):
        response = self.client.get(reverse('article_search'), {'title': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article-search.html')
        self.assertContains(response, self.article.title)

    def test_article_edit_view_invalid_data(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(
            reverse('article_edit', kwargs={'pk': self.article.pk}),
            {'title': 'Short', 'content': '', 'tags': []}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.') 
        self.article.refresh_from_db()
        self.assertNotEqual(self.article.title, 'Short') 

