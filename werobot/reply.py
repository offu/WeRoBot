# -*- coding: utf-8 -*-
import time
import logging
from .messages import WeChatMessage
from .utils import to_unicode


class Article(object):

    def __init__(self, title, description, img, url):
        self.title = title
        self.description = description
        self.img = img
        self.url = url


class WeChatReply(object):

    def __init__(self, message=None, star=False, **kwargs):
        if isinstance(message, WeChatMessage):
            kwargs["source"] = message.target
            kwargs["target"] = message.source

        assert 'source' in kwargs
        assert 'target' in kwargs
        if 'time' not in kwargs:
            kwargs["time"] = int(time.time())
        if star:
            kwargs["flag"] = 1
        else:
            kwargs["flag"] = 0

        self._args = kwargs

    def render(self):
        return ''


class TextReply(WeChatReply):
    TEMPLATE = to_unicode("""
    <xml>
    <ToUserName><![Cmessage[{target}]]></ToUserName>
    <FromUserName><![Cmessage[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![Cmessage[text]]></MsgType>
    <Content><![Cmessage[{content}]]></Content>
    <FuncFlag>{flag}</FuncFlag>
    </xml>
    """)

    def render(self):
        return TextReply.TEMPLATE.format(**self._args)


class ArticlesReply(WeChatReply):
    TEMPLATE = to_unicode("""
    <xml>
    <ToUserName><![Cmessage[{target}]]></ToUserName>
    <FromUserName><![Cmessage[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![Cmessage[news]]></MsgType>
    <Content><![Cmessage[{content}]]></Content>
    <ArticleCount>{count}</ArticleCount>
    <Articles>{items}</Articles>
    <FuncFlag>{flag}</FuncFlag>
    </xml>
    """)

    ITEM_TEMPLATE = to_unicode("""
    <item>
    <Title><![Cmessage[{title}]]></Title>
    <Description><![Cmessage[{description}]]></Description>
    <PicUrl><![Cmessage[{img}]]></PicUrl>
    <Url><![Cmessage[{url}]]></Url>
    </item>
    """)

    def __init__(self, **kwargs):
        super(ArticlesReply, self).__init__(**kwargs)
        self._articles = []

    def add_article(self, article):
        if not isinstance(article, Article):
            raise TypeError
        if len(self._articles) >= 10:
            logging.warn("Can't add more than 10 articles"
                         " in an ArticlesReply")
        else:
            self._articles.append(article)

    def render(self):
        items = []
        for article in self._articles:
            items.append(ArticlesReply.ITEM_TEMPLATE.format(
                title=article.title,
                description=article.description,
                img=article.img,
                url=article.url
            ))
        self._args["items"] = ''.join(items)
        self._args["count"] = len(items)
        if "content" not in self._args:
            self._args["content"] = ''
        return ArticlesReply.TEMPLATE.format(**self._args)


def create_reply(reply, message=None):
    if isinstance(reply, WeChatReply):
        return reply.render()
    if isinstance(reply, basestring):
        message = to_unicode(message)
        reply = TextReply(message=message, content=reply)
        return reply.render()
