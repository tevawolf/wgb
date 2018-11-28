from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import list
from django.views.generic import edit
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms
from . import models

import hashlib


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


class LoginView(AuthLoginView):
    form_class = forms.LoginForm

    """ログイン実行"""
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            auth_login(request, form.user_cache)
            return redirect(reverse('WGB:top'))

        return render(request, 'login.html', {'form': form})


login = LoginView.as_view()


class LogoutView(AuthLogoutView):
    """ログアウト実行"""
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect(reverse('WGB:top'))


logout = LogoutView.as_view()


class CreateUserView(edit.FormView):
    """ユーザー登録ページ表示"""
    form_class = forms.CreateUserForm
    template_name = 'create_user.html'


create_user = CreateUserView.as_view()


class ExecuteCreateUserView(View):
    """ユーザー登録実行"""
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


class CreateThreadView(edit.FormView):
    """掲示板作成画面表示"""
    form_class = forms.CreateThreadForm
    template_name = 'create_thread.html'


create_thread = CreateThreadView.as_view()


class ExecuteCreateThreadView(View):
    """掲示板作成実行"""
    def post(self, request, *args, **kwargs):
        form = forms.CreateThreadForm(request.POST)
        if not form.is_valid():
            return render(request, 'create_thread.html', {'form': form})

        thread = form.save()
        password = form.cleaned_data['password']
        if password:
            thread.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            thread.save()
        # 掲示板参加者として作成者を登録
        member = models.ThreadMember()
        member.thread = thread
        member.member = request.user
        member.create = True
        member.save()
        # 最初の書き込みを登録
        write = models.ThreadWrite()
        write.thread = thread
        write.number = 1
        write.member = member
        write.sentence = form.cleaned_data['first_write']
        write.save()

        return redirect(reverse('WGB:top'))


execute_create_thread = ExecuteCreateThreadView.as_view()


class ShowThreadView(View):
    """掲示板ページ表示"""
    def get(self, request, thread_no, *args, **kwargs):
        thread = models.Threads.objects.get(thread_no=thread_no)
        form = forms.ThreadWriteForm()
        context = {
            'thread': thread,
            'form': form,
        }
        return render(request, 'thread.html', context)


show_thread = ShowThreadView.as_view()


class ThreadWriteView(View):
    """掲示板書き込み実行"""
    def post(self, request, thread_no, *args, ** kwargs):
        form = forms.ThreadWriteForm(request.POST)
        if not form.is_valid():
            return render(request, 'thread.html',
                          {
                              'form': form,
                              'thread': models.Threads.objects.get(thread_no=thread_no),
                          })

        write = form.save()

        # 添付ファイルの保存

        return redirect(reverse('WGB:show_thread', thread_no))


write_thread = ThreadWriteView.as_view()
