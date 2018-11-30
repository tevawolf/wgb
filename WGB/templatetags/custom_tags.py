from django import template

register = template.Library()


@register.filter
def find_create_user(member):
    if member.filter(create=True).exists():
        return member.get(create=True).member.display_name()
    else:
        return ''


@register.filter
def find_member_self(member, user):
    if user.is_authenticated and \
            member.filter(member_id=user).exists():
        return member.get(member_id=user).id

    return ''
