from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import list
from django.views.generic import edit
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from . import forms
from . import models
from .character_decoration import CharacterDecoration

import hashlib
import html


class MemberChecker:
    def member_check(self, request, thread):
        if not request.user.is_authenticated\
                or not models.ThreadMember.objects.filter(thread=thread, member=request.user).exists():
            messages.add_message(request, messages.WARNING, '不正な操作です。')
            return False
        else:
            return True


class MessageWriter:
    def decorate(self, message):
        escape_sentence = html.escape(message)
        cd = CharacterDecoration()
        return cd.decorate(escape_sentence)


class TopPageView(list.ListView):
    """トップページ表示"""
    model = models.Threads
    template_name = 'thread_list.html'
    paginate_by = 50
    ordering = ['-thread_no']


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


class ExecuteCreateThreadView(View, MessageWriter):
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
        # 文字装飾
        write.sentence = self.decorate(form.cleaned_data['first_write'])
        write.save()
        # 画像添付

        return redirect(reverse('WGB:top'))


execute_create_thread = ExecuteCreateThreadView.as_view()


class ShowThreadView(View, MemberChecker):
    """掲示板ページ表示"""
    def get(self, request, thread_no, *args, **kwargs):
        thread = models.Threads.objects.get(thread_no=thread_no)
        # 参加チェック
        if thread.open_level == 0 and not self.member_check(request, thread):
            return redirect(reverse('WGB:top'))

        form = forms.ThreadWriteForm()
        context = {
            'thread': thread,
            'form': form,
        }
        return render(request, 'thread.html', context)


show_thread = ShowThreadView.as_view()


class ThreadWriteView(View, MemberChecker, MessageWriter):
    """掲示板書き込み実行"""
    def post(self, request, thread_no, *args, ** kwargs):

        # 認証
        if not self.member_check(request, thread_no):
            return redirect(reverse('WGB:top'))

        form = forms.ThreadWriteForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'thread.html',
                          {
                              'form': form,
                              'thread': models.Threads.objects.get(thread_no=thread_no),
                          })

        write = form.save()
        # 文字装飾
        write.sentence = self.decorate(write.sentence)
        write.save()

        # 添付ファイルの保存
        attach1 = form.cleaned_data['attachment1']
        if attach1:
            self.create_attach(write, 1, attach1)
        attach2 = form.cleaned_data['attachment2']
        if attach2:
            self.create_attach(write, 2, attach2)
        attach3 = form.cleaned_data['attachment3']
        if attach3:
            self.create_attach(write, 3, attach3)

        return redirect(reverse('WGB:show_thread', args=[thread_no]))

    def create_attach(self, write, seq, attachment):
        attach = models.ThreadWriteAttachment()
        attach.thread_write = write
        attach.sequence = seq
        attach.attachment = attachment
        attach.save()


write_thread = ThreadWriteView.as_view()


class JoinMemberView(View):
    """掲示板参加実行"""
    def post(self, request, *args, **kwargs):
        password = request.POST['password']
        thread_no = request.POST['thread_no']
        thread = models.Threads.objects.get(thread_no=thread_no)
        if thread.password == hashlib.sha256(password.encode('utf-8')).hexdigest():
            member = models.ThreadMember()
            member.thread = thread
            member.member = request.user
            member.create = False
            member.save()
            return redirect(reverse('WGB:show_thread', args=[thread_no]))
        else:
            messages.add_message(request, messages.WARNING, 'パスワードが間違っています。')
            return redirect(reverse('WGB:top'))


join_member = JoinMemberView.as_view()


class ShowJoinThreadListView(View):
    """参加掲示板・メンバー一覧ページ表示"""
    def get(self, request, *args, **kwargs):
        members = models.ThreadMember.objects.filter(member=request.user)
        threads = []
        for m in members:
            threads.append(m.thread)
        return render(request, 'join_thread_list.html', {'threads': threads})


show_join_thread_list = ShowJoinThreadListView.as_view()


class ShowSenderListView(View, MemberChecker):
    """送受信メッセージ一覧ページ表示"""
    def get(self, request, thread_no, member_id, *args, **kwargs):

        # 参加チェック
        if not self.member_check(request, thread_no):
            return redirect(reverse('WGB:top'))

        member_object = models.ThreadMember.objects.get(pk=member_id)
        member_self = models.ThreadMember.objects.get(thread=thread_no, member=request.user)
        pop_message = models.DirectMessage.objects.filter(from_member=member_object, to_member=member_self).order_by('-send_datetime')
        send_message = models.DirectMessage.objects.filter(from_member=member_self, to_member=member_object).order_by('-send_datetime')
        thread_title = models.Threads.objects.get(thread_no=thread_no).thread_title
        context = {
            'member': member_object,
            'pop': pop_message,
            'send': send_message,
            'thread_no': thread_no,
            'thread_title': thread_title
        }
        return render(request, 'sender_list.html', context)


show_sender_list = ShowSenderListView.as_view()


class SendMessageView(View, MemberChecker):
    """メッセージ送信ページ表示"""
    def get(self, request, thread_no, member_id, *args, **kwargs):

        # 参加チェック
        if not self.member_check(request, thread_no):
            return redirect(reverse('WGB:top'))

        form = forms.DirectMessageForm
        from_member = models.ThreadMember.objects.get(thread=thread_no, member=request.user)
        to_member = models.ThreadMember.objects.get(pk=member_id)
        if models.DirectMessage.objects.filter(from_member=from_member, to_member=to_member).exists():
            next_sequence = models.DirectMessage.objects.filter(
                from_member=from_member, to_member=to_member
            ).latest().next_sequence()
        else:
            next_sequence = 1
        context = {
            'from_member': from_member,
            'to_member': to_member,
            'form': form,
            'sequence': next_sequence,
        }
        return render(request, 'send_message.html', context)


send_message = SendMessageView.as_view()


class ExecuteSendMessageView(View, MessageWriter):
    """メッセージ送信実行"""
    def post(self, request, *args, **kwargs):
        form = forms.DirectMessageForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'send_message.html', {'form': form, })

        message = form.save()
        # 文字装飾
        message.message = self.decorate(form.cleaned_data['message'])
        message.save()

        # 添付ファイルの保存
        attach1 = form.cleaned_data['attachment1']
        if attach1:
            self.create_attach(message, 1, attach1)
        attach2 = form.cleaned_data['attachment2']
        if attach2:
            self.create_attach(message, 2, attach2)
        attach3 = form.cleaned_data['attachment3']
        if attach3:
            self.create_attach(message, 3, attach3)

        member = form.cleaned_data['to_member']
        return redirect(reverse('WGB:show_sender_list', args=[member.thread.thread_no, member.id]))

    def create_attach(self, message, seq, attachment):
        attach = models.DirectMessageAttachment()
        attach.message = message
        attach.sequence = seq
        attach.attachment = attachment
        attach.save()


exe_send_message = ExecuteSendMessageView.as_view()


class ShowMessageView(View, MemberChecker):
    """メッセージ表示ページ"""
    def get(self, request, message_id, member_object_id, *args, **kwargs):

        message = models.DirectMessage.objects.get(pk=message_id)
        thread = models.Threads.objects.get(thread_no=message.from_member.thread.thread_no)

        # 参加チェック
        if not self.member_check(request, thread.thread_no):
            return redirect(reverse('WGB:top'))

        context = {
            'message': message,
            'thread': thread,
            'member_object_id': member_object_id,
        }
        return render(request, 'show_message.html', context)


show_message = ShowMessageView.as_view()

