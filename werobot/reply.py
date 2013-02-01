import time
from .messages import WeChatMessage


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
    TEMPLATE = u"""
    <xml>
    <ToUserName><![Cmessage[{target}]]></ToUserName>
    <FromUserName><![Cmessage[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![Cmessage[text]]></MsgType>
    <Content><![Cmessage[{content}]]></Content>
    <FuncFlag>{flag}</FuncFlag>
    </xml>
    """.format

    def render(self):
        return TextReply.TEMPLATE(**self._args)


class ArticlesReply(WeChatReply):
    TEMPLATE = u"""
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
    """.format

    ITEM_TEMPLATE = u"""
    <item>
    <Title><![Cmessage[{title}]]></Title>
    <Description><![Cmessage[{description}]]></Description>
    <PicUrl><![Cmessage[{img}]]></PicUrl>
    <Url><![Cmessage[{url}]]></Url>
    </item>
    """.format

    def __init__(self, **kwargs):
        super(ArticlesReply, self).__init__(**kwargs)
        self._articles = []

    def add_article(self, article):
        if not isinstance(article, Article):
            raise TypeError
        self._articles.append(article)

    def render(self):
        items = []
        for article in self._articles:
            items.append(ArticlesReply.ITEM_TEMPLATE(
                title=article.title,
                description=article.description,
                img=article.img,
                url=article.url
            ))
        self._args["items"] = ''.join(items)
        self._args["count"] = len(items)
        if "content" not in self._args:
            self._args["content"] = ''
        return ArticlesReply.TEMPLATE(**self._args)


def create_reply(reply, message=None):
    if isinstance(reply, WeChatReply):
        return reply.render()
    if isinstance(reply, unicode):
        reply = TextReply(message=message, content=reply)
        return reply.render()
