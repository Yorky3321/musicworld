from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# --- 使用者模型 ---
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('member', '一般會員'),
        ('creator', '創作者'),
        ('admin', '後台管理者'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    nickname = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, blank=True)
    avatar = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.username} 的個人資料"

# --- 音樂作品 ---
class Music(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='music/')
    created_at = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    def vote_score(self):
        return self.votes.aggregate(score=models.Sum('value'))['score'] or 0
    def vote_count(self):
        return self.votes.count()
    def __str__(self):
        return self.title

# --- 音樂投票與留言 ---

class Vote(models.Model):
    VOTE_CHOICES = ((1, '👍'), (-1, '👎'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    music = models.ForeignKey(Music, related_name='votes', on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VOTE_CHOICES, null=False)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'music')

class Comment(models.Model):
    music = models.ForeignKey(Music, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"

# --- 聊天室 ---
class ChatRoom(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

class Message(models.Model):
    TAG_CHOICES = [
        ('question', '問題'),
        ('announcement', '公告'),
        ('discussion', '討論'),
    ]
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    anonymous_name = models.CharField(max_length=50, blank=True)
    content = models.TextField(default="無內容")
    tag = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)




# --- 發文與留言功能 ---
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"

class MusicPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='music/')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def vote_score(self):
        return self.votes.aggregate(score=models.Sum('value'))['score'] or 0

    def __str__(self):
        return self.title

class MusicPostVote(models.Model):
    VOTE_CHOICES = ((1, '👍'), (-1, '👎'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(MusicPost, related_name='votes', on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class MusicPostComment(models.Model):
    post = models.ForeignKey(MusicPost, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    music = models.ForeignKey(Music, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"
