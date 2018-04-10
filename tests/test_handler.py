# -*- coding: utf-8 -*-

from werobot import WeRoBot
from werobot.parser import parse_user_msg
from werobot.replies import TextReply
import os

werobot = WeRoBot(enable_session=False)


def teardown_module(module):
    try:
        os.remove(os.path.abspath("werobot_session"))
    except OSError:
        pass


def test_subscribe_handler():
    @werobot.subscribe
    def subscribe(message):
        return '关注'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[subscribe]]></Event>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'关注'


def test_unsubscribe_handler():
    @werobot.unsubscribe
    def unsubscribe(message):
        return '取消关注'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[unsubscribe]]></Event>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'取消关注'


def test_scan_push_handler():
    @werobot.scancode_push
    def scancode_push(message):
        return '扫描推送'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[scancode_push]]></Event>
            <EventKey><![CDATA[EVENTKEY]]></EventKey>
            <ScanCodeInfo>
                <ScanType><![CDATA[qrcode]]></ScanType>
                <ScanResult><![CDATA[http://www.qq.com]]></ScanResult>
            </ScanCodeInfo>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'扫描推送'


def test_scan_waitmsg_handler():
    @werobot.scancode_waitmsg
    def scancode_waitmsg(message):
        return '扫描弹消息'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[scancode_waitmsg]]></Event>
            <EventKey><![CDATA[EVENTKEY]]></EventKey>
            <ScanCodeInfo>
                <ScanType><![CDATA[qrcode]]></ScanType>
                <ScanResult><![CDATA[http://www.qq.com]]></ScanResult>
            </ScanCodeInfo>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'扫描弹消息'


def test_pic_sysphoto_handler():
    @werobot.pic_sysphoto
    def pic_sysphoto():
        return '瞧一瞧系统拍照'

    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[gh_e136c6e50636]]></ToUserName>
        <FromUserName><![CDATA[oMgHVjngRipVsoxg6TuX3vz6glDg]]></FromUserName>
        <CreateTime>1408090651</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[pic_sysphoto]]></Event>
        <EventKey><![CDATA[6]]></EventKey>
        <SendPicsInfo>
            <Count>1</Count>
            <PicList>
                <item>
                    <PicMd5Sum><![CDATA[1b5f7c23b5bf75682a53e7b6d163e185]]></PicMd5Sum>
                </item>
            </PicList>
        </SendPicsInfo>
    </xml>
    """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'瞧一瞧系统拍照'


def test_pic_photo_or_album_handler():
    @werobot.pic_photo_or_album
    def pic_photo_or_album():
        return '瞧一瞧拍照或者相册'

    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[gh_e136c6e50636]]></ToUserName>
        <FromUserName><![CDATA[oMgHVjngRipVsoxg6TuX3vz6glDg]]></FromUserName>
        <CreateTime>1408090816</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[pic_photo_or_album]]></Event>
        <EventKey><![CDATA[6]]></EventKey>
        <SendPicsInfo>
            <Count>1</Count>
            <PicList>
                <item>
                    <PicMd5Sum><![CDATA[5a75aaca956d97be686719218f275c6b]]></PicMd5Sum>
                </item>
            </PicList>
        </SendPicsInfo>
    </xml>
    """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'瞧一瞧拍照或者相册'


def test_pic_weixin_handler():
    @werobot.pic_weixin
    def pic_weixin():
        return '瞧一瞧微信相册'

    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[gh_e136c6e50636]]></ToUserName>
        <FromUserName><![CDATA[oMgHVjngRipVsoxg6TuX3vz6glDg]]></FromUserName>
        <CreateTime>1408090816</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[pic_weixin]]></Event>
        <EventKey><![CDATA[6]]></EventKey>
        <SendPicsInfo>
            <Count>1</Count>
            <PicList>
                <item>
                    <PicMd5Sum><![CDATA[5a75aaca956d97be686719218f275c6b]]></PicMd5Sum>
                </item>
            </PicList>
        </SendPicsInfo>
    </xml>
    """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'瞧一瞧微信相册'


def test_location_select_handler():
    @werobot.location_select
    def location_select():
        return '瞧一瞧地理位置'

    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[gh_e136c6e50636]]></ToUserName>
        <FromUserName><![CDATA[oMgHVjngRipVsoxg6TuX3vz6glDg]]></FromUserName>
        <CreateTime>1408091189</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[location_select]]></Event>
        <EventKey><![CDATA[6]]></EventKey>
        <SendLocationInfo>
            <Location_X><![CDATA[23]]></Location_X>
            <Location_Y><![CDATA[113]]></Location_Y>
            <Scale><![CDATA[15]]></Scale>
            <Label><![CDATA[广州市海珠区客村艺苑路 106号]]></Label>
            <Poiname><![CDATA[]]></Poiname>
        </SendLocationInfo>
    </xml>
    """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'瞧一瞧地理位置'


def test_click_handler():
    @werobot.click
    def scan(message):
        return '喵喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[CLICK]]></Event>
            <EventKey><![CDATA[EVENTKEY]]></EventKey>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'喵喵'


def test_view_handler():
    @werobot.view
    def view(message):
        return '汪汪'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[VIEW]]></Event>
            <EventKey><![CDATA[www.qq.com]]></EventKey>
        </xml>""")

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'汪汪'


def test_location_event_handler():
    @werobot.location_event
    def location_event(message):
        return '位置喵喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[LOCATION]]></Event>
            <Latitude>23.137466</Latitude>
            <Longitude>113.352425</Longitude>
            <Precision>119.385040</Precision>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'位置喵喵'


def test_unknown_event():
    @werobot.unknown_event
    def unknown_event(message):
        return '不知道的事件喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[unknown]]></Event>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'不知道的事件喵'


def test_text():
    @werobot.text
    def text(message):
        return '普通的Text喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1348831860</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[this is a test]]></Content>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'普通的Text喵'


def test_image():
    @werobot.image
    def image(message):
        return '图片喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1348831860</CreateTime>
            <MsgType><![CDATA[image]]></MsgType>
            <PicUrl><![CDATA[this is a url]]></PicUrl>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'图片喵'


def test_location():
    @werobot.location
    def location(message):
        return '地理位置汪'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1351776360</CreateTime>
            <MsgType><![CDATA[location]]></MsgType>
            <Location_X>23.134521</Location_X>
            <Location_Y>113.358803</Location_Y>
            <Scale>20</Scale>
            <Label><![CDATA[Location]]></Label>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'地理位置汪'


def test_link():
    @werobot.link
    def link(message):
        return '链接喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1351776360</CreateTime>
            <MsgType><![CDATA[link]]></MsgType>
            <Title><![CDATA[WeRoBot]]></Title>
            <Description><![CDATA[Link to WeRoBot]]></Description>
            <Url><![CDATA[https://github.com/whtsky/WeRoBot]]></Url>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'链接喵'


def test_voice():
    @werobot.voice
    def voice(message):
        return '声音喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1357290913</CreateTime>
            <MsgType><![CDATA[voice]]></MsgType>
            <MediaId><![CDATA[media_id]]></MediaId>
            <Format><![CDATA[Format]]></Format>
            <Recognition><![CDATA[Meow~]]></Recognition>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'声音喵'


def test_video():
    @werobot.video
    def video():
        return '请收下这一段榴莲的视频'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1357290913</CreateTime>
            <MsgType><![CDATA[video]]></MsgType>
            <MediaId><![CDATA[media_id]]></MediaId>
            <ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>
            <MsgId>1234567890123456</MsgId>
            </xml>""")

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'请收下这一段榴莲的视频'


def test_shortvideo():
    @werobot.shortvideo
    def shortvideo():
        return '请收下这一段榴莲的小视频'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1357290913</CreateTime>
            <MsgType><![CDATA[shortvideo]]></MsgType>
            <MediaId><![CDATA[media_id]]></MediaId>
            <ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>
            <MsgId>1234567890123456</MsgId>
        </xml>
    """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'请收下这一段榴莲的小视频'


def test_user_scan_product():
    @werobot.user_scan_product
    def user_scan_product():
        return '打扰了'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[gh_4e47c9c9ecad]]></ToUserName>
            <FromUserName><![CDATA[okkeXs1nI-xU4ql8-5BXkv1f0gDo]]></FromUserName>
            <CreateTime>1438250110</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[user_scan_product]]></Event>
            <KeyStandard><![CDATA[ean13]]></KeyStandard>
            <KeyStr><![CDATA[6901481811083]]></KeyStr>
            <Country><![CDATA[中国]]></Country>
            <Province><![CDATA[广东]]></Province>
            <City><![CDATA[揭阳]]></City>
            <Sex>1</Sex>
            <Scene>2</Scene>
            <ExtInfo><![CDATA[123]]></ExtInfo>
        </xml>
    """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'打扰了'


def test_user_scan_product_enter_session():
    @werobot.user_scan_product_enter_session
    def user_scan_product_enter_session():
        return '再次打扰了'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[gh_fbe8a958756e]]></ToUserName>
            <FromUserName><![CDATA[otAzGjrS4AYCmeJM1GhEOcHXXTAo]]></FromUserName>
            <CreateTime>1433259128</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[user_scan_product_enter_session]]></Event>
            <KeyStandard><![CDATA[ena13]]></KeyStandard>
            <KeyStr><![CDATA[6954767461373]]></KeyStr>
            <ExtInfo><![CDATA[]]></ExtInfo>
        </xml>
    """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'再次打扰了'


def test_user_scan_product_async():
    @werobot.user_scan_product_async
    def user_scan_product_async():
        return '异步的地理位置喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[gh_fbe8a958756e]]></ToUserName>
            <FromUserName><![CDATA[otAzGjrS4AYCmeJM1GhEOcHXXTAo]]></FromUserName>
            <CreateTime>1434541327</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[user_scan_product_async]]></Event>
            <KeyStandard><![CDATA[qrcode]]></KeyStandard>
            <KeyStr><![CDATA[lincolntest2]]></KeyStr>
            <ExtInfo><![CDATA[123]]></ExtInfo>
            <RegionCode><![CDATA[440105]]></RegionCode>
        </xml>
    """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'异步的地理位置喵'


def test_user_scan_product_verify_action():
    @werobot.user_scan_product_verify_action
    def user_scan_product_verify_action():
        return '审核通过了喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[gh_404e58ec528e]]></ToUserName>
            <FromUserName><![CDATA[od_ikt8qi21-hVTtYgm8xSfTLH5w]]></FromUserName>
            <CreateTime>1450429257</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[user_scan_product_verify_action]]></Event>
            <KeyStandard><![CDATA[ean13]]></KeyStandard>
            <KeyStr><![CDATA[6901481811083]]></KeyStr>
            <Result><![CDATA[verify_ok]]></Result>
            <ReasonMsg><![CDATA[]]></ReasonMsg>
        </xml>
    """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'审核通过了喵'


def test_unknown():
    @werobot.unknown
    def unknown(message):
        return '不知道喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1351776360</CreateTime>
            <MsgType><![CDATA[unknown]]></MsgType>
            <Title><![CDATA[WeRoBot]]></Title>
            <Description><![CDATA[Link to WeRoBot]]></Description>
            <Url><![CDATA[https://github.com/whtsky/WeRoBot]]></Url>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'不知道喵'
