from django.contrib import admin
from . import models


admin.site.register(models.UserAccount)


class ThreadMemberInline(admin.TabularInline):
    model = models.ThreadMember
    extra = 0


class ThreadsAdmin(admin.ModelAdmin):
    inlines = [ThreadMemberInline]


admin.site.register(models.Threads, ThreadsAdmin)


class ThreadWriteAttachmentInline(admin.TabularInline):
    model = models.ThreadWriteAttachment
    extra = 0


class ThreadWriteAdmin(admin.ModelAdmin):
    inlines = [ThreadWriteAttachmentInline]
    list_filter = ['thread']


admin.site.register(models.ThreadWrite, ThreadWriteAdmin)


class DirectMessageAttachmentInline(admin.TabularInline):
    model = models.DirectMessageAttachment
    extra = 0


class DirectMessageAdmin(admin.ModelAdmin):
    inlines = [DirectMessageAttachmentInline]
    list_filter = ['from_member', 'to_member']


admin.site.register(models.DirectMessage, DirectMessageAdmin)
