from django import forms
from .models import Post, PostComment, Music, Comment

class VoteForm(forms.Form):
    value = forms.ChoiceField(
        choices=[('1', '👍'), ('-1', '👎')],
        widget=forms.HiddenInput
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border-2 border-black px-4 py-2 rounded',
                'placeholder': '請輸入文章標題'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full border-2 border-black px-4 py-2 rounded',
                'rows': 5,
                'placeholder': '推薦的音樂內容或想法...'
            }),
        }

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'w-full border px-3 py-2 rounded',
                'rows': 3,
                'placeholder': '留言內容...'
            })
        }

class MusicUploadForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'description', 'audio_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control border-2 border-black px-4 py-2 rounded',
                'placeholder': '請輸入歌曲名稱'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control border-2 border-black px-4 py-2 rounded',
                'rows': 3,
                'placeholder': '簡短描述這首歌...'
            }),
            'audio_file': forms.ClearableFileInput(attrs={
                'class': 'form-control border-2 border-black px-4 py-2 rounded'
            }),
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': '寫下你的留言...',
                'class': 'w-full p-2 border border-gray-300 rounded'
            })
        }

def music_detail(request, pk):
    music = get_object_or_404(Music, pk=pk)
    comments = Comment.objects.filter(music=music).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.music = music
            comment.user = request.user
            comment.save()
            return redirect('music_detail', pk=music.pk)
    else:
        form = CommentForm()

    return render(request, 'music_detail.html', {
        'music': music,
        'comments': comments,
        'form': form
    })