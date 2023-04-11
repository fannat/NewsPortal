from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Post
import datetime



class PostForm(forms.ModelForm):
    head_post = forms.CharField(required=False)

    class Meta:
       model = Post
       fields = ['head_post', 'text_post', 'author', 'cathegories']


    def clean(self):
        cleaned_data = super().clean()
        head_post = cleaned_data.get("head_post")
        text_post = cleaned_data.get("text_post")
        if text_post is not None and len(text_post) < 20:
            raise ValidationError({
                "text_post": "Текст не может быть менее 20 символов."
            })
        if not head_post:
            cleaned_data['head_post'] = datetime.datetime.now()

        return cleaned_data


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

