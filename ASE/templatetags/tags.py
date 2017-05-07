from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.simple_tag
def active_page(request, view_name):
    """ Tag for active highlighting of navigation bar links """
    from django.core.urlresolvers import resolve, Resolver404
    path = resolve(request.path_info)
    if not request:
        return ""
    try:
        return "active" if path.url_name == view_name else ""
    except Resolver404:
        return ""

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """ Returns verbose_name for a field. """
    return instance._meta.get_field(field_name).verbose_name.title()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='is_checkboxes')
def is_checkboxes(form_field_obj):
    return form_field_obj.field.widget.__class__.__name__ == "CheckboxSelectMultiple"

@register.filter(name='has_group') 
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name) 
    except Group.DoesNotExist:
        return False
        
    return group in user.groups.all() 
