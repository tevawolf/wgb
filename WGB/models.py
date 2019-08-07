from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import FileExtensionValidator

import os


def get_upload_to(instance, filename):
    return os.path.join(instance.category, filename)


class UserAccount(AbstractUser):
    class Meta:
        verbose_name = '利用者アカウント'
        verbose_name_plural = '0.利用者アカウント'
        db_table = 'wgb_user_account'

    nickname = models.CharField(verbose_name='ニックネーム', max_length=100, null=False, blank=True)
    icon = models.ImageField(verbose_name='アイコン画像パス', upload_to=get_upload_to, null=True, blank=True,
                             validators=[FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png', ])], )
    category = 'icon'

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
        (0, 'メンバーのみ'),
        (1, '誰でも'),
    )
    open_level = models.SmallIntegerField(verbose_name='閲覧レベル', choices=OPEN_LEVEL, null=False, blank=False)
    password = models.CharField(verbose_name='利用パスワード', max_length=100, null=False, blank=False)

    def __str__(self):
        return '{}:{}'.format(self.thread_no, self.thread_title)

    def display_open_level(self):
        return '{}'.format([l[1] for l in self.OPEN_LEVEL if self.open_level == l[0]][0])

    def display_create_user(self):
        return self.threadmember_set.get(create=True).member.display_name()

    def display_create_user_icon(self):
        return self.threadmember_set.get(create=True).member.icon.url

    def display_last_update_user(self):
        return self.threadwrite_set.latest('write_datetime').member.member.display_name()

    def display_last_update_user_icon(self):
        return self.threadwrite_set.latest('write_datetime').member.member.icon.url

    def display_last_update_datetime(self):
        return self.threadwrite_set.latest('write_datetime').write_datetime


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
    # write_datetime = models.DateTimeField(verbose_name='書き込み日時', null=False, blank=False, default=timezone.now())
    write_datetime = models.DateTimeField(verbose_name='書き込み日時', null=False, blank=False, auto_now=True)

    def next_number(self):
        return self.number + 1

    def __str__(self):
        return '{}.{}'.format(self.thread, self.number)


class ThreadWriteAttachment(models.Model):
    class Meta:
        verbose_name = '書き込み添付ファイル'
        verbose_name_plural = '添付ファイル'
        db_table = 'thread_write_attachment'
        unique_together = ('thread_write', 'sequence')

    thread_write = models.ForeignKey(ThreadWrite, verbose_name='書き込み', on_delete=models.CASCADE)
    sequence = models.IntegerField(verbose_name='連番')
    attachment = models.ImageField(verbose_name='添付画像ファイル', upload_to=get_upload_to, null=True, blank=True)
    category = 'attachment_write'


class DirectMessage(models.Model):
    class Meta:
        verbose_name = 'メッセージ'
        verbose_name_plural = '3.ダイレクトメッセージ'
        db_table = 'direct_message'
        unique_together = ('from_member', 'to_member', 'sequence')
        get_latest_by = ('from_member', 'to_member', 'sequence')

    from_member = models.ForeignKey(ThreadMember, related_name='from_member', verbose_name='送信者',
                                    on_delete=models.PROTECT, null=False, blank=False)
    to_member = models.ForeignKey(ThreadMember, related_name='to_member',  verbose_name='送信相手',
                                  on_delete=models.PROTECT, null=False, blank=False)
    sequence = models.IntegerField(verbose_name='連番')
    title = models.CharField(verbose_name='タイトル', null=False, blank=False, max_length=100)
    message = models.TextField(verbose_name='メッセージ', null=False, blank=False, max_length=5000)
    send_datetime = models.DateTimeField(verbose_name='送信日時', null=False, blank=False, default=timezone.now())

    def next_sequence(self):
        return self.sequence + 1


class DirectMessageAttachment(models.Model):
    class Meta:
        verbose_name = 'メッセージ添付ファイル'
        verbose_name_plural = '添付ファイル'
        db_table = 'direct_message_attachment'
        unique_together = ('message', 'sequence')

    message = models.ForeignKey(DirectMessage, verbose_name='メッセージ', on_delete=models.CASCADE)
    sequence = models.IntegerField(verbose_name='連番')
    attachment = models.ImageField(verbose_name='添付ファイル', upload_to=get_upload_to, null=True, blank=True)
    category = 'attachment_messages'
