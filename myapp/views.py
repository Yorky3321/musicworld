from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from .models import Music, MusicPost, Vote, Comment, ChatRoom, Message, Post, PostComment
from .forms import MusicUploadForm, PostForm, PostCommentForm, VoteForm, CommentForm


# --- 首頁音樂排行榜 + 發文（支援投票與留言） ---
def home(request):
    music_list = Music.objects.all().order_by('-created_at')
    paginator = Paginator(music_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 留言提交處理
    if request.method == 'POST' and 'comment_submit' in request.POST:
        comment_form = CommentForm(request.POST)
        music_id = request.POST.get('music_id')
        music = get_object_or_404(Music, id=music_id)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.music = music
            comment.save()
            messages.success(request, '留言成功！')
            return redirect('home')  # 回首頁
    else:
        comment_form = CommentForm()

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'comment_form': comment_form,
    })


# --- 音樂上傳 ---
@login_required
def upload_music(request):
    if request.method == 'POST':
        form = MusicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            music = form.save(commit=False)
            music.uploader = request.user
            music.save()
            messages.success(request, '上傳成功')
            return redirect('home')
    else:
        form = MusicUploadForm()
    return render(request, 'upload_music.html', {'form': form})

# --- 投票功能 ---
@login_required
def vote_view(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    value = int(request.POST.get('value'))

    vote, created = Vote.objects.get_or_create(
        user=request.user,
        music=music,
        defaults={'value': value}
    )

    if not created:
        vote.value = value
        vote.save()

    return redirect('home')
# --- 登入/登出/註冊 ---
def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            messages.success(request, '登入成功')
        else:
            messages.error(request, '登入失敗')
        return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, '已登出')
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        User = get_user_model()
        if request.POST['password1'] != request.POST['password2']:
            messages.error(request, '兩次密碼不一致')
        elif User.objects.filter(username=request.POST['username']).exists():
            messages.error(request, '帳號已存在')
        else:
            User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password1']
            )
            messages.success(request, '註冊成功！')
        return redirect('home')
    return redirect('home')

# --- 聊天室 ---
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, pk=room_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        tag = request.POST.get('tag', '')  # ← 預設空字串，避免錯誤
        anonymous_name = request.POST.get('anonymous_name', '')

        if content:
            Message.objects.create(
                room=room,
                user=request.user if request.user.is_authenticated else None,
                anonymous_name=anonymous_name,
                content=content,
                tag=tag
            )
            return redirect('chat-room', room_id=room_id)

    messages_list = room.messages.order_by('created_at')
    return render(request, 'chat_room.html', {
        'room': room,
        'messages': messages_list,
    })

# --- 五線譜 ---
def melody(request):
    return render(request, 'melody.html')

def music_detail(request, pk):
    music = get_object_or_404(Music, pk=pk)
    comments = music.comments.order_by('-created_at')
    comment_form = CommentForm()
    return render(request, 'music_detail.html', {
        'music': music,
        'comments': comments,
        'comment_form': comment_form,
    })
@login_required
def post_comment(request, pk):
    music = get_object_or_404(Music, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.music = music
        comment.user = request.user
        comment.save()
        messages.success(request, "留言成功！")
    else:
        messages.error(request, "留言失敗")
    return redirect('music_detail', pk=pk)
@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        return redirect('home')

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('music_detail', pk=comment.music.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})
@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.user != request.user:
        return HttpResponseForbidden("你無權刪除這則訊息")

    room_id = message.room.id
    message.delete()
    messages.success(request, "留言已刪除")
    return redirect('chat-room', room_id=room_id)
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        return HttpResponseForbidden("你無權刪除此留言")

    music_id = comment.music.id
    comment.delete()
    messages.success(request, "留言已刪除")
    return redirect('music_detail', pk=music_id)
@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.user != request.user:
        return HttpResponseForbidden("你無權編輯這則訊息")

    if request.method == 'POST':
        message.content = request.POST.get('content')
        message.tag = request.POST.get('tag', '')
        message.save()
        messages.success(request, '留言已更新')
        return redirect('chat-room', room_id=message.room.id)

    return render(request, 'edit_message.html', {'message': message})
