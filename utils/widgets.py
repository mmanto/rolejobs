# encoding=utf-8

from django.forms.utils import flatatt
from django.utils.html import format_html
from django.forms.widgets import Widget


class TextAngular(Widget):
    """TextAngular widget"""

    def render(self, name, value, attrs=None):
        if value is None:
            value = ""

        if attrs is None:
            attrs = {}

        attrs['class'] = "ta-field-complete"

        final_attrs = self.build_attrs(
            attrs,
            name=name,
            value=attrs.get('ng-model', value))

        return format_html(
            '<div text-angular{}>{}</div>',
            flatatt(final_attrs),
            value)


class FoundationRating(Widget):
    """Rating widget"""

    def render(self, name, value, attrs=None):
        if value is not None:
            value = int(value)
        else:
            value = 0

        final_attrs = self.build_attrs(
            attrs,
            name=name,
            value=attrs.get('ng-model', value))

        if "max" not in final_attrs:
            raise Exception("No max defined")

        return format_html('<rating{} />', flatatt(final_attrs))
