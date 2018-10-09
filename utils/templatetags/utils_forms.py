

from django import template

register = template.Library()


@register.inclusion_tag('form_standar_field.html')
def standar_field(field, **kargs):

    return {
        "field": field,
        "column_size": kargs.get("column_size", 4),
        "field_extra_class": kargs.get("field_extra_class", ""),
        "shadow": kargs.get("shadow", True)
    }


@register.inclusion_tag('placeholder_based_field.html')
def placeholder_based_field(field, **kargs):

    return {
        "field": field,
        "column_size": kargs.get("column_size", 4),
        "field_extra_class": kargs.get("field_extra_class", ""),
        "shadow": kargs.get("shadow", True)
    }


@register.inclusion_tag('form_checkbox_field.html')
def checkbox_field(field, **kargs):

    return {
        "field": field,
        "column_size": kargs.get("column_size", 4),
        "field_extra_class": kargs.get("field_extra_class", "")
    }
