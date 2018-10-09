# -*- coding: utf-8 -*-

from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe, SafeText
from django.utils.encoding import force_text

from djng.forms.angular_base import TupleErrorList


class NgErrorList(TupleErrorList):

    def as_ul(self):
        if not self:
            return SafeText()
        first = self[0]
        if isinstance(first, tuple):
            error_lists = {'$pristine': [], '$dirty': []}
            for e in self:
                li_format = e[
                    5] == '$message' and self.li_format_bind or self.li_format
                err_tuple = (e[0], e[3], e[4], force_text(e[5]))
                error_lists[e[2]].append(format_html(li_format, *err_tuple))

            err_tuple = (
                "apiErrors." + first[0],
                "msg",
                first[4], "msg")

            error_lists["$dirty"].append(
                format_html(self.li_format_bind, *err_tuple)
            )

            # renders and combine both of these lists
            return mark_safe(
                ''.join(
                    [
                        format_html(
                            self.ul_format,
                            first[0],
                            first[1],
                            prop,
                            mark_safe(
                                ''.join(list_items))) for prop,
                        list_items in error_lists.items()]))
        return format_html('<ul class="errorlist">{0}</ul>',
                           format_html_join(
                               '',
                               '<li>{0}</li>',
                               ((force_text(e),) for e in self))
                           )
