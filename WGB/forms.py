from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import FileExtensionValidator

from . import models


class LoginForm(AuthenticationForm):
    """ログインフォーム"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class CreateUserForm(forms.ModelForm):
    """ユーザー登録フォーム"""
    class Meta:
        model = models.UserAccount
        fields = ('username', 'password', 'nickname', 'email', 'icon',)
        widgets = {'password': forms.PasswordInput()}

    password2 = forms.CharField(
        label='パスワード確認用入力欄',
        required=True,
        strip=False,
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

        self.fields['nickname'].label = 'ニックネーム(任意)'
        self.fields['email'].label = 'メールアドレス(任意)'
        self.fields['icon'].label = 'アイコン画像(任意)'
        self.fields['icon'].required = False

    def clean(self):
        super(CreateUserForm, self).clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("パスワードの入力が確認用と一致しません")


class CreateThreadForm(forms.ModelForm):
    """掲示板作成フォーム"""
    class Meta:
        model = models.Threads
        fields = ('thread_title', 'open_level', 'password', 'create_date')
        widgets = {'password': forms.PasswordInput()}

    password2 = forms.CharField(
        label='パスワード確認用入力欄',
        required=True,
        strip=False,
        widget=forms.PasswordInput()
    )

    first_write = forms.CharField(
        label='最初に書き込む内容',
        required=True,
        max_length=5000,
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40})
    )

    attachment1 = forms.ImageField(label='画像添付１', required=False,
                                   validators=[FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png', ])], )
    attachment2 = forms.ImageField(label='画像添付２', required=False,
                                   validators=[FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png', ])], )
    attachment3 = forms.ImageField(label='画像添付３', required=False,
                                   validators=[FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png', ])], )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].label = '掲示板利用パスワード'
        self.fields['create_date'].required = False
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def clean(self):
        super(CreateThreadForm, self).clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("パスワードの入力が確認用と一致しません")


class ThreadWriteForm(forms.ModelForm):
    """掲示板書き込みフォーム"""
    class Meta:
        model = models.ThreadWrite
        fields = ('thread', 'number', 'member', 'sentence', )
        widgets = {'sentence': forms.Textarea(attrs={'rows': 4, 'cols': 40})}

    attachment1 = forms.ImageField(label='画像添付１', required=False,
                                   validators=[FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png', ])], )
    attachment2 = forms.ImageField(label='画像添付２', required=False,
                                   validators=[FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png', ])], )
    attachment3 = forms.ImageField(label='画像添付３', required=False,
                                   validators=[FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png', ])], )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class DirectMessageForm(forms.ModelForm):
    """メッセージ送信フォーム"""
    class Meta:
        model = models.DirectMessage
        fields = ('from_member', 'to_member', 'sequence', 'title', 'message', )
        widgets = {'message': forms.Textarea(attrs={'rows': 4, 'cols': 40})}

    attachment1 = forms.ImageField(label='画像添付１', required=False,
                                   validators=[FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png', ])], )
    attachment2 = forms.ImageField(label='画像添付２', required=False,
                                   validators=[FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png', ])], )
    attachment3 = forms.ImageField(label='画像添付３', required=False,
                                   validators=[FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png', ])], )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

