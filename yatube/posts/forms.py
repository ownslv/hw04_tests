from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["text", "group"]
        labels = {
            'group': 'Группа',
            'text': 'Текст',
        }
        help_texts = {'text': "Введите текст поста",
                      'group': "Выберете группу"}
