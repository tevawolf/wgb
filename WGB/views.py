from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import list
from django.views.generic import edit
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms
from . import models


class TopPageView(list.ListView):
    """トップページ表示"""
    model = models.Threads
    template_name = 'thread_list.html'
    paginate_by = 50


top_page = TopPageView.as_view()


class ShowLoginView(AuthLoginView):
    """ログインページ表示"""
    form_class = forms.LoginForm
    template_name = 'login.html'


show_login = ShowLoginView.as_view()


class LoginView(AuthLoginView, LoginRequiredMixin):
    """ログイン実行"""
    form_class = forms.LoginForm

    def get(self, *args, **kwargs):
        self.login(self.request)
        return redirect('WGB:top')


login = LoginView.as_view()


class LogoutView(AuthLogoutView):
    """ログアウト実行"""
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('WGB:top')


logout = LogoutView.as_view()


class CreateUserView(edit.FormView):
    """ユーザー登録表示"""
    form_class = forms.CreateUserForm
    template_name = 'create_user.html'


create_user = CreateUserView.as_view()


class ExecuteCreateUserView(View):
    """トップページ実行"""
    def post(self, request, *args, **kwargs):
        form = forms.CreateUserForm(request.POST)
        if not form.is_valid():
            return render(request, 'create_user.html', {'form': form})

        user = form.save()
        # パスワードは改めてUserオブジェクトにセットしてセーブしないと暗号化されない
        # (変な仕様・・・)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect(reverse('WGB:top'))


execute_create_user = ExecuteCreateUserView.as_view()
