"""Template filter that rewrites resource URLs through affiliate networks."""

from django import template

from roadmap.affiliates import affiliate_url

register = template.Library()


@register.filter(name='affiliate')
def affiliate(url):
    return affiliate_url(url or '')
