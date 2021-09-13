from django import template

register = template.Library()


@register.filter(name='split')
def split(value, key):
    """
      Returns the value turned into a list.
    """
    return value.split(key)


@register.filter
def count_filter_by_status(thing, value):
    return thing.filter(status=value).count()
    # return things.filter(project_id=client_project_id).supportrequest_set.all


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    if pattern_or_urlname == context['request'].resolver_match.url_name:
        return 'active'
    return ''
