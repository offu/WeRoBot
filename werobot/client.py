# -*- coding: utf-8 -*-

import time
import requests

from requests.compat import json as _json
from werobot.utils import to_text


class ClientException(Exception):
    pass


def check_error(json):
    """
    检测微信公众平台返回值中是否包含错误的返回码。
    如果返回码提示有错误，抛出一个 :class:`ClientException` 异常。否则返回 True 。
    """
    if "errcode" in json and json["errcode"] != 0:
        raise ClientException("{}: {}".format(json["errcode"], json["errmsg"]))
    return json


class Client(object):
    """
    微信 API 操作类
    通过这个类可以方便的通过微信 API 进行一系列操作，比如主动发送消息、创建自定义菜单等
    """

    def __init__(self, config):
        self.config = config
        self.appid = self.config.get("APP_ID", None)
        self.appsecret = self.config.get("APP_SECRET", None)
        self._token = None
        self.token_expires_at = None

    def request(self, method, url, **kwargs):
        if "params" not in kwargs:
            kwargs["params"] = {"access_token": self.token}
        if isinstance(kwargs.get("data", ""), dict):
            body = _json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode('utf8')
            kwargs["data"] = body

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
        json = r.json()
        if check_error(json):
            return json

    def get(self, url, **kwargs):
        return self.request(
            method="get",
            url=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self.request(
            method="post",
            url=url,
            **kwargs
        )

    def grant_token(self):
        """
        获取 Access Token 。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档

        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": self.appid,
                "secret": self.appsecret
            }
        )

    def get_access_token(self):
        """
        判断现有的token是否过期。
        用户需要多进程或者多机部署可以手动重写这个函数
        来自定义token的存储，刷新策略。

        :return: 返回token
        """
        if self._token:
            now = time.time()
            if self.token_expires_at - now > 60:
                return self._token
        json = self.grant_token()
        self._token = json["access_token"]
        self.token_expires_at = int(time.time()) + json["expires_in"]
        return self._token

    @property
    def token(self):
        return self.get_access_token()

    def create_menu(self, menu_data):
        """
        创建自定义菜单。::

            client = Client("id", "secret")
            client.create_menu({
                "button":[
                    {
                        "type":"click",
                        "name":"今日歌曲",
                        "key":"V1001_TODAY_MUSIC"
                    },
                    {
                        "type":"click",
                        "name":"歌手简介",
                        "key":"V1001_TODAY_SINGER"
                    },
                    {
                        "name":"菜单",
                        "sub_button":[
                            {
                                "type":"view",
                                "name":"搜索",
                                "url":"http://www.soso.com/"
                            },
                            {
                                "type":"view",
                                "name":"视频",
                                "url":"http://v.qq.com/"
                            },
                            {
                                "type":"click",
                                "name":"赞一下我们",
                                "key":"V1001_GOOD"
                            }
                        ]
                    }
                ]})

        :param menu_data: Python 字典
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/menu/create",
            data=menu_data
        )

    def get_menu(self):
        """
        查询自定义菜单。

        :return: 返回的 JSON 数据包
        """
        return self.get("https://api.weixin.qq.com/cgi-bin/menu/get")

    def delete_menu(self):
        """
        删除自定义菜单。

        :return: 返回的 JSON 数据包
        """
        return self.get("https://api.weixin.qq.com/cgi-bin/menu/delete")

    def create_custom_menu(self, menu_data, matchrule):
        """
        创建个性化菜单。::

            button = [
                {
                    "type":"click",
                    "name":"今日歌曲",
                    "key":"V1001_TODAY_MUSIC"
                },
                {
                    "name":"菜单",
                    "sub_button":[
                    {
                        "type":"view",
                        "name":"搜索",
                        "url":"http://www.soso.com/"
                    },
                    {
                        "type":"view",
                        "name":"视频",
                        "url":"http://v.qq.com/"
                    },
                    {
                        "type":"click",
                        "name":"赞一下我们",
                        "key":"V1001_GOOD"
                    }]
             }]
             matchrule = {
                "group_id":"2",
                "sex":"1",
                "country":"中国",
                "province":"广东",
                "city":"广州",
                "client_platform_type":"2",
                "language":"zh_CN"
            }
            client.create_custom_menu(button, matchrule)

        :param menu_data: 如上所示的 Python 字典
        :param matchrule: 如上所示的匹配规则
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/menu/addconditional",
            data={
                "button": menu_data,
                "matchrule": matchrule
            }
        )

    def delete_custom_menu(self, menu_id):
        """
        删除个性化菜单。

        :param menu_id: 菜单的 ID
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/menu/delconditional",
            data={
                "menuid": menu_id
            }
        )

    def match_custom_menu(self, user_id):
        """
        测试个性化菜单匹配结果。

        :param user_id: 要测试匹配的用户 ID
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/menu/trymatch",
            data={
                "user_id": user_id
            }
        )

    def get_custom_menu_config(self):
        """
        获取自定义菜单配置接口。

        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info"
        )

    def upload_media(self, media_type, media_file):
        """
        上传临时多媒体文件。

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media_file: 要上传的文件，一个 File-object
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/media/upload",
            params={
                "access_token": self.token,
                "type": media_type
            },
            files={
                "media": media_file
            }
        )

    def download_media(self, media_id):
        """
        下载临时多媒体文件。

        :param media_id: 媒体文件 ID
        :return: requests 的 Response 实例
        """
        return requests.get(
            url="https://api.weixin.qq.com/cgi-bin/media/get",
            params={
                "access_token": self.token,
                "media_id": media_id
            }
        )

    def add_news(self, articles):
        """
        新增永久图文素材。::

            articles = [{
               "title": TITLE,
               "thumb_media_id": THUMB_MEDIA_ID,
               "author": AUTHOR,
               "digest": DIGEST,
               "show_cover_pic": SHOW_COVER_PIC(0 / 1),
               "content": CONTENT,
               "content_source_url": CONTENT_SOURCE_URL
            }
            # 若新增的是多图文素材，则此处应有几段articles结构，最多8段
            ]
            client.add_news(articles)

        :param articles: 如示例中的数组
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/material/add_news",
            data={
                "articles": articles
            }
        )

    def upload_news_picture(self, file):
        """
        上传图文消息内的图片。

        :param file: 要上传的文件，一个 File-object
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/media/uploadimg",
            params={
                "access_token": self.token
            },
            files={
                "media": file
            }
        )

    def upload_permanent_media(self, media_type, media_file):
        """
        上传其他类型永久素材。

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）和缩略图（thumb）
        :param media_file: 要上传的文件，一个 File-object
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/material/add_material",
            params={
                "access_token": self.token,
                "type": media_type
            },
            files={
                "media": media_file
            }
        )

    def upload_permanent_video(self, title, introduction, video):
        """
        上传永久视频。

        :param title: 视频素材的标题
        :param introduction: 视频素材的描述
        :param video: 要上传的视频，一个 File-object
        :return: requests 的 Response 实例
        """
        return requests.post(
            url="https://api.weixin.qq.com/cgi-bin/material/add_material",
            params={
                "access_token": self.token,
                "type": "video"
            },
            data={
                "description": _json.dumps({
                    "title": title,
                    "introduction": introduction
                }, ensure_ascii=False).encode("utf-8")
            },
            files={
                "media": video
            }
        )

    def download_permanent_media(self, media_id):
        """
        获取永久素材。

        :param media_id: 媒体文件 ID
        :return: requests 的 Response 实例
        """
        return requests.post(
            url="https://api.weixin.qq.com/cgi-bin/material/get_material",
            params={
                "access_token": self.token
            },
            data=_json.dumps({
                "media_id": media_id
            }, ensure_ascii=False).encode("utf-8")
        )

    def delete_permanent_media(self, media_id):
        """
        删除永久素材。

        :param media_id: 媒体文件 ID
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/material/del_material",
            data={
                "media_id": media_id
            }
        )

    def update_news(self, update_data):
        """
        修改永久图文素材。::

            update_data = {
                "media_id":MEDIA_ID,
                "index":INDEX,
                "articles": {
                    "title": TITLE,
                    "thumb_media_id": THUMB_MEDIA_ID,
                    "author": AUTHOR,
                    "digest": DIGEST,
                    "show_cover_pic": SHOW_COVER_PIC(0 / 1),
                    "content": CONTENT,
                    "content_source_url": CONTENT_SOURCE_URL
                }
            }
            client.update_news(update_data)

        :param update_data: 更新的数据，要包含 media_id（图文素材的 ID），index（要更新的文章在图文消息中的位置），articles（新的图文素材数据）
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/material/update_news",
            data=update_data
        )

    def create_group(self, name):
        """
        创建分组。

        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包

        """
        name = to_text(name)
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/groups/create",
            data={"group": {"name": name}}
        )

    def get_groups(self):
        """
        查询所有分组。

        :return: 返回的 JSON 数据包
        """
        return self.get("https://api.weixin.qq.com/cgi-bin/groups/get")

    def get_group_by_id(self, openid):
        """
        查询用户所在分组。

        :param openid: 用户的OpenID
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/groups/getid",
            data={"openid": openid}
        )

    def update_group(self, group_id, name):
        """
        修改分组名。

        :param group_id: 分组 ID，由微信分配
        :param name: 分组名字（30个字符以内）
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/groups/update",
            data={"group": {
                "id": int(group_id),
                "name": to_text(name)
            }}
        )

    def move_user(self, user_id, group_id):
        """
        移动用户分组。

        :param user_id: 用户 ID，即收到的 `Message` 的 source
        :param group_id: 分组 ID
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/groups/members/update",
            data={
                "openid": user_id,
                "to_groupid": group_id
            }
        )

    def move_users(self, user_id_list, group_id):
        """
        批量移动用户分组。

        :param user_id_list: 用户 ID 的列表（长度不能超过50）
        :param group_id: 分组 ID
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/groups/members/batchupdate",
            data={
                "openid_list": user_id_list,
                "to_groupid": group_id
            }
        )

    def delete_group(self, group_id):
        """
        删除分组。

        :param group_id: 要删除的分组的 ID
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/groups/delete",
            data={
                "group": {
                    "id": group_id
                }
            }
        )

    def remark_user(self, user_id, remark):
        """
        设置备注名。

        :param user_id: 设置备注名的用户 ID
        :param remark: 新的备注名，长度必须小于30字符
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/user/info/updateremark",
            data={
                "openid": user_id,
                "remark": remark
            }
        )

    def get_user_info(self, user_id, lang="zh_CN"):
        """
        获取用户基本信息。

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/user/info",
            params={
                "access_token": self.token,
                "openid": user_id,
                "lang": lang
            }
        )

    def get_users_info(self, user_id_list, lang="zh_CN"):
        """
        批量获取用户基本信息。

        :param user_id_list: 用户 ID 的列表
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/user/info/batchget",
            data={
                "user_list": [
                    {"openid": user_id,
                     "lang": lang} for user_id in user_id_list
                    ]
            }
        )

    def get_followers(self, first_user_id=None):
        """
        获取关注者列表
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=获取关注者列表

        :param first_user_id: 可选。第一个拉取的OPENID，不填默认从头开始拉取
        :return: 返回的 JSON 数据包
        """
        params = {
            "access_token": self.token
        }
        if first_user_id:
            params["next_openid"] = first_user_id
        return self.get(
            "https://api.weixin.qq.com/cgi-bin/user/get",
            params=params
        )

    def send_text_message(self, user_id, content):
        """
        发送文本消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param content: 消息正文
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "text",
                "text": {"content": content}
            }
        )

    def send_image_message(self, user_id, media_id):
        """
        发送图片消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 图片的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "image",
                "image": {
                    "media_id": media_id
                }
            }
        )

    def send_voice_message(self, user_id, media_id):
        """
        发送语音消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 发送的语音的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "voice",
                "voice": {
                    "media_id": media_id
                }
            }
        )

    def send_video_message(self, user_id, media_id,
                           title=None, description=None):
        """
        发送视频消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 发送的视频的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :return: 返回的 JSON 数据包
        """
        video_data = {
            "media_id": media_id,
        }
        if title:
            video_data["title"] = title
        if description:
            video_data["description"] = description

        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "video",
                "video": video_data
            }
        )

    def send_music_message(self, user_id, url, hq_url, thumb_media_id,
                           title=None, description=None):
        """
        发送音乐消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param url: 音乐链接
        :param hq_url: 高品质音乐链接，wifi环境优先使用该链接播放音乐
        :param thumb_media_id: 缩略图的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 音乐标题
        :param description: 音乐描述
        :return: 返回的 JSON 数据包
        """
        music_data = {
            "musicurl": url,
            "hqmusicurl": hq_url,
            "thumb_media_id": thumb_media_id
        }
        if title:
            music_data["title"] = title
        if description:
            music_data["description"] = description

        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "music",
                "music": music_data
            }
        )

    def send_article_message(self, user_id, articles):
        """
        发送图文消息
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=发送客服消息

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param articles: 一个包含至多10个 :class:`Article` 实例的数组
        :return: 返回的 JSON 数据包
        """
        articles_data = []
        for article in articles:
            articles_data.append({
                "title": article.title,
                "description": article.description,
                "url": article.url,
                "picurl": article.img
            })
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "news",
                "news": {
                    "articles": articles_data
                }
            }
        )

    def create_qrcode(self, **data):
        """
        创建二维码
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=生成带参数的二维码

        :param data: 你要发送的参数 dict
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/qrcode/create",
            data=data
        )

    def show_qrcode(self, ticket):
        """
        通过ticket换取二维码
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=生成带参数的二维码

        :param ticket: 二维码 ticket 。可以通过 :func:`create_qrcode` 获取到
        :return: 返回的 Request 对象
        """
        return requests.get(
            url="https://mp.weixin.qq.com/cgi-bin/showqrcode",
            params={
                "ticket": ticket
            }
        )

    def send_template_message(self, user_id, template_id, data, url=''):
        """
        发送模板消息
        详情请参考 http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param template_id: 模板 ID。
        :param data: 用于渲染模板的数据。
        :param url: 模板消息的可选链接。
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/template/send",
            data={
                "touser": user_id,
                "template_id": template_id,
                "url": url,
                "data": data
            }
        )
