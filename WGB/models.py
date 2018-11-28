from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone

from datetime import datetime

from config import settings


class UserAccount(AbstractUser):
    class Meta:
        verbose_name = '利用者アカウント'
        verbose_name_plural = '0.利用者アカウント'
        db_table = 'user_account'

    nickname = models.CharField(verbose_name='ニックネーム', max_length=100, null=False, blank=True)
    icon = models.ImageField(verbose_name='アイコン画像パス', upload_to='icons/')

    def display_name(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username


class Threads(models.Model):
    class Meta:
        verbose_name = '掲示板スレッド'
        verbose_name_plural = '1.掲示板スレッド'
        db_table = 'threads'

    thread_no = models.AutoField(verbose_name='掲示板No', primary_key=True)
    thread_title = models.CharField(verbose_name='掲示板タイトル', max_length=100, null=False, blank=False)
    create_date = models.DateTimeField(verbose_name='作成日時', default=timezone.now())
    OPEN_LEVEL = (
        (0, '非公開(パスワードがないと閲覧・書き込み不可)'),
        (1, '閲覧のみ(パスワードがないと書き込み不可)'),
        (2, '閲覧・書き込みとも可能'),
    )
    open_level = models.SmallIntegerField(verbose_name='公開レベル', choices=OPEN_LEVEL, null=False, blank=False)
    password = models.CharField(verbose_name='利用パスワード', max_length=100, null=True, blank=True)

    def __str__(self):
        return '{}:{}'.format(self.thread_no, self.thread_title)

    def display_open_level(self):
        return '{}'.format([l[1] for l in self.OPEN_LEVEL if self.open_level == l[0]][0])

    def display_create_user(self):
        return self.threadmember_set.get(create=True).member.display_name()


class ThreadMember(models.Model):
    class Meta:
        verbose_name = '掲示板参加メンバー'
        verbose_name_plural = '参加メンバー'
        db_table = 'thread_member'
        unique_together = ("thread", "member")

    thread = models.ForeignKey(Threads, verbose_name='掲示板スレッド', on_delete=models.CASCADE)
    member = models.ForeignKey(UserAccount, verbose_name='参加メンバー', on_delete=models.PROTECT)
    create = models.BooleanField(verbose_name='掲示板作成者フラグ', default=False)

    def __str__(self):
        return '掲示板No.{}【{}】:{}さん'.format(self.thread.thread_no, self.thread.thread_title,
                                          self.member.display_name())


class ThreadWrite(models.Model):
    class Meta:
        verbose_name = '掲示板書き込み'
        verbose_name_plural = '2.掲示板書き込み'
        db_table = 'thread_write'
        unique_together = ('thread', 'number')
        get_latest_by = 'number'

    thread = models.ForeignKey(Threads, verbose_name='掲示板スレッド', on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name='書き込み番号')
    member = models.ForeignKey(ThreadMember, verbose_name='参加メンバー', on_delete=models.PROTECT)
    sentence = models.TextField(verbose_name='書き込み', null=False, blank=False, max_length=5000)
    write_datetime = models.DateTimeField(verbose_name='書き込み日時', null=False, blank=False, default=timezone.now())

    def next_number(self):
        return self.number + 1


class ThreadWriteAttachment(models.Model):
    class Meta:
        verbose_name = '書き込み添付ファイル'
        verbose_name_plural = '添付ファイル'
        db_table = 'thread_write_attachment'
        unique_together = ('thread_write', 'sequence')

    thread_write = models.ForeignKey(ThreadWrite, verbose_name='書き込み', on_delete=models.CASCADE)
    sequence = models.IntegerField(verbose_name='連番')
    attachment = models.FileField(verbose_name='添付ファイル',
                                  upload_to='attachments/')


class DirectMessage(models.Model):
    class Meta:
        verbose_name = 'メッセージ'
        verbose_name_plural = '3.ダイレクトメッセージ'
        db_table = 'direct_message'
        unique_together = ('thread', 'member', 'sequence')

    thread = models.ForeignKey(Threads, verbose_name='掲示板スレッド', on_delete=models.CASCADE)
    member = models.ForeignKey(ThreadMember, verbose_name='参加メンバー', on_delete=models.PROTECT)
    sequence = models.IntegerField(verbose_name='連番')
    message = models.TextField(verbose_name='メッセージ', null=False, blank=False, max_length=5000)


class DirectMessageAttachment(models.Model):
    class Meta:
        verbose_name = 'メッセージ添付ファイル'
        verbose_name_plural = '添付ファイル'
        db_table = 'direct_message_attachment'
        unique_together = ('message', 'sequence')

    message = models.ForeignKey(DirectMessage, verbose_name='メッセージ', on_delete=models.CASCADE)
    sequence = models.IntegerField(verbose_name='連番')
    attachment = models.FileField(verbose_name='添付ファイル',
                                  upload_to='attachment_messages/')



