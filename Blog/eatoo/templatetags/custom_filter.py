from django.template import Library

register = Library()


@register.filter(name='sorted_tag')
def sorted_tag(value):
    return "%s年%s月"%(value.year,value.month)


@register.filter(name="plusone")
def plusone(value):
    return value+1


@register.filter(name="minusone")
def minusone(value):
    return value-1