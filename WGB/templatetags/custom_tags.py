from django import template

register = template.Library()


@register.filter
def find_create_user(member):
    create_user = member.get(create=True)
    if create_user:
        return create_user.member.display_name()
    else:
        return ''


@register.filter
def find_member_self(member, user):
    member_self = member.get(member=user)
    if member_self:
        return member_self.id
    else:
        return ''
