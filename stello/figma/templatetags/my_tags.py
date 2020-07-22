from django import template

register = template.Library()


@register.simple_tag
def background_image(file_url):
    if file_url:
        return 'background: url(' + file_url.url + ');background-repeat:\
            no-repeat;background-size: cover;'

    else:
        return ''


@register.simple_tag
def product_url(kind):
    if kind == 'text_input':
        return 'manager:product_detail'
    elif kind == 'image_select':
        return 'manager:product_photo_detail'


@register.simple_tag
def is_selected(val1, val2):
    if val1 == val2:
        return 'selected'
    else:
        return ''
