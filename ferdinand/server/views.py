import json

from aiohttp import web
from aiohttp_swagger import swagger_path

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