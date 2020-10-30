from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Follow, Post

User = get_user_model()


class TestPosts(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="sarah", email="connor.s@skynet.com", password="12345")
        self.user2 = User.objects.create_user(
            username='john', email='connor.j@skynet.com', password='09876')
        self.user3 = User.objects.create_user(
            username='terminator', email='terminator@skynet.com', password='56789')

    def test_new_post(self):
        self.client.force_login(self.user)
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_not_auth_new(self):
        response = self.client.get('/new/')
        self.assertRedirects(response, '/auth/login/?next=/new/')

    def test_new_post_pub(self):
        self.client.force_login(self.user)
        post = Post.objects.create(
            text="Текст тестового поста", author=self.user)

        pages = (
            '',
            f'/{self.user.username}/',
            f'/{self.user.username}/{post.id}/'
        )

        for page in pages:
            response = self.client.get(page)
            self.assertContains(
                response, 'Текст тестового поста', status_code=200)

    def test_post_edit(self):
        self.client.force_login(self.user)
        post = Post.objects.create(
            text="Текст тестового поста 2", author=self.user)
        post_edit = self.client.post(
            f'/{post.author}/{post.id}/edit/', {'text': 'Новый текст поста (ред.)'}, follow=True)

        pages = (
            '',
            f'/{self.user.username}/',
            f'/{self.user.username}/{post.id}/'
        )

        for page in pages:
            response = self.client.get(page)
            self.assertContains(
                response, 'Новый текст поста (ред.)', status_code=200)

    def test_404_error_page(self):
        response = self.client.get('/abrakadabra/')
        self.assertEqual(response.status_code, 404)

    def test_post_with_img(self):
        self.client.force_login(self.user)
        post = Post.objects.create(
            text="Текст тестового поста 777", author=self.user)
        with open('media\posts\leo.jpg', 'rb') as fp:
            self.client.post(
                f'/{self.user.username}/{post.id}/edit/', {'text': 'fred', 'image': fp})

        response = self.client.get(f'/{self.user.username}/{post.id}/')
        self.assertContains(response, '<img', status_code=200)

    def test_post_with_img_pages(self):
        self.client.force_login(self.user)
        post = Post.objects.create(
            text="Текст тестового поста 777", author=self.user)
        with open('media\posts\leo.jpg', 'rb') as fp:
            self.client.post(
                f'/{self.user.username}/{post.id}/edit/', {'text': 'fred', 'image': fp})

        pages = (
            '',
            f'/{self.user.username}/',
            f'/{self.user.username}/{post.id}/'
        )

        for page in pages:
            response = self.client.get(page)
            self.assertContains(response, '<img', status_code=200)

    def test_upload_not_img_file(self):
        self.client.force_login(self.user)
        post = Post.objects.create(
            text="Текст тестового поста 777", author=self.user)
        with open('media\posts\kirrik.txt', 'rb') as fp:
            response = self.client.post(
                f'/{self.user.username}/{post.id}/edit/', {'text': 'fred', 'image': fp})

        self.assertFalse(response.context['form'].is_valid())

    def test_new_post_only_for_followers(self):
        Post.objects.create(text="Текст тестового поста", author=self.user)
        Follow.objects.create(user=self.user2, author=self.user)

        self.client.force_login(self.user2)
        response = self.client.get('/follow/')
        self.assertContains(response, "Текст тестового поста", status_code=200)
        self.client.logout()

        self.client.force_login(self.user3)
        response = self.client.get('/follow/')
        self.assertNotContains(
            response, "Текст тестового поста", status_code=200)
