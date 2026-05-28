"""URL rewriting for affiliate programs.

Each rewriter takes the original URL + the affiliate ID from settings and
returns the URL the user should actually click. If no ID is configured
for that program, the URL passes through unchanged. This keeps the site
working with zero config and lights up monetization the moment IDs are
filled in.

To add a new program: write a rewriter function, append it to REWRITERS,
add the env var to settings.AFFILIATE_IDS.
"""

from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse

from django.conf import settings


def _set_query(url: str, **params: str) -> str:
    parts = urlparse(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update({k: v for k, v in params.items() if v})
    return urlunparse(parts._replace(query=urlencode(query)))


def _amazon(url: str, ids: dict) -> str:
    """Tag amazon.com / amazon.in / amzn.to product URLs only.

    AWS docs (aws.amazon.com), developer (developer.amazon.com), and
    other non-shop subdomains don't earn affiliate commissions, so we
    skip them to keep clean URLs.
    """
    tag = ids.get('amazon')
    if not tag:
        return url
    host = urlparse(url).netloc.lower()
    if 'amzn.to' in host:
        return _set_query(url, tag=tag)
    # Shopping subdomains: bare "amazon.tld" or "www.amazon.tld" only.
    if host.startswith('amazon.') or host.startswith('www.amazon.'):
        return _set_query(url, tag=tag)
    return url


def _impact(url: str, ids: dict, mid: str) -> str:
    """Wrap a destination URL in an Impact.com deep link.

    Impact (formerly LinkShare) is the affiliate network behind Udemy,
    Coursera, Skillshare, and many others. You get one Impact publisher
    ID, then each merchant has a distinct `mid`. Set AFFILIATE_IMPACT_ID
    plus the per-merchant ID env vars.
    """
    impact_id = ids.get('impact_id')
    if not impact_id or not mid:
        return url
    base = 'https://click.linksynergy.com/deeplink'
    params = urlencode({'id': impact_id, 'mid': mid, 'murl': url})
    return f'{base}?{params}'


def _udemy(url: str, ids: dict) -> str:
    if 'udemy.com' not in urlparse(url).netloc.lower():
        return url
    return _impact(url, ids, mid=ids.get('udemy', ''))


def _coursera(url: str, ids: dict) -> str:
    if 'coursera.org' not in urlparse(url).netloc.lower():
        return url
    return _impact(url, ids, mid=ids.get('coursera', ''))


def _skillshare(url: str, ids: dict) -> str:
    if 'skillshare.com' not in urlparse(url).netloc.lower():
        return url
    return _impact(url, ids, mid=ids.get('skillshare', ''))


def _educative(url: str, ids: dict) -> str:
    aff = ids.get('educative')
    if not aff or 'educative.io' not in urlparse(url).netloc.lower():
        return url
    return _set_query(url, aff=aff)


REWRITERS = [_amazon, _udemy, _coursera, _skillshare, _educative]


def affiliate_url(url: str) -> str:
    if not url:
        return url
    ids = getattr(settings, 'AFFILIATE_IDS', {})
    for rewrite in REWRITERS:
        url = rewrite(url, ids)
    return url
