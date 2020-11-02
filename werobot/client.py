# -*- coding: utf-8 -*-

import time
import requests
import urllib.parse

from requests.compat import json as _json
from werobot.utils import to_text
from werobot.replies import Article


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


def _build_send_data(msg_type, content):
    """
    编译群发参数
    :param msg_type: 群发类型，图文消息为 mpnews，文本消息为 text，语音为 voice，音乐为 music，图片为 image，视频为 video，卡券为 wxcard。
    :param content: 群发内容。
    :return: 群发参数。
    """
    send_data = {}
    send_data['msgtype'] = msg_type
    if msg_type in ['mpnews', 'voice', 'music', 'image']:
        send_data[msg_type] = {'media_id': content}
    elif msg_type == 'video':
        send_data['mpvideo'] = {'media_id': content}
        send_data['msgtype'] = 'mpvideo'
    elif msg_type == 'text':
        send_data['text'] = {'content': content}
    elif msg_type == 'wxcard':
        send_data['wxcard'] = {'card_id': content}
    else:
        send_data['text'] = {'content': content}
        send_data['msgtype'] = 'text'
    return send_data


class Client(object):
    """
    微信 API 操作类
    通过这个类可以方便的通过微信 API 进行一系列操作，比如主动发送消息、创建自定义菜单等
    """
    def __init__(self, config):
        self.config = config
        self._token = None
        self.token_expires_at = None

    @property
    def appid(self):
        return self.config.get("APP_ID", None)

    @property
    def appsecret(self):
        return self.config.get("APP_SECRET", None)

    @staticmethod
    def _url_encode_files(file):
        if hasattr(file, "name"):
            file = (urllib.parse.quote(file.name), file)
        return file

    def request(self, method, url, **kwargs):
        if "params" not in kwargs:
            kwargs["params"] = {"access_token": self.token}
        if isinstance(kwargs.get("data", ""), dict):
            body = _json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode('utf8')
            kwargs["data"] = body

        r = requests.request(method=method, url=url, **kwargs)
        r.raise_for_status()
        r.encoding = "utf-8"
        json = r.json()
        if check_error(json):
            return json

    def get(self, url, **kwargs):
        return self.request(method="get", url=url, **kwargs)

    def post(self, url, **kwargs):
        if "files" in kwargs:
            # Although there is only one key "media" possible in "files" now,
            # we decide to check every key to support possible keys in the future
            # Fix chinese file name error #292
            kwargs["files"] = dict(
                zip(
                    kwargs["files"],
                    map(self._url_encode_files, kwargs["files"].values())
                )
            )
        return self.request(method="post", url=url, **kwargs)

    def grant_token(self):
        """
        获取 Access Token。

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

    def get_ip_list(self):
        """
        获取微信服务器IP地址。

        :return: 返回的 JSON 数据包
        """
        return self.get(url="https://api.weixin.qq.com/cgi-bin/getcallbackip")

    def create_menu(self, menu_data):
        """
        创建自定义菜单::

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
        创建个性化菜单::

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
            data={"menuid": menu_id}
        )

    def match_custom_menu(self, user_id):
        """
        测试个性化菜单匹配结果。

        :param user_id: 要测试匹配的用户 ID
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/menu/trymatch",
            data={"user_id": user_id}
        )

    def get_custom_menu_config(self):
        """
        获取自定义菜单配置接口。

        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info"
        )

    def add_custom_service_account(self, account, nickname, password):
        """
        添加客服帐号。

        :param account: 客服账号的用户名
        :param nickname: 客服账号的昵称
        :param password: 客服账号的密码
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/customservice/kfaccount/add",
            data={
                "kf_account": account,
                "nickname": nickname,
                "password": password
            }
        )

    def update_custom_service_account(self, account, nickname, password):
        """
        修改客服帐号。

        :param account: 客服账号的用户名
        :param nickname: 客服账号的昵称
        :param password: 客服账号的密码
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/customservice/kfaccount/update",
            data={
                "kf_account": account,
                "nickname": nickname,
                "password": password
            }
        )

    def delete_custom_service_account(self, account, nickname, password):
        """
        删除客服帐号。

        :param account: 客服账号的用户名
        :param nickname: 客服账号的昵称
        :param password: 客服账号的密码
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/customservice/kfaccount/del",
            data={
                "kf_account": account,
                "nickname": nickname,
                "password": password
            }
        )

    def upload_custom_service_account_avatar(self, account, avatar):
        """
        设置客服帐号的头像。

        :param account: 客服账号的用户名
        :param avatar: 头像文件，必须是 jpg 格式
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url=
            "http://api.weixin.qq.com/customservice/kfaccount/uploadheadimg",
            params={
                "access_token": self.token,
                "kf_account": account
            },
            files={"media": avatar}
        )

    def get_custom_service_account_list(self):
        """
        获取所有客服账号。

        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/customservice/getkflist"
        )

    def get_online_custom_service_account_list(self):
        """
        获取状态为"在线"的客服账号列表。

        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/customservice/getonlinekflist"
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
            files={"media": media_file}
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
        新增永久图文素材::

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
            data={"articles": articles}
        )

    def upload_news_picture(self, file):
        """
        上传图文消息内的图片。

        :param file: 要上传的文件，一个 File-object
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/media/uploadimg",
            params={"access_token": self.token},
            files={"media": file}
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
            files={"media": media_file}
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
                "description": _json.dumps(
                    {
                        "title": title,
                        "introduction": introduction
                    },
                    ensure_ascii=False
                ).encode("utf-8")
            },
            files={"media": video}
        )

    def download_permanent_media(self, media_id):
        """
        获取永久素材。

        :param media_id: 媒体文件 ID
        :return: requests 的 Response 实例
        """
        return requests.post(
            url="https://api.weixin.qq.com/cgi-bin/material/get_material",
            params={"access_token": self.token},
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
            data={"media_id": media_id}
        )

    def update_news(self, update_data):
        """
        修改永久图文素材::

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

    def get_media_count(self):
        """
        获取素材总数。

        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/material/get_materialcount"
        )

    def get_media_list(self, media_type, offset, count):
        """
        获取素材列表。

        :param media_type: 素材的类型，图片（image）、视频（video）、语音 （voice）、图文（news）
        :param offset: 从全部素材的该偏移位置开始返回，0表示从第一个素材返回
        :param count: 返回素材的数量，取值在1到20之间
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/material/batchget_material",
            data={
                "type": media_type,
                "offset": offset,
                "count": count
            }
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
            data={"group": {
                "name": name
            }}
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
            data={"group": {
                "id": group_id
            }}
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
                    {
                        "openid": user_id,
                        "lang": lang
                    } for user_id in user_id_list
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
        params = {"access_token": self.token}
        if first_user_id:
            params["next_openid"] = first_user_id
        return self.get(
            "https://api.weixin.qq.com/cgi-bin/user/get", params=params
        )

    def send_text_message(self, user_id, content, kf_account=None):
        """
        发送文本消息。

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param content: 消息正文
        :param kf_account: 发送消息的客服账户，默认值为 None，None 为不指定
        :return: 返回的 JSON 数据包
        """
        data = {
            "touser": user_id,
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        if kf_account is not None:
            data['customservice'] = {'kf_account': kf_account}
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data=data
        )

    def send_image_message(self, user_id, media_id, kf_account=None):
        """
        发送图片消息。

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 图片的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param kf_account: 发送消息的客服账户，默认值为 None，None 为不指定
        :return: 返回的 JSON 数据包
        """
        data = {
            "touser": user_id,
            "msgtype": "image",
            "image": {
                "media_id": media_id
            }
        }
        if kf_account is not None:
            data['customservice'] = {'kf_account': kf_account}
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data=data
        )

    def send_voice_message(self, user_id, media_id, kf_account=None):
        """
        发送语音消息。

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 发送的语音的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param kf_account: 发送消息的客服账户，默认值为 None，None 为不指定
        :return: 返回的 JSON 数据包
        """
        data = {
            "touser": user_id,
            "msgtype": "voice",
            "voice": {
                "media_id": media_id
            }
        }
        if kf_account is not None:
            data['customservice'] = {'kf_account': kf_account}
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data=data
        )

    def send_video_message(
        self,
        user_id,
        media_id,
        title=None,
        description=None,
        kf_account=None
    ):
        """
        发送视频消息。

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 发送的视频的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        :param kf_account: 发送消息的客服账户，默认值为 None，None 为不指定
        :return: 返回的 JSON 数据包
        """
        video_data = {
            "media_id": media_id,
        }
        if title:
            video_data["title"] = title
        if description:
            video_data["description"] = description
        data = {"touser": user_id, "msgtype": "video", "video": video_data}
        if kf_account is not None:
            data['customservice'] = {'kf_account': kf_account}
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data=data
        )

    def send_music_message(
        self,
        user_id,
        url,
        hq_url,
        thumb_media_id,
        title=None,
        description=None,
        kf_account=None
    ):
        """
        发送音乐消息。
        注意如果你遇到了缩略图不能正常显示的问题， 不要慌张； 目前来看是微信服务器端的问题。
        对此我们也无能为力 ( `#197 <https://github.com/whtsky/WeRoBot/issues/197>`_ )

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param url: 音乐链接
        :param hq_url: 高品质音乐链接，wifi环境优先使用该链接播放音乐
        :param thumb_media_id: 缩略图的媒体ID。 可以通过 :func:`upload_media` 上传。
        :param title: 音乐标题
        :param description: 音乐描述
        :param kf_account: 发送消息的客服账户，默认值为 None，None 为不指定
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
        data = {"touser": user_id, "msgtype": "music", "music": music_data}
        if kf_account is not None:
            data['customservice'] = {'kf_account': kf_account}

        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data=data
        )

    def send_article_message(self, user_id, articles, kf_account=None):
        """
        发送图文消息::

            articles = [
                {
                    "title":"Happy Day",
                    "description":"Is Really A Happy Day",
                    "url":"URL",
                    "picurl":"PIC_URL"
                },
                {
                    "title":"Happy Day",
                    "description":"Is Really A Happy Day",
                    "url":"URL",
                    "picurl":"PIC_URL"
                }
            ]
            client.send_acticle_message("user_id", acticles)

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param articles: 一个包含至多8个 article 字典或 Article 对象的数组
        :param kf_account: 发送消息的客服账户，默认值为 None，None 为不指定
        :return: 返回的 JSON 数据包
        """
        if isinstance(articles[0], Article):
            formatted_articles = []
            for article in articles:
                result = article.args
                result["picurl"] = result.pop("img")
                formatted_articles.append(result)
        else:
            formatted_articles = articles
        data = {
            "touser": user_id,
            "msgtype": "news",
            "news": {
                "articles": formatted_articles
            }
        }
        if kf_account is not None:
            data['customservice'] = {'kf_account': kf_account}
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data=data
        )

    def send_news_message(self, user_id, media_id, kf_account=None):
        """
        发送永久素材中的图文消息。

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 媒体文件 ID
        :param kf_account: 发送消息的客服账户，默认值为 None，None 为不指定
        :return: 返回的 JSON 数据包
        """
        data = {
            "touser": user_id,
            "msgtype": "mpnews",
            "mpnews": {
                "media_id": media_id
            }
        }
        if kf_account is not None:
            data['customservice'] = {'kf_account': kf_account}
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data=data
        )

    def send_miniprogrampage_message(
        self,
        user_id,
        title,
        appid,
        pagepath,
        thumb_media_id,
        kf_account=None
    ):
        """
        发送小程序卡片（要求小程序与公众号已关联）

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param title: 小程序卡片的标题
        :param appid: 小程序的 appid，要求小程序的 appid 需要与公众号有关联关系
        :param pagepath: 小程序的页面路径，跟 app.json 对齐，支持参数，比如 pages/index/index?foo=bar
        :param thumb_media_id: 小程序卡片图片的媒体 ID，小程序卡片图片建议大小为 520*416
        :param kf_account: 需要以某个客服帐号来发消息时指定的客服账户
        :return: 返回的 JSON 数据包
        """
        data = {
            "touser": user_id,
            "msgtype": "miniprogrampage",
            "miniprogrampage": {
                "title": title,
                "appid": appid,
                "pagepath": pagepath,
                "thumb_media_id": thumb_media_id
            }
        }
        if kf_account is not None:
            data["customservice"] = {"kf_account": kf_account}
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data=data
        )

    def create_qrcode(self, data):
        """
        创建二维码。

        :param data: 你要发送的参数 dict
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/qrcode/create", data=data
        )

    def show_qrcode(self, ticket):
        """
        通过ticket换取二维码。

        :param ticket: 二维码 ticket 。可以通过 :func:`create_qrcode` 获取到
        :return: 返回的 Request 对象
        """
        return requests.get(
            url="https://mp.weixin.qq.com/cgi-bin/showqrcode",
            params={"ticket": ticket}
        )

    def send_template_message(
        self, user_id, template_id, data, url='', miniprogram=None
    ):
        """
        发送模板消息
        详情请参考 https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param template_id: 模板 ID。
        :param data: 用于渲染模板的数据。
        :param url: 模板消息的可选链接。
        :param miniprogram: 跳小程序所需数据的可选数据。
        :return: 返回的 JSON 数据包
        """
        payload = {
            "touser": user_id,
            "template_id": template_id,
            "url": url,
            "data": data
        }
        if miniprogram:
            payload["miniprogram"] = miniprogram
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/template/send",
            data=payload
        )

    def create_tag(self, tag_name):
        """
        创建一个新标签

        :param tag_name: 标签名
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/tags/create",
            data={"tag": {
                "name": tag_name
            }}
        )

    def get_tags(self):
        """
        获取已经存在的标签

        :return: 返回的 JSON 数据包
        """
        return self.get(url="https://api.weixin.qq.com/cgi-bin/tags/get", )

    def update_tag(self, tag_id, tag_name):
        """
        修改标签

        :param tag_id: 标签 ID
        :param tag_name: 新的标签名
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/tags/update",
            data={"tag": {
                "id": tag_id,
                "name": tag_name
            }}
        )

    def delete_tag(self, tag_id):
        """
        删除标签

        :param tag_id: 标签 ID
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/tags/delete",
            data={"tag": {
                "id": tag_id,
            }}
        )

    def get_users_by_tag(self, tag_id, next_open_id=""):
        """
        获取标签下粉丝列表

        :param tag_id: 标签 ID
        :param next_open_id: 第一个拉取用户的 OPENID，默认从头开始拉取
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/user/tag/get",
            data={
                "tagid": tag_id,
                "next_openid": next_open_id
            }
        )

    def get_tags_by_user(self, open_id):
        """
        获取用户身上的标签列表

        :param open_id: 用户的 OPENID
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/tags/getidlist",
            data={
                "openid": open_id,
            }
        )

    def tag_users(self, tag_id, open_id_list):
        """
        批量为用户打标签

        :param tag_id: 标签 ID
        :param open_id_list: 包含一个或多个用户的 OPENID 的列表
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging",
            data={
                "openid_list": open_id_list,
                "tagid": tag_id
            }
        )

    def untag_users(self, tag_id, open_id_list):
        """
        批量为用户取消标签

        :param tag_id: 标签 ID
        :param open_id_list: 包含一个或多个用户的 OPENID 的列表
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/tags/members/batchuntagging",
            data={
                "openid_list": open_id_list,
                "tagid": tag_id
            }
        )

    def upload_news(self, articles):
        """
        上传图文消息素材 ::

            articles = [{
                "thumb_media_id":"qI6_Ze_6PtV7svjolgs-rN6stStuHIjs9_DidOHaj0Q-mwvBelOXCFZiq2OsIU-p",
                "author":"xxx",
                "title":"Happy Day",
                "content_source_url":"www.qq.com",
                "content":"content",
                "digest":"digest",
                "show_cover_pic":1,
                "need_open_comment":1,
                "only_fans_can_comment":1
            }]

        具体请参考: https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Batch_Sends_and_Originality_Checks.html#1


        :param articles: 上传的图文消息数据。
        :return: 返回的 JSON 数据包。
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/media/uploadnews",
            data={
                "articles": articles,
            }
        )

    def send_mass_msg(
        self,
        msg_type,
        content,
        user_list=None,
        send_ignore_reprint=False,
        client_msg_id=None
    ):
        """
        向指定对象群发信息。

        :param msg_type: 群发类型，图文消息为 mpnews，文本消息为 text，语音为 voice，音乐为 music，图片为 image，视频为 video，卡券为 wxcard。
        :param content: 群发内容。
        :param user_list: 发送对象，整型代表用户组，列表代表指定用户，如果为 None 则代表全部发送。
        :param send_ignore_reprint: 图文消息被判定为转载时，是否继续群发。 True 为继续群发（转载），False 为停止群发。 该参数默认为 False。
        :param client_msg_id: 群发时，微信后台将对 24 小时内的群发记录进行检查，如果该 clientmsgid 已经存在一条群发记录，则会拒绝本次群发请求，返回已存在的群发 msgid, 控制再 64 个字符内。
        :return: 返回的 JSON 数据包。
        """
        send_data = _build_send_data(msg_type, content)
        send_data['send_ignore_reprint'] = send_ignore_reprint
        if client_msg_id is not None:
            send_data['clientmsgid'] = client_msg_id
        if isinstance(user_list, list):
            url = 'https://api.weixin.qq.com/cgi-bin/message/mass/send'
            send_data['touser'] = user_list
        else:
            url = 'https://api.weixin.qq.com/cgi-bin/message/mass/sendall'
            if user_list == None:
                send_data['filter'] = {
                    "is_to_all": True,
                }
            else:
                send_data['filter'] = {"is_to_all": False, "tag_id": user_list}

        return self.post(url=url, data=send_data)

    def delete_mass_msg(self, msg_id, article_idx=0):
        """
        群发之后，随时可以通过该接口删除群发。

        :param msg_id: 发送出去的消息 ID。
        :param article_idx: 要删除的文章在图文消息中的位置，第一篇编号为 1，该字段不填或填 0 会删除全部文章。
        :return: 微信返回的 json 数据。
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/mass/delete",
            data={
                "msg_id": msg_id,
                "article_idx": article_idx
            }
        )

    def send_mass_preview_to_user(
        self, msg_type, content, user, user_type='openid'
    ):
        """
        开发者可通过该接口发送消息给指定用户，在手机端查看消息的样式和排版。为了满足第三方平台开发者的需求，在保留对 openID 预览能力的同时，增加了对指定微信号发送预览的能力，但该能力每日调用次数有限制（100 次），请勿滥用。

        :param user_type: 预览对象，`openid` 代表以 openid 发送，`wxname` 代表以微信号发送。
        :param msg_type: 发送类型，图文消息为 mpnews，文本消息为 text，语音为 voice，音乐为 music，图片为 image，视频为 video，卡券为 wxcard。
        :param content: 预览内容。
        :param user: 预览用户。
        :return: 返回的 json。
        """
        send_data = _build_send_data(msg_type, content)
        if user_type == 'openid':
            send_data['touser'] = user
        else:
            send_data['towxname'] = user
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/mass/preview",
            data=send_data
        )

    def get_mass_msg_status(self, msg_id):
        """
        查询群发消息发送状态。

        :param msg_id: 群发消息后返回的消息 id。
        :return: 返回的 json。
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/mass/get",
            data={'msg_id': msg_id}
        )

    def get_mass_msg_speed(self):
        """
        获取群发速度。

        :return: 返回的 json。
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/mass/speed/get",
            data={}
        )

    def set_mass_msg_speed(self, speed):
        """
        设置群发速度。

        :param speed: 群发速度的级别，是一个 0 到 4 的整数，数字越大表示群发速度越慢。
        :return: 返回的 json。
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/mass/speed/set",
            data={"speed": speed}
        )
