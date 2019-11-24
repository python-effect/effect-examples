from txeffect import deferred_performer

import treq


@deferred_performer
def perform_request_with_treq(dispatcher, http_request):
    """A performer for :obj:`HTTPRequest` that uses the ``treq`` library."""
    headers = (
        http_request.headers.copy()
        if http_request.headers is not None
        else {})
    if 'user-agent' not in headers:
        headers['user-agent'] = ['Effect example']
    d = treq.request(
        http_request.method.lower(),
        http_request.url,
        headers=headers,
        data=http_request.data).addCallback(treq.content)
    return d
