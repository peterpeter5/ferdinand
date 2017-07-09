from __future__ import absolute_import, unicode_literals
import json

# problems for ansi aiohttp dispatch of methods get put post
# error handle
# hooks for security

from aiohttp import web


async def index(request):
    return web.Response(text=json.dumps(dict(key="map")))

async def get_topic_tuple(request):
    """
    the url dispatch should match multiple urls need to look for rekursion
    :param request:
    :return: list
    """
    matching_info = dict(request.match_info)
    return list(matching_info.values())

async def create_response(content, status):
    if isinstance(content, dict):
        content = json.dumps(content)
    else:
        content = str(content)
    return web.Response(text=content, status=status)


class TopicView(web.View):

    async def get(self):
        """

        :param request:
        :type topic_path: tuple
        :return:
        """
        topic_path = await get_topic_tuple(self.request)
        return await create_response({'topic': topic_path}, 200)

    async def post(self):
        """

        :param request:
        :type topic_path: tuple
        :return:
        """
        topic_path = await get_topic_tuple(self.request)

        return await create_response({'topic post': topic_path}, 200)


class TopicDetailView(web.View):

    async def get(self):
        topic_path = await get_topic_tuple(self.request)
        detail_id = topic_path.pop()

        return await create_response({'topic': topic_path, 'detail_id': detail_id}, 200)

    async def put(self):
        topic_path = await get_topic_tuple(self.request)
        detail_id = topic_path.pop()

        return await create_response({'topic': topic_path, 'detail_id': detail_id}, 200)

app = web.Application()
app.router.add_get("/", index)
app.router.add_get("/{topic}", TopicView)
app.router.add_get("/{topic}/", TopicView)
app.router.add_get("/{topic}/{detail}", TopicDetailView)
app.router.add_get("/{topic}/{detail}/", TopicDetailView)

if __name__ == '__main__':
    # async call to start
    web.run_app(app, port=1234, host="127.0.0.1")