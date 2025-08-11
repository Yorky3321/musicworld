from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Music, Vote, Comment, ChatRoom

class UserAuthTest(APITestCase):
    def test_register(self):
        url = reverse('register')  # 需對應你的 users app url name
        data = {'username': 'test1', 'password': '12345678', 'password_confirm': '12345678', 'email': 'test1@test.com'}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

class MusicCRUDTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user1', password='pass')
        self.client.force_authenticate(self.user)
        self.music = Music.objects.create(title='test', description='desc', audio_file='file.mp3', uploader=self.user)

    def test_create_music(self):
        url = reverse('music-list')
        data = {'title': 'new song', 'description': 'desc', 'audio_file': 'file2.mp3'}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_music_ranking(self):
        url = reverse('music-ranking')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(resp.data, list))

class VoteTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user2', password='pass')
        self.music = Music.objects.create(title='vote-song', description='vote', audio_file='file.mp3', uploader=self.user)
        self.client.force_authenticate(self.user)

    def test_vote(self):
        url = reverse('vote-list')
        data = {'music': self.music.id, 'value': 1}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

class CommentTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user3', password='pass')
        self.music = Music.objects.create(title='comment-song', description='c', audio_file='file.mp3', uploader=self.user)
        self.client.force_authenticate(self.user)

    def test_create_comment(self):
        url = reverse('comment-list')
        data = {'music': self.music.id, 'content': 'Great song!'}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

class ChatRoomTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='chatuser', password='pass')
        self.client.force_authenticate(self.user)
        self.room = ChatRoom.objects.create(name='lobby')

    def test_online_count(self):
        url = reverse('room-online-count', args=[self.room.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
