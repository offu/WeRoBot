# -*- coding:utf-8 -*-

import time
import pytest

from werobot.parser import parse_user_msg
from werobot.replies import WeChatReply, TextReply, ImageReply, MusicReply
from werobot.replies import VoiceReply, VideoReply
from werobot.replies import Article, ArticlesReply
from werobot.replies import TransferCustomerServiceReply, SuccessReply
from werobot.replies import process_function_reply
from werobot.utils import to_binary, to_text


def test_wechat_reply():
    message = parse_user_msg("""
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <PicUrl><![CDATA[this is a url]]></PicUrl>
        <MediaId><![CDATA[media_id]]></MediaId>
        <MsgId>1234567890123456</MsgId>
        </xml>
    """)
    s = to_binary("喵fdsjaklfsk")
    reply = WeChatReply(message=message, s=s)
    assert reply._args['source'] == 'toUser'
    assert reply._args['target'] == 'fromUser'
    assert reply._args['s'] == to_text(s)
    assert isinstance(reply._args['time'], int)


def test_text_reply():
    t = int(time.time())
    reply = TextReply(
        target='fromUser', source='toUser',
        content="aa", time=t
    )
    assert reply.render().strip() == """
    <xml>
    <ToUserName><![CDATA[fromUser]]></ToUserName>
    <FromUserName><![CDATA[toUser]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[aa]]></Content>
    </xml>""".format(time=t).strip()


def test_image_reply():
    t = int(time.time())
    reply = ImageReply(
        target='fromUser',
        source='toUser',
        media_id="fdasfdasfasd", time=t
    )
    assert reply.render().strip() == """
    <xml>
    <ToUserName><![CDATA[fromUser]]></ToUserName>
    <FromUserName><![CDATA[toUser]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[image]]></MsgType>
    <Image>
    <MediaId><![CDATA[fdasfdasfasd]]></MediaId>
    </Image>
    </xml>""".format(time=t).strip()


def test_voice_reply():
    t = int(time.time())
    reply = VoiceReply(
        target='tgu',
        source='su',
        media_id="fdasfdasfasd", time=t
    )
    assert reply.render().strip() == """
    <xml>
    <ToUserName><![CDATA[tgu]]></ToUserName>
    <FromUserName><![CDATA[su]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[voice]]></MsgType>
    <Voice>
    <MediaId><![CDATA[fdasfdasfasd]]></MediaId>
    </Voice>
    </xml>""".format(time=t).strip()


def test_video_reply():
    t = int(time.time())
    reply = VideoReply(
        target='tgu',
        source='su',
        media_id="fdasfdasfasd", time=t,
    )
    assert reply.render().strip() == """
    <xml>
    <ToUserName><![CDATA[tgu]]></ToUserName>
    <FromUserName><![CDATA[su]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[video]]></MsgType>
    <Video>
    <MediaId><![CDATA[fdasfdasfasd]]></MediaId>
    <Title><![CDATA[]]></Title>
    <Description><![CDATA[]]></Description>
    </Video>
    </xml>""".format(time=t).strip()

    reply_2 = VideoReply(
        target='tgu',
        source='su',
        media_id="fdasfdasfasd", time=t,
        title='meow'
    )

    assert reply_2.render().strip() == """
    <xml>
    <ToUserName><![CDATA[tgu]]></ToUserName>
    <FromUserName><![CDATA[su]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[video]]></MsgType>
    <Video>
    <MediaId><![CDATA[fdasfdasfasd]]></MediaId>
    <Title><![CDATA[meow]]></Title>
    <Description><![CDATA[]]></Description>
    </Video>
    </xml>""".format(time=t).strip()

    reply_3 = VideoReply(
        target='tgu',
        source='su',
        media_id="fdasfdasfasd", time=t,
        title='meow',
        description='www'
    )
    assert reply_3.render().strip() == """
    <xml>
    <ToUserName><![CDATA[tgu]]></ToUserName>
    <FromUserName><![CDATA[su]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[video]]></MsgType>
    <Video>
    <MediaId><![CDATA[fdasfdasfasd]]></MediaId>
    <Title><![CDATA[meow]]></Title>
    <Description><![CDATA[www]]></Description>
    </Video>
    </xml>""".format(time=t).strip()


def test_video_reply_process_args():
    reply = VideoReply(
        target='tgu',
        source='su',
        media_id="fdasfdasfasd",
    )
    assert reply._args['title'] == ''
    assert reply._args['description'] == ''


def test_music_reply():
    t = int(time.time())
    reply = MusicReply(
        target='tg',
        source='ss',
        time=t,
        title='tt',
        description='ds',
        url='u1',
        hq_url='u2',
    )
    assert reply.render().strip() == """
    <xml>
    <ToUserName><![CDATA[tg]]></ToUserName>
    <FromUserName><![CDATA[ss]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[music]]></MsgType>
    <Music>
    <Title><![CDATA[tt]]></Title>
    <Description><![CDATA[ds]]></Description>
    <MusicUrl><![CDATA[u1]]></MusicUrl>
    <HQMusicUrl><![CDATA[u2]]></HQMusicUrl>
    </Music>
    </xml>""".format(time=t).strip()


def test_music_reply_process_args():
    reply = MusicReply(
        target='tg',
        source='ss',
        title='tt',
        description='ds',
        url='u1',
    )
    assert reply._args['hq_url'] == 'u1'

    reply_2 = MusicReply(
        target='tg',
        source='ss',
        title='tt',
        description='ds',
        url='u1',
        hq_url='u2'
    )
    assert reply_2._args['hq_url'] == 'u2'


def test_article():
    article = Article(
        title="tt",
        description=to_binary("附近的萨卡里发生"),
        img="http",
        url="uuu"
    )
    assert article.render().strip() == to_text("""
    <item>
    <Title><![CDATA[tt]]></Title>
    <Description><![CDATA[附近的萨卡里发生]]></Description>
    <PicUrl><![CDATA[http]]></PicUrl>
    <Url><![CDATA[uuu]]></Url>
    </item>
    """).strip()


def test_articles_reply():
    article = Article(
        title="tt",
        description="附近的萨卡里发生",
        img="http",
        url="uuu"
    )
    t = int(time.time())
    reply = ArticlesReply(
        target='tg',
        source='ss',
        time=t
    )
    assert reply.render().strip() == """
    <xml>
    <ToUserName><![CDATA[tg]]></ToUserName>
    <FromUserName><![CDATA[ss]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <Content><![CDATA[]]></Content>
    <ArticleCount>0</ArticleCount>
    <Articles></Articles>
    </xml>""".format(time=t).strip()

    reply._args['content'] = 'wwww'
    assert '<Content><![CDATA[wwww]]></Content>' in reply.render()
    reply.add_article(article)
    assert '<ArticleCount>1</ArticleCount>' in reply.render()
    assert article.render() in reply.render()
    for _ in range(9):
        reply.add_article(article)
    assert '<ArticleCount>10</ArticleCount>' in reply.render()
    with pytest.raises(AttributeError):
        reply.add_article(article)


def test_transfer_customer_service_reply():
    t = int(time.time())
    reply = TransferCustomerServiceReply(
        source='aaa',
        target='bbb',
        time=t
    )
    assert reply.render().strip() == """
    <xml>
    <ToUserName><![CDATA[bbb]]></ToUserName>
    <FromUserName><![CDATA[aaa]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[transfer_customer_service]]></MsgType>
    </xml>
    """.format(time=t).strip()


def test_success_reply():
    assert SuccessReply().render() == "success"


def test_process_unknown_function_reply():
    reply = SuccessReply()
    assert process_function_reply(reply) == reply


def test_process_text_function_reply():
    reply = process_function_reply("test")
    assert isinstance(reply, TextReply)
    assert reply.content == "test"


def test_process_music_function_reply():
    reply = process_function_reply([
       "title",
       "desc",
       "url"
    ])
    assert isinstance(reply, MusicReply)
    assert reply.title == "title"
    assert reply.description == "desc"
    assert reply.url == reply.hq_url == "url"

    reply = process_function_reply([
       "title",
       "desc",
       "url",
       "hq"
    ])
    assert isinstance(reply, MusicReply)
    assert reply.title == "title"
    assert reply.description == "desc"
    assert reply.url == "url"
    assert reply.hq_url == "hq"


def test_process_articles_function_reply():
    reply = process_function_reply([
        ["tt1", 'ds1', 'img', 'url'],
        ["tt2", 'ds2', 'im2g', 'u2rl']
    ])
    assert isinstance(reply, ArticlesReply)
    assert len(reply._articles) == 2
    article_1, article_2 = reply._articles
    assert isinstance(article_1, Article), isinstance(article_2, Article)
    assert article_1.title == "tt1", article_2.title == "tt2"
    assert article_1.description == "ds1", article_2.description == "ds2"
    assert article_1.img == "img", article_2.img == "im2g"
    assert article_1.url == "url", article_2.url == "u2rl"

    process_function_reply([[1, 2, 3, 4]] * 10)

    with pytest.raises(AttributeError):
        process_function_reply([[1, 2, 3, 4]] * 11)
