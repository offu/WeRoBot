# -*- coding: utf-8 -*-
import os
import responses
import json
import pytest
import requests
import multipart
from six.moves import urllib
from six import BytesIO

from werobot import WeRoBot
from werobot.config import Config
from werobot.client import Client, check_error, ClientException
from werobot.utils import cached_property

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GOD_PIC = os.path.join(os.path.dirname(__file__), '照桥心美.png')
TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
JSON_HEADER = {'content-type': 'application/json'}


def token_callback(request):
    return 200, JSON_HEADER, json.dumps(
        {
            "access_token": "ACCESS_TOKEN",
            "expires_in": 7200
        }
    )


def add_token_response(method):
    def wrapped_func(self, *args, **kwargs):
        responses.add_callback(
            responses.GET, TOKEN_URL, callback=token_callback
        )
        method(self, *args, **kwargs)

    return wrapped_func


def create_pic_file(func):
    def wrapped_func(self, *args, **kwargs):
        with open(GOD_PIC, 'a') as f:
            f.write("just a test")
        try:
            func(self, *args, **kwargs)
        finally:
            os.remove(GOD_PIC)

    return wrapped_func


class BaseTestClass:
    @cached_property
    def client(self):
        config = Config()
        config.from_pyfile(os.path.join(BASE_DIR, "client_config.py"))
        return Client(config)

    @staticmethod
    def callback_without_check(request):
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})


class TestClientBaseClass(BaseTestClass):
    def test_id_and_secret(self):
        assert self.client.appid == "123"
        assert self.client.appsecret == "321"

    def test_robot_client(self):
        robot = WeRoBot()
        assert robot.client.config == robot.config

    def test_robot_reuse_client(self):
        robot = WeRoBot()
        client_1 = robot.client
        client_2 = robot.client
        assert client_1 is client_2

    def test_check_error(self):
        error_json = dict(error_code=0)
        assert error_json == check_error(error_json)

        error_json = dict(errcode=1, errmsg="test")
        with pytest.raises(ClientException) as err:
            check_error(error_json)
        assert err.value.args[0] == "1: test"

    @responses.activate
    @add_token_response
    def test_grant_token(self):
        # responses.add_callback(responses.GET, TOKEN_URL, callback=token_callback)
        self.client.grant_token()
        assert self.client.token == "ACCESS_TOKEN"

    @responses.activate
    @add_token_response
    def test_client_request(self):
        EMPTY_PARAMS_URL = "http://empty-params.werobot.com/"
        DATA_EXISTS_URL = "http://data-exists.werobot.com/"

        def empty_params_callback(request):
            params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
            assert params["access_token"][0] == self.client.token
            return 200, JSON_HEADER, json.dumps({"test": "test"})

        def data_exists_url(request):
            assert json.loads(request.body.decode('utf-8')) == {"test": "test"}
            return 200, JSON_HEADER, json.dumps({"test": "test"})

        responses.add_callback(
            responses.POST, DATA_EXISTS_URL, callback=data_exists_url
        )
        responses.add_callback(
            responses.GET, EMPTY_PARAMS_URL, callback=empty_params_callback
        )
        responses.add_callback(
            responses.GET, TOKEN_URL, callback=token_callback
        )

        r = self.client.get(url=EMPTY_PARAMS_URL)
        assert r == {"test": "test"}

        r = self.client.post(url=DATA_EXISTS_URL, data={"test": "test"})
        assert r == {"test": "test"}


class TestClientBaseClassPost(TestClientBaseClass):
    @pytest.fixture(autouse=True)
    def mock_request(self, mocker):
        self.mocked_request = mocker.spy(self.client, 'request')

    @responses.activate
    @add_token_response
    @create_pic_file
    def test_post_with_unittest(self):
        POST_FILE_URL = "http://post_file.werobot.com/"

        def empty_post_file_callback(request):
            return 200, JSON_HEADER, json.dumps({"test": "test"})

        responses.add_callback(
            responses.POST, POST_FILE_URL, callback=empty_post_file_callback
        )

        with open(GOD_PIC, 'rb') as f:
            self.client.post(url=POST_FILE_URL, files={"media": f})
            self.mocked_request.assert_any_call(
                method='post',
                url='http://post_file.werobot.com/',
                files=dict(media=(urllib.parse.quote(GOD_PIC), f))
            )

        # Test another attribute
        with open(GOD_PIC, 'rb') as f:
            self.client.post(url=POST_FILE_URL, files={"gugugu": f})
            self.mocked_request.assert_any_call(
                method='post',
                url='http://post_file.werobot.com/',
                files=dict(gugugu=(urllib.parse.quote(GOD_PIC), f))
            )

    @responses.activate
    @add_token_response
    def test_post_with_file_object_without_name(self):
        POST_FILE_URL = "http://post_file.werobot.com/"

        def empty_post_file_callback(request):
            return 200, JSON_HEADER, json.dumps({"test": "test"})

        responses.add_callback(
            responses.POST, POST_FILE_URL, callback=empty_post_file_callback
        )

        f = BytesIO(b'gugugu')
        self.client.post(url=POST_FILE_URL, files={"media": f})
        self.mocked_request.assert_any_call(
            method='post',
            url='http://post_file.werobot.com/',
            files=dict(media=f)
        )

    @responses.activate
    @add_token_response
    @create_pic_file
    def test_post_with_integration_test(self):
        POST_FILE_URL = "http://post_file.werobot.com/"

        def post_file_callback(request):
            s = request.body.split(b"\r")[0][2:]
            p = list(
                multipart.MultipartParser(
                    BytesIO(multipart.tob(request.body)), s
                )
            )[0]
            assert "filename" in p.options
            return 200, JSON_HEADER, json.dumps({"test": "test"})

        responses.add_callback(
            responses.POST, POST_FILE_URL, callback=post_file_callback
        )

        with open(GOD_PIC, 'rb') as f:
            self.client.post(url=POST_FILE_URL, files={"media": f})


class TestClientMenuClass(BaseTestClass):
    CREATE_URL = "https://api.weixin.qq.com/cgi-bin/menu/create"
    GET_URL = "https://api.weixin.qq.com/cgi-bin/menu/get"
    DELETE_URL = "https://api.weixin.qq.com/cgi-bin/menu/delete"

    menu_data = {
        "button": [
            {
                "type": "click",
                "name": u"今日歌曲",
                "key": "V1001_TODAY_MUSIC"
            }, {
                "type": "click",
                "name": u"歌手简介",
                "key": "V1001_TODAY_SINGER"
            }, {
                "name": u"菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": u"搜索",
                        "url": "http://www.soso.com/"
                    }, {
                        "type": "view",
                        "name": u"视频",
                        "url": "http://v.qq.com/"
                    }, {
                        "type": "click",
                        "name": u"赞一下我们",
                        "key": "V1001_GOOD"
                    }
                ]
            }
        ]
    }

    @staticmethod
    def create_menu_callback(request):
        def check_menu_data(item):
            keys = item.keys()
            assert "name" in keys
            if "sub_button" in keys:
                for button in item["sub_button"]:
                    check_menu_data(button)
                return
            assert "type" in keys
            if "type" == "click":
                assert "key" in keys
            elif "type" == "view":
                assert "url" in keys
            elif "type" == "media_id" or "type" == "view_limited":
                assert "media_id" in keys

        try:
            body = json.loads(request.body.decode("utf-8"))["button"]
        except KeyError:
            return 200, JSON_HEADER, json.dumps(
                {
                    "errcode": 1,
                    "errmsg": "error"
                }
            )
        try:
            for item in body:
                check_menu_data(item)
        except AssertionError:
            return 200, JSON_HEADER, json.dumps(
                {
                    "errcode": 1,
                    "errmsg": "error"
                }
            )
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_create_menu(self):
        responses.add_callback(
            responses.POST,
            self.CREATE_URL,
            callback=self.create_menu_callback
        )
        r = self.client.create_menu(self.menu_data)
        assert r == {"errcode": 0, "errmsg": "ok"}
        with pytest.raises(ClientException) as err:
            self.client.create_menu({"error": "error"})
        assert err.value.args[0] == "1: error"

    @responses.activate
    @add_token_response
    def test_get_menu(self):
        responses.add_callback(
            responses.GET, self.GET_URL, callback=self.callback_without_check
        )
        r = self.client.get_menu()
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_delete_menu(self):
        responses.add_callback(
            responses.GET,
            self.DELETE_URL,
            callback=self.callback_without_check
        )
        r = self.client.delete_menu()
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestClientGroupClass(BaseTestClass):
    CREATE_URL = "https://api.weixin.qq.com/cgi-bin/groups/create"
    GET_URL = "https://api.weixin.qq.com/cgi-bin/groups/get"
    GET_WITH_ID_URL = "https://api.weixin.qq.com/cgi-bin/groups/getid"
    UPDATE_URL = "https://api.weixin.qq.com/cgi-bin/groups/update"
    MOVE_URL = "https://api.weixin.qq.com/cgi-bin/groups/members/update"
    MOVE_USERS_URL = "https://api.weixin.qq.com/cgi-bin/groups/members/batchupdate"
    DELETE_URL = "https://api.weixin.qq.com/cgi-bin/groups/delete"

    @staticmethod
    def create_group_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "group" in body.keys()
        assert "name" in body["group"].keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def get_groups_with_id_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "openid" in body.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def update_group_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "group" in body.keys()
        assert "id" in body["group"].keys()
        assert "name" in body["group"].keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def move_user_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "openid" in body.keys()
        assert "to_groupid" in body.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def move_users_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "openid_list" in body.keys()
        assert "to_groupid" in body.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def delete_group_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "group" in body.keys()
        assert "id" in body["group"].keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_create_group(self):
        responses.add_callback(
            responses.POST,
            self.CREATE_URL,
            callback=self.create_group_callback
        )
        r = self.client.create_group("test")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_get_group(self):
        responses.add_callback(
            responses.GET, self.GET_URL, callback=self.callback_without_check
        )
        r = self.client.get_groups()
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_get_group_with_id(self):
        responses.add_callback(
            responses.POST,
            self.GET_WITH_ID_URL,
            callback=self.get_groups_with_id_callback
        )
        r = self.client.get_group_by_id("test")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_update_group(self):
        responses.add_callback(
            responses.POST,
            self.UPDATE_URL,
            callback=self.update_group_callback
        )
        r = self.client.update_group("0", "test")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_move_user(self):
        responses.add_callback(
            responses.POST, self.MOVE_URL, callback=self.move_user_callback
        )
        r = self.client.move_user("test", "0")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_move_users(self):
        responses.add_callback(
            responses.POST,
            self.MOVE_USERS_URL,
            callback=self.move_users_callback
        )
        r = self.client.move_users("test", "test")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_delete_group(self):
        responses.add_callback(
            responses.POST,
            self.DELETE_URL,
            callback=self.delete_group_callback
        )
        r = self.client.delete_group("test")
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestClientRemarkClass(BaseTestClass):
    REMARK_URL = "https://api.weixin.qq.com/cgi-bin/user/info/updateremark"

    @staticmethod
    def remark_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "openid" in body.keys()
        assert "remark" in body.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_client_remark(self):
        responses.add_callback(
            responses.POST, self.REMARK_URL, callback=self.remark_callback
        )
        r = self.client.remark_user("test", "test")
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestClientUserInfo(BaseTestClass):
    SINGLE_USER_URL = "https://api.weixin.qq.com/cgi-bin/user/info"
    MULTI_USER_URL = "https://api.weixin.qq.com/cgi-bin/user/info/batchget"

    @staticmethod
    def single_user_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        assert "openid" in params.keys()
        assert "lang" in params.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def multi_user_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "user_list" in body.keys()
        for user in body["user_list"]:
            assert "openid" in user.keys()
            assert "lang" in user.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_single_user(self):
        responses.add_callback(
            responses.GET,
            self.SINGLE_USER_URL,
            callback=self.single_user_callback
        )
        r = self.client.get_user_info("test")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_multi_user(self):
        responses.add_callback(
            responses.POST,
            self.MULTI_USER_URL,
            callback=self.multi_user_callback
        )
        r = self.client.get_users_info(["test1", "test2"])
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestClientGetFollowersClass(BaseTestClass):
    FOLLOWER_URL = "https://api.weixin.qq.com/cgi-bin/user/get"

    @staticmethod
    def get_followers_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        assert "next_openid" in params.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_get_followers(self):
        responses.add_callback(
            responses.GET,
            self.FOLLOWER_URL,
            callback=self.get_followers_callback
        )
        r = self.client.get_followers("test")
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestClientCustomMenuClass(BaseTestClass):
    GET_URL = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info"
    CREATE_URL = "https://api.weixin.qq.com/cgi-bin/menu/addconditional"
    DELETE_URL = "https://api.weixin.qq.com/cgi-bin/menu/delconditional"
    MATCH_URL = "https://api.weixin.qq.com/cgi-bin/menu/trymatch"

    custom_data = {
        "menu_data": [
            {
                "type": "click",
                "name": u"今日歌曲",
                "key": "V1001_TODAY_MUSIC"
            }, {
                "name": u"菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": u"搜索",
                        "url": "http://www.soso.com/"
                    }, {
                        "type": "view",
                        "name": u"视频",
                        "url": "http://v.qq.com/"
                    }, {
                        "type": "click",
                        "name": u"赞一下我们",
                        "key": "V1001_GOOD"
                    }
                ]
            }
        ],
        "matchrule": {
            "group_id": "2",
            "sex": "1",
            "country": u"中国",
            "province": u"广东",
            "city": u"广州",
            "client_platform_type": "2",
            "language": "zh_CN"
        }
    }

    @staticmethod
    def get_custom_menu_callback(request):
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def create_custom_menu_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "button" in body.keys()
        assert "matchrule" in body.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def delete_custom_menu_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "menuid" in body.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def match_custom_menu(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "user_id" in body.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_get_custom_menu(self):
        responses.add_callback(
            responses.GET,
            self.GET_URL,
            callback=self.get_custom_menu_callback
        )
        r = self.client.get_custom_menu_config()
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_create_custom_menu(self):
        responses.add_callback(
            responses.POST,
            self.CREATE_URL,
            callback=self.create_custom_menu_callback
        )
        r = self.client.create_custom_menu(**self.custom_data)
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_delete_custom_menu(self):
        responses.add_callback(
            responses.POST,
            self.DELETE_URL,
            callback=self.delete_custom_menu_callback
        )
        r = self.client.delete_custom_menu("test")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_march_custom_menu(self):
        responses.add_callback(
            responses.POST, self.MATCH_URL, callback=self.match_custom_menu
        )
        r = self.client.match_custom_menu("test")
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestClientResourceClass(BaseTestClass):
    UPLOAD_URL = "https://api.weixin.qq.com/cgi-bin/media/upload"
    DOWNLOAD_URL = "https://api.weixin.qq.com/cgi-bin/media/get"
    ADD_NEWS_URL = "https://api.weixin.qq.com/cgi-bin/material/add_news"
    UPLOAD_PICTURE_URL = "https://api.weixin.qq.com/cgi-bin/media/uploadimg"
    UPLOAD_P_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    DOWNLOAD_P_URL = "https://api.weixin.qq.com/cgi-bin/material/get_material"
    DELETE_P_URL = "https://api.weixin.qq.com/cgi-bin/material/del_material"
    UPDATE_NEWS_URL = "https://api.weixin.qq.com/cgi-bin/material/update_news"
    add_news_data = [
        {
            "title": "test_title",
            "thumb_media_id": "test",
            "author": "test",
            "digest": "test",
            "show_cover_pic": 1,
            "content": "test",
            "content_source_url": "test"
        }
    ]
    update_data = {
        "media_id": "test",
        "index": "test",
        "articles": {
            "title": "test",
            "thumb_media_id": "test",
            "author": "test",
            "digest": "test",
            "show_cover_pic": 1,
            "content": "test",
            "content_source_url": "test"
        }
    }

    @staticmethod
    def upload_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "type" in params.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def download_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "media_id" in params.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def add_news_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "articles" in body.keys()
        for article in body["articles"]:
            assert "title" in article.keys()
            assert "thumb_media_id" in article.keys()
            assert "author" in article.keys()
            assert "digest" in article.keys()
            assert "show_cover_pic" in article.keys()
            assert "content" in article.keys()
            assert "content_source_url" in article.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def upload_picture_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def upload_p_media_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        assert "type" in params.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def download_p_media_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        body = json.loads(request.body.decode("utf-8"))
        assert "media_id" in body.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def delete_p_media_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "media_id" in body.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def update_news_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "media_id" in body.keys()
        assert "index" in body.keys()
        assert "articles" in body.keys()
        articles = body["articles"]
        assert "title" in articles.keys()
        assert "thumb_media_id" in articles.keys()
        assert "author" in articles.keys()
        assert "digest" in articles.keys()
        assert "show_cover_pic" in articles.keys()
        assert "content" in articles.keys()
        assert "content_source_url" in articles.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    @create_pic_file
    def test_upload_media(self):
        responses.add_callback(
            responses.POST, self.UPLOAD_URL, callback=self.upload_callback
        )
        with open(GOD_PIC, 'rb') as f:
            r = self.client.upload_media('image', f)
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_download_media(self):
        responses.add_callback(
            responses.GET, self.DOWNLOAD_URL, callback=self.download_callback
        )
        r = self.client.download_media("test")
        assert isinstance(r, requests.Response)

    @responses.activate
    @add_token_response
    def test_add_news(self):
        responses.add_callback(
            responses.POST, self.ADD_NEWS_URL, callback=self.add_news_callback
        )
        r = self.client.add_news(self.add_news_data)
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    @create_pic_file
    def test_upload_news_picture(self):
        responses.add_callback(
            responses.POST,
            self.UPLOAD_PICTURE_URL,
            callback=self.upload_picture_callback
        )
        with open(GOD_PIC, 'rb') as f:
            r = self.client.upload_news_picture(f)
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    @create_pic_file
    def test_upload_permanent_media(self):
        responses.add_callback(
            responses.POST,
            self.UPLOAD_P_URL,
            callback=self.upload_p_media_callback
        )
        with open(GOD_PIC, 'rb') as f:
            r = self.client.upload_permanent_media('image', f)
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_download_permanent_media(self):
        responses.add_callback(
            responses.POST,
            self.DOWNLOAD_P_URL,
            callback=self.download_p_media_callback
        )
        r = self.client.download_permanent_media("test")
        assert isinstance(r, requests.Response)

    @responses.activate
    @add_token_response
    def test_delete_permanent_media(self):
        responses.add_callback(
            responses.POST,
            self.DELETE_P_URL,
            callback=self.delete_p_media_callback
        )
        r = self.client.delete_permanent_media("test")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_update_news(self):
        responses.add_callback(
            responses.POST,
            self.UPDATE_NEWS_URL,
            callback=self.update_news_callback
        )
        r = self.client.update_news(self.update_data)
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestUploadVideoClass(BaseTestClass):
    UPLOAD_VIDEO_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"

    @staticmethod
    def upload_video_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "type" in params.keys()
        assert params["type"][0] == "video"
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    @create_pic_file
    def test_upload_video(self):
        responses.add_callback(
            responses.POST,
            self.UPLOAD_VIDEO_URL,
            callback=self.upload_video_callback
        )
        with open(GOD_PIC, 'rb') as f:
            r = self.client.upload_permanent_video("test", "test", f)
        assert isinstance(r, requests.Response)


class TestMediaClass(BaseTestClass):
    GET_URL = "https://api.weixin.qq.com/cgi-bin/material/get_materialcount"
    GET_LIST_URL = "https://api.weixin.qq.com/cgi-bin/material/batchget_material"

    @staticmethod
    def get_media_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def get_media_list_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "type" in body.keys()
        assert "offset" in body.keys()
        assert "count" in body.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_get_media(self):
        responses.add_callback(
            responses.GET, self.GET_URL, callback=self.get_media_callback
        )
        r = self.client.get_media_count()
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_get_media_list(self):
        responses.add_callback(
            responses.POST,
            self.GET_LIST_URL,
            callback=self.get_media_list_callback
        )
        r = self.client.get_media_list("test", "test", "test")
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestGetIpListClass(BaseTestClass):
    GET_URL = "https://api.weixin.qq.com/cgi-bin/getcallbackip"

    @staticmethod
    def get_ip_list_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_get_ip_list(self):
        responses.add_callback(
            responses.GET, self.GET_URL, callback=self.get_ip_list_callback
        )
        r = self.client.get_ip_list()
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestCustomService(BaseTestClass):
    ADD_URL = "https://api.weixin.qq.com/customservice/kfaccount/add"
    UPDATE_URL = "https://api.weixin.qq.com/customservice/kfaccount/update"
    DELETE_URL = "https://api.weixin.qq.com/customservice/kfaccount/del"
    UPLOAD_URL = "http://api.weixin.qq.com/customservice/kfaccount/uploadheadimg"
    GET_URL = "https://api.weixin.qq.com/cgi-bin/customservice/getkflist"
    GET_ONLINE_URL = "https://api.weixin.qq.com/cgi-bin/customservice/getonlinekflist"

    @staticmethod
    def add_update_delete_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "kf_account" in body.keys()
        assert "nickname" in body.keys()
        assert "password" in body.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def upload_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def get_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_add_custom_service_account(self):
        responses.add_callback(
            responses.POST,
            self.ADD_URL,
            callback=self.add_update_delete_callback
        )
        r = self.client.add_custom_service_account("test", "test", "test")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_update_custom_service_account(self):
        responses.add_callback(
            responses.POST,
            self.UPDATE_URL,
            callback=self.add_update_delete_callback
        )
        r = self.client.update_custom_service_account("test", "test", "test")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_delete_custom_service_account(self):
        responses.add_callback(
            responses.POST,
            self.DELETE_URL,
            callback=self.add_update_delete_callback
        )
        r = self.client.delete_custom_service_account("test", "test", "test")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    @create_pic_file
    def test_upload_custom_service_account_avatar(self):
        responses.add_callback(
            responses.POST, self.UPLOAD_URL, callback=self.upload_callback
        )
        with open(GOD_PIC, 'rb') as f:
            r = self.client.upload_custom_service_account_avatar("image", f)
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_get_custom_service_account_list(self):
        responses.add_callback(
            responses.GET, self.GET_URL, callback=self.get_callback
        )
        r = self.client.get_custom_service_account_list()
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_get_online_custom_service_account_list(self):
        responses.add_callback(
            responses.GET, self.GET_ONLINE_URL, callback=self.get_callback
        )
        r = self.client.get_online_custom_service_account_list()
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestQrcodeClass(BaseTestClass):
    CREATE_URL = "https://api.weixin.qq.com/cgi-bin/qrcode/create"
    SHOW_URL = "https://mp.weixin.qq.com/cgi-bin/showqrcode"

    @staticmethod
    def create_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @staticmethod
    def show_callback(request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "ticket" in params.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_create_qrcode(self):
        responses.add_callback(
            responses.POST, self.CREATE_URL, callback=self.create_callback
        )
        r = self.client.create_qrcode("test")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @responses.activate
    @add_token_response
    def test_show_qrcode(self):
        responses.add_callback(
            responses.GET, self.SHOW_URL, callback=self.show_callback
        )
        r = self.client.show_qrcode("test")
        assert isinstance(r, requests.Response)


class TestSendArticleMessagesClass(BaseTestClass):
    URL = "https://api.weixin.qq.com/cgi-bin/message/custom/send"

    @staticmethod
    def article_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "news"
        assert "news" in body.keys()
        for article in body["news"]["articles"]:
            assert "title" in article.keys()
            assert "description" in article.keys()
            assert "url" in article.keys()
            assert "picurl" in article.keys()
        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_article_messages(self):
        responses.add_callback(
            responses.POST, self.URL, callback=self.article_callback
        )

        from werobot.replies import Article
        articles = []
        for _ in range(0, 8):
            articles.append(
                Article(
                    *[
                        "test_title", "test_description", "test_img",
                        "test_url"
                    ]
                )
            )

        r = self.client.send_article_message("test_id", articles)
        assert r == {"errcode": 0, "errmsg": "ok"}

        articles = []
        for _ in range(0, 8):
            articles.append(
                {
                    "title": "test_title",
                    "description": "test_description",
                    "url": "test_url",
                    "picurl": "test_pic_url"
                }
            )

        r = self.client.send_article_message("test_id", articles)
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestSendTextMessageClass(BaseTestClass):
    URL = "https://api.weixin.qq.com/cgi-bin/message/custom/send"

    @staticmethod
    def text_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "text"
        assert "text" in body.keys()
        assert "content" in body["text"].keys()
        assert "customservice" not in body.keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_text_message(self):
        responses.add_callback(
            responses.POST, self.URL, callback=self.text_callback
        )

        r = self.client.send_text_message("test_id", "test_message")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @staticmethod
    def text_with_kf_account_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "text"
        assert "text" in body.keys()
        assert "content" in body["text"].keys()
        assert "customservice" in body.keys()
        assert "kf_account" in body["customservice"].keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_text_message_with_kf_account(self):
        responses.add_callback(
            responses.POST,
            self.URL,
            callback=self.text_with_kf_account_callback
        )
        r = self.client.send_text_message("test_id", "test_message", "233@233")
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestSendImageMessageClass(BaseTestClass):
    URL = "https://api.weixin.qq.com/cgi-bin/message/custom/send"

    @staticmethod
    def image_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "image"
        assert "image" in body.keys()
        assert "media_id" in body["image"].keys()
        assert "customservice" not in body.keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_image_message(self):
        responses.add_callback(
            responses.POST, self.URL, callback=self.image_callback
        )

        r = self.client.send_image_message("test_id", "test_media_id")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @staticmethod
    def image_with_kf_account_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "image"
        assert "image" in body.keys()
        assert "media_id" in body["image"].keys()
        assert "customservice" in body.keys()
        assert "kf_account" in body["customservice"].keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_image_message_with_kf_account(self):
        responses.add_callback(
            responses.POST,
            self.URL,
            callback=self.image_with_kf_account_callback
        )

        r = self.client.send_image_message(
            "test_id", "test_media_id", "233@233"
        )
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestSendVoiceMessageClass(BaseTestClass):
    URL = "https://api.weixin.qq.com/cgi-bin/message/custom/send"

    @staticmethod
    def voice_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "voice"
        assert "voice" in body.keys()
        assert "media_id" in body["voice"].keys()
        assert "customservice" not in body.keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_voice_message(self):
        responses.add_callback(
            responses.POST, self.URL, callback=self.voice_callback
        )

        r = self.client.send_voice_message("test_id", "test_media_id")
        assert r == {"errcode": 0, "errmsg": "ok"}

    @staticmethod
    def voice_with_kf_account_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "voice"
        assert "voice" in body.keys()
        assert "media_id" in body["voice"].keys()
        assert "customservice" in body.keys()
        assert "kf_account" in body["customservice"].keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_voice_message_with_kf_account(self):
        responses.add_callback(
            responses.POST,
            self.URL,
            callback=self.voice_with_kf_account_callback
        )

        r = self.client.send_voice_message(
            "test_id", "test_media_id", "233@233"
        )
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestMusicMessageClass(BaseTestClass):
    URL = "https://api.weixin.qq.com/cgi-bin/message/custom/send"

    @staticmethod
    def music_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "music"
        assert "music" in body.keys()
        assert "musicurl" in body["music"].keys()
        assert "hqmusicurl" in body["music"].keys()
        assert "thumb_media_id" in body["music"].keys()
        assert "customservice" not in body.keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_music_message(self):
        responses.add_callback(
            responses.POST, self.URL, callback=self.music_callback
        )

        r = self.client.send_music_message(
            user_id="test_id",
            url="test_url",
            hq_url="test_hq_url",
            thumb_media_id="test_media_id",
            title="test_title",
            description="test_description"
        )
        assert r == {"errcode": 0, "errmsg": "ok"}

    @staticmethod
    def music_with_kf_account_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "music"
        assert "music" in body.keys()
        assert "musicurl" in body["music"].keys()
        assert "hqmusicurl" in body["music"].keys()
        assert "thumb_media_id" in body["music"].keys()
        assert "customservice" in body.keys()
        assert "kf_account" in body["customservice"].keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_music_message_with_kf_account(self):
        responses.add_callback(
            responses.POST,
            self.URL,
            callback=self.music_with_kf_account_callback
        )

        r = self.client.send_music_message(
            user_id="test_id",
            url="test_url",
            hq_url="test_hq_url",
            thumb_media_id="test_media_id",
            title="test_title",
            description="test_description",
            kf_account="233@233"
        )
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestVideoMessageClass(BaseTestClass):
    URL = "https://api.weixin.qq.com/cgi-bin/message/custom/send"

    @staticmethod
    def video_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "video"
        assert "video" in body.keys()
        assert "media_id" in body["video"].keys()
        assert "customservice" not in body.keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_video_message(self):
        responses.add_callback(
            responses.POST, self.URL, callback=self.video_callback
        )
        r = self.client.send_video_message(
            user_id="test_id",
            media_id="test_media_id",
            title="test_title",
            description="test_description",
        )
        assert r == {"errcode": 0, "errmsg": "ok"}

    @staticmethod
    def video_with_kf_account_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "video"
        assert "video" in body.keys()
        assert "media_id" in body["video"].keys()
        assert "customservice" in body.keys()
        assert "kf_account" in body["customservice"].keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_video_message_with_kf_account(self):
        responses.add_callback(
            responses.POST,
            self.URL,
            callback=self.video_with_kf_account_callback
        )
        r = self.client.send_video_message(
            user_id="test_id",
            media_id="test_media_id",
            title="test_title",
            description="test_description",
            kf_account="233@233"
        )
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestNewsMessageClass(BaseTestClass):
    URL = "https://api.weixin.qq.com/cgi-bin/message/custom/send"

    @staticmethod
    def news_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "mpnews"
        assert "mpnews" in body.keys()
        assert "media_id" in body["mpnews"].keys()
        assert "customservice" not in body.keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_news_message(self):
        responses.add_callback(
            responses.POST, self.URL, callback=self.news_callback
        )

        r = self.client.send_news_message(
            user_id="test_id", media_id="test_media_id"
        )
        assert r == {"errcode": 0, "errmsg": "ok"}

    @staticmethod
    def news_with_kf_account_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "mpnews"
        assert "mpnews" in body.keys()
        assert "media_id" in body["mpnews"].keys()
        assert "customservice" in body.keys()
        assert "kf_account" in body["customservice"].keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_news_message_with_kf_account(self):
        responses.add_callback(
            responses.POST,
            self.URL,
            callback=self.news_with_kf_account_callback
        )

        r = self.client.send_news_message(
            user_id="test_id", media_id="test_media_id", kf_account="233@233"
        )
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestTemplateMessage(BaseTestClass):
    URL = "https://api.weixin.qq.com/cgi-bin/message/template/send"

    @staticmethod
    def template_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "template_id" in body.keys()
        assert "url" in body.keys()
        assert "data" in body.keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_template_message(self):
        responses.add_callback(
            responses.POST, self.URL, callback=self.template_callback
        )

        r = self.client.send_template_message(
            user_id="test_id",
            template_id="test_template_id",
            data="test_data",
            url="test_url"
        )
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestMiniprogrampageMessage(BaseTestClass):
    URL = "https://api.weixin.qq.com/cgi-bin/message/custom/send"

    @staticmethod
    def miniprogrampage_callback(request):
        body = json.loads(request.body.decode("utf-8"))
        assert "touser" in body.keys()
        assert "msgtype" in body.keys()
        assert body["msgtype"] == "miniprogrampage"
        assert "miniprogrampage" in body.keys()
        miniprogrampage = body["miniprogrampage"]
        assert "title" in miniprogrampage.keys()
        assert "appid" in miniprogrampage.keys()
        assert "pagepath" in miniprogrampage.keys()
        assert "thumb_media_id" in miniprogrampage.keys()

        return 200, JSON_HEADER, json.dumps({"errcode": 0, "errmsg": "ok"})

    @responses.activate
    @add_token_response
    def test_send_miniprogrampage_message(self):
        responses.add_callback(
            responses.POST, self.URL, callback=self.miniprogrampage_callback
        )

        r = self.client.send_miniprogrampage_message(
            user_id="test_id",
            title="test_title",
            appid="test_appid",
            pagepath="test_pagepath",
            thumb_media_id="test_id"
        )
        assert r == {"errcode": 0, "errmsg": "ok"}


class TestClientTagManageClass(BaseTestClass):
    CREATE_TAG_URL = "https://api.weixin.qq.com/cgi-bin/tags/create"
    GET_TAGS_URL = "https://api.weixin.qq.com/cgi-bin/tags/get"
    UPDATE_TAG_URL = "https://api.weixin.qq.com/cgi-bin/tags/update"
    DELETE_TAG_URL = "https://api.weixin.qq.com/cgi-bin/tags/delete"
    GET_USERS_BY_TAG_URL = "https://api.weixin.qq.com/cgi-bin/user/tag/get"

    create_tag_name = u"喵喵喵"
    create_tag_id = 100

    update_tag_name = "nyanya"
    update_tag_id = 100

    get_tags_response = {
        'tags': [
            {
                'id': 2,
                'name': u'星标组',
                'count': 0
            }, {
                'id': 100,
                'name': update_tag_name,
                'count': 0
            }
        ]
    }

    get_users_by_tag_id = 100
    get_users_by_tag_response = {
        'count': 1,
        'data': {
            'openid': ['testopenid']
        },
        'next_openid': 'testopenid'
    }

    delete_tag_id = 100

    def create_tag_callback(self, request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        body = json.loads(request.body.decode("utf-8"))
        assert body == {"tag": {"name": self.create_tag_name}}
        return 200, JSON_HEADER, json.dumps(
            {"tag": {
                "id": self.create_tag_id,
                "name": self.create_tag_name
            }}
        )

    def update_tag_callback(self, request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        body = json.loads(request.body.decode("utf-8"))
        assert body == {
            "tag": {
                "id": self.update_tag_id,
                "name": self.update_tag_name
            }
        }
        return 200, JSON_HEADER, json.dumps({'errcode': 0, 'errmsg': 'ok'})

    def get_tags_callback(self, request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        return 200, JSON_HEADER, json.dumps(self.get_tags_response)

    def get_users_by_tag_callback(self, request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        body = json.loads(request.body.decode("utf-8"))
        assert body == {"tagid": self.get_users_by_tag_id, "next_openid": ""}
        return 200, JSON_HEADER, json.dumps(self.get_users_by_tag_response)

    def delete_tag_callback(self, request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        body = json.loads(request.body.decode("utf-8"))
        assert body == {
            "tag": {
                "id": self.delete_tag_id,
            }
        }
        return 200, JSON_HEADER, json.dumps({'errcode': 0, 'errmsg': 'ok'})

    @responses.activate
    @add_token_response
    def test_create_tag(self):
        responses.add_callback(
            responses.POST,
            self.CREATE_TAG_URL,
            callback=self.create_tag_callback
        )
        r = self.client.create_tag(self.create_tag_name)
        assert r == {
            "tag": {
                "id": self.create_tag_id,
                "name": self.create_tag_name
            }
        }

    @responses.activate
    @add_token_response
    def test_update_tag(self):
        responses.add_callback(
            responses.POST,
            self.UPDATE_TAG_URL,
            callback=self.update_tag_callback
        )
        r = self.client.update_tag(self.update_tag_id, self.update_tag_name)
        assert r == {'errcode': 0, 'errmsg': 'ok'}

    @responses.activate
    @add_token_response
    def test_get_tags(self):
        responses.add_callback(
            responses.GET, self.GET_TAGS_URL, callback=self.get_tags_callback
        )
        r = self.client.get_tags()
        assert r == self.get_tags_response

    @responses.activate
    @add_token_response
    def test_get_users_by_tag(self):
        responses.add_callback(
            responses.POST,
            self.GET_USERS_BY_TAG_URL,
            callback=self.get_users_by_tag_callback
        )
        r = self.client.get_users_by_tag(self.get_users_by_tag_id)
        assert r == self.get_users_by_tag_response

    @responses.activate
    @add_token_response
    def test_delete_tag(self):
        responses.add_callback(
            responses.POST,
            self.DELETE_TAG_URL,
            callback=self.delete_tag_callback
        )
        r = self.client.delete_tag(self.delete_tag_id)
        assert r == {'errcode': 0, 'errmsg': 'ok'}


class TestClientMembersTagClass(BaseTestClass):
    TAG_USER_URL = "https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging"
    UNTAG_USER_URL = "https://api.weixin.qq.com/cgi-bin/tags/members/batchuntagging"
    GET_TAGS_BY_USER_URL = "https://api.weixin.qq.com/cgi-bin/tags/getidlist"

    tag_id = 100
    user_a_open_id = 'a'
    user_b_open_id = 'b'
    user_c_open_id = 'c'
    users_list = [user_a_open_id, user_b_open_id, user_c_open_id]

    get_tags_by_user_response = {'tagid_list': [tag_id]}

    def tag_user_callback(self, request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        body = json.loads(request.body.decode("utf-8"))
        assert body == {"openid_list": self.users_list, "tagid": self.tag_id}
        return 200, JSON_HEADER, json.dumps({'errcode': 0, 'errmsg': 'ok'})

    def untag_user_callback(self, request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        body = json.loads(request.body.decode("utf-8"))
        assert body == {"openid_list": self.users_list, "tagid": self.tag_id}
        return 200, JSON_HEADER, json.dumps({'errcode': 0, 'errmsg': 'ok'})

    def get_tags_by_user_callback(self, request):
        params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
        assert "access_token" in params.keys()
        body = json.loads(request.body.decode("utf-8"))
        assert body == {
            "openid": self.user_a_open_id,
        }
        return 200, JSON_HEADER, json.dumps(self.get_tags_by_user_response)

    @responses.activate
    @add_token_response
    def test_tag_users(self):
        responses.add_callback(
            responses.POST, self.TAG_USER_URL, callback=self.tag_user_callback
        )
        r = self.client.tag_users(self.tag_id, self.users_list)
        assert r == {'errcode': 0, 'errmsg': 'ok'}

    @responses.activate
    @add_token_response
    def test_untag_users(self):
        responses.add_callback(
            responses.POST,
            self.UNTAG_USER_URL,
            callback=self.untag_user_callback
        )
        r = self.client.untag_users(self.tag_id, self.users_list)
        assert r == {'errcode': 0, 'errmsg': 'ok'}

    @responses.activate
    @add_token_response
    def test_get_tags_by_user(self):
        responses.add_callback(
            responses.POST,
            self.GET_TAGS_BY_USER_URL,
            callback=self.get_tags_by_user_callback
        )
        r = self.client.get_tags_by_user(self.user_a_open_id)
        assert r == self.get_tags_by_user_response
