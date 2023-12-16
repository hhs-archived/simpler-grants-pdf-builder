from django import template
from django.utils.safestring import mark_safe

from bs4 import BeautifulSoup

from ..nofo import add_caption_to_table

register = template.Library()


@register.filter()
def add_captions_to_tables(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    for table in soup.find_all("table"):
        add_caption_to_table(table)

    return mark_safe(soup.prettify())
