from __future__ import absolute_import, unicode_literals

import json

from aiohttp import web

# problems for ansi aiohttp dispatch of methods get put post
# error handle
# hooks for security
from ferdinand.server.views import TopicView, TopicDetailView
from aiohttp_swagger import setup_swagger


def setup_appilation(folder_deepth=3):
    """

    :type folder_deepth: int
    :rtype: web.Application
    """
    app = web.Application()

    # adds deepth of possible subscribe patterns
    base_url = ""
    for deepth in range(0, folder_deepth):
        base_url = "%s/{topic%s}" % (base_url, deepth)
        app.router.add_get(base_url, TopicView)
        app.router.add_get("%s/" % base_url, TopicView)
        app.router.add_get("%s/{detail:\d+}" % base_url, TopicDetailView)
        app.router.add_get("%s/{detail:\d+}/" % base_url, TopicDetailView)

    setup_swagger(app, swagger_url="/", api_version="0.0.1", ) # my index will be my swagger path ?
    return app

if __name__ == '__main__':
    # async call to start
    app = setup_appilation(4)
    web.run_app(app, port=1234, host="127.0.0.1")
