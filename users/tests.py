from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Follow, Post

User = get_user_model()


class TestPosts(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='sarah', email='connor.s@skynet.com', password='12345')
        self.user2 = User.objects.create_user(
            username='john', email='connor.j@skynet.com', password='09876')

    def test_profile_page(self):
        self.client.force_login(self.user)
        response = self.client.get(f'/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

    def test_auth_user_following(self):
        self.client.force_login(self.user)

        self.client.get(reverse('profile_follow', kwargs={
                        'username': self.user2.username}))
        self.assertEqual(Follow.objects.count(), 1)

        self.client.get(reverse('profile_unfollow', kwargs={
                        'username': self.user2.username}))
        self.assertEqual(Follow.objects.count(), 0)

    def test_only_auth_user_can_comment(self):
        self.client.force_login(self.user)
        user_post = Post.objects.create(
            text="Текст тестового поста", author=self.user)
        self.client.post(
            f'/{self.user.username}/{user_post.id}/comment/',
            {
                'text': 'Текст комментария авторизованного пользователя',
                'author': '{self.user}',
                'post': '{user_post}'
            }
        )
        auth_response = self.client.get(
            f'/{self.user.username}/{user_post.id}/')
        self.assertContains(
            auth_response, "Текст комментария авторизованного пользователя", status_code=200)

        self.client.logout()
        not_auth_response = self.client.post(
            f'/{self.user.username}/{user_post.id}/comment/',
            {
                'text': 'Текст комментария авторизованного пользователя',
                'author': '{self.user}',
                'post': '{user_post}'
            }
        )
        self.assertRedirects(
            not_auth_response, '/auth/login/?next=/sarah/1/comment/')
