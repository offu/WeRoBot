# -*- coding: utf-8 -*-
import time

from werobot.messages import WeChatMessage
from werobot.utils import is_string, to_text


class Article(object):
    def __init__(self, title, description, img, url):
        self.title = title
        self.description = description
        self.img = img
        self.url = url


class WeChatReply(object):

    def __init__(self, message=None, star=False, **kwargs):
        if "source" not in kwargs and isinstance(message, WeChatMessage):
            kwargs["source"] = message.target

        if "target" not in kwargs and isinstance(message, WeChatMessage):
            kwargs["target"] = message.source

        if 'time' not in kwargs:
            kwargs["time"] = int(time.time())
        if star:
            kwargs["flag"] = 1
        else:
            kwargs["flag"] = 0

        args = dict()
        for k, v in kwargs.items():
            if is_string(v):
                v = to_text(v)
            args[k] = v

        self._args = args

    def render(self):
        raise NotImplementedError()


class TextReply(WeChatReply):
    TEMPLATE = to_text("""
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
    <FuncFlag>{flag}</FuncFlag>
    </xml>
    """)

    def render(self):
        return TextReply.TEMPLATE.format(**self._args)


class ArticlesReply(WeChatReply):
    TEMPLATE = to_text("""
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
    <ArticleCount>{count}</ArticleCount>
    <Articles>{items}</Articles>
    <FuncFlag>{flag}</FuncFlag>
    </xml>
    """)

    ITEM_TEMPLATE = to_text("""
    <item>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{description}]]></Description>
    <PicUrl><![CDATA[{img}]]></PicUrl>
    <Url><![CDATA[{url}]]></Url>
    </item>
    """)

    def __init__(self, message=None, star=False, **kwargs):
        super(ArticlesReply, self).__init__(message, star, **kwargs)
        self._articles = []

    def add_article(self, article):
        if len(self._articles) >= 10:
            raise AttributeError("Can't add more than 10 articles"
                                 " in an ArticlesReply")
        else:
            self._articles.append(article)

    def render(self):
        items = []
        for article in self._articles:
            items.append(ArticlesReply.ITEM_TEMPLATE.format(
                title=to_text(article.title),
                description=to_text(article.description),
                img=to_text(article.img),
                url=to_text(article.url)
            ))
        self._args["items"] = ''.join(items)
        self._args["count"] = len(items)
        if "content" not in self._args:
            self._args["content"] = ''
        return ArticlesReply.TEMPLATE.format(**self._args)


class MusicReply(WeChatReply):
    TEMPLATE = to_text("""
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[music]]></MsgType>
    <Music>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{description}]]></Description>
    <MusicUrl><![CDATA[{url}]]></MusicUrl>
    <HQMusicUrl><![CDATA[{hq_url}]]></HQMusicUrl>
    </Music>
    <FuncFlag>{flag}</FuncFlag>
    </xml>
    """)

    def render(self):
        return MusicReply.TEMPLATE.format(**self._args)


class TransferCustomerServiceReply(WeChatReply):
    TEMPLATE = to_text("""
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[transfer_customer_service]]></MsgType>
    </xml>
    """)

    def render(self):
        return TransferCustomerServiceReply.TEMPLATE.format(**self._args)


def process_function_reply(reply, message=None):
    if is_string(reply):
        return TextReply(message=message, content=reply)
    elif isinstance(reply, list) and all([len(x) == 4 for x in reply]):
        if len(reply) > 10:
            raise AttributeError("Can't add more than 10 articles"
                                 " in an ArticlesReply")
        r = ArticlesReply(message=message)
        for article in reply:
            article = Article(*article)
            r.add_article(article)
        return r
    elif isinstance(reply, list) and 3 <= len(reply) <= 4:
        if len(reply) == 3:
            # 如果数组长度为3， 那么高质量音乐链接的网址和普通质量的网址相同。
            reply.append(reply[-1])
        title, description, url, hq_url = reply
        return MusicReply(
            message=message,
            title=title,
            description=description,
            url=url,
            hq_url=hq_url
        )


def create_reply(reply, message=None):
    if not isinstance(reply, WeChatReply):
        reply = process_function_reply(reply, message=message)
    return reply.render()
