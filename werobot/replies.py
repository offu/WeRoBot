# -*- coding: utf-8 -*-
import time

from collections import defaultdict, namedtuple
from werobot.utils import is_string, to_text


def renderable_named_tuple(typename, field_names, tempalte):
    class TMP(namedtuple(typename=typename, field_names=field_names)):
        __TEMPLATE__ = tempalte

        @property
        def args(self):
            # https://bugs.python.org/issue24931
            return dict(zip(self._fields, self))

        def process_args(self, kwargs):
            args = defaultdict(str)
            for k, v in kwargs.items():
                if is_string(v):
                    v = to_text(v)
                args[k] = v
            return args

        def render(self):
            return to_text(
                self.__TEMPLATE__.format(**self.process_args(self.args))
            )

    TMP.__name__ = typename
    return TMP


class WeChatReply(object):
    def process_args(self, args):
        pass

    def __init__(self, message=None, **kwargs):
        if message and "source" not in kwargs:
            kwargs["source"] = message.target

        if message and "target" not in kwargs:
            kwargs["target"] = message.source

        if 'time' not in kwargs:
            kwargs["time"] = int(time.time())

        args = defaultdict(str)
        for k, v in kwargs.items():
            if is_string(v):
                v = to_text(v)
            args[k] = v
        self.process_args(args)
        self._args = args

    def render(self):
        return to_text(self.TEMPLATE.format(**self._args))

    def __getattr__(self, item):
        if item in self._args:
            return self._args[item]


class TextReply(WeChatReply):
    TEMPLATE = to_text(
        """
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
    </xml>
    """
    )


class ImageReply(WeChatReply):
    TEMPLATE = to_text(
        """
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[image]]></MsgType>
    <Image>
    <MediaId><![CDATA[{media_id}]]></MediaId>
    </Image>
    </xml>
    """
    )


class VoiceReply(WeChatReply):
    TEMPLATE = to_text(
        """
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[voice]]></MsgType>
    <Voice>
    <MediaId><![CDATA[{media_id}]]></MediaId>
    </Voice>
    </xml>
    """
    )


class VideoReply(WeChatReply):
    TEMPLATE = to_text(
        """
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[video]]></MsgType>
    <Video>
    <MediaId><![CDATA[{media_id}]]></MediaId>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{description}]]></Description>
    </Video>
    </xml>
    """
    )

    def process_args(self, args):
        args.setdefault('title', '')
        args.setdefault('description', '')


Article = renderable_named_tuple(
    typename="Article",
    field_names=("title", "description", "img", "url"),
    tempalte=to_text(
        """
    <item>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{description}]]></Description>
    <PicUrl><![CDATA[{img}]]></PicUrl>
    <Url><![CDATA[{url}]]></Url>
    </item>
    """
    )
)


class ArticlesReply(WeChatReply):
    TEMPLATE = to_text(
        """
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
    <ArticleCount>{count}</ArticleCount>
    <Articles>{items}</Articles>
    </xml>
    """
    )

    def __init__(self, message=None, **kwargs):
        super(ArticlesReply, self).__init__(message, **kwargs)
        self._articles = []

    def add_article(self, article):
        if len(self._articles) >= 10:
            raise AttributeError(
                "Can't add more than 10 articles"
                " in an ArticlesReply"
            )
        else:
            self._articles.append(article)

    def render(self):
        items = []
        for article in self._articles:
            items.append(article.render())
        self._args["items"] = ''.join(items)
        self._args["count"] = len(items)
        if "content" not in self._args:
            self._args["content"] = ''
        return ArticlesReply.TEMPLATE.format(**self._args)


class MusicReply(WeChatReply):
    TEMPLATE = to_text(
        """
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
    </xml>
    """
    )

    def process_args(self, args):
        if 'hq_url' not in args:
            args['hq_url'] = args['url']


class TransferCustomerServiceReply(WeChatReply):
    @property
    def TEMPLATE(self):
        if 'account' in self._args:
            return to_text(
                """
            <xml>
            <ToUserName><![CDATA[{target}]]></ToUserName>
            <FromUserName><![CDATA[{source}]]></FromUserName>
            <CreateTime>{time}</CreateTime>
            <MsgType><![CDATA[transfer_customer_service]]></MsgType>
            <TransInfo>
                 <KfAccount><![CDATA[{account}]]></KfAccount>
             </TransInfo>
            </xml>
            """
            )
        else:
            return to_text(
                """
            <xml>
            <ToUserName><![CDATA[{target}]]></ToUserName>
            <FromUserName><![CDATA[{source}]]></FromUserName>
            <CreateTime>{time}</CreateTime>
            <MsgType><![CDATA[transfer_customer_service]]></MsgType>
            </xml>
            """
            )


class SuccessReply(WeChatReply):
    def render(self):
        return "success"


def process_function_reply(reply, message=None):
    if is_string(reply):
        return TextReply(message=message, content=reply)
    elif isinstance(reply, list) and all([len(x) == 4 for x in reply]):
        if len(reply) > 10:
            raise AttributeError(
                "Can't add more than 10 articles"
                " in an ArticlesReply"
            )
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
    return reply
