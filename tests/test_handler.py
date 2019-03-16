# -*- coding: utf-8 -*-

from werobot import WeRoBot
from werobot.parser import parse_user_msg
from werobot.replies import TextReply
import os

werobot = WeRoBot(SESSION_STORAGE=False)


def teardown_module(module):
    try:
        os.remove(os.path.abspath("werobot_session"))
    except OSError:
        pass


def test_subscribe_handler():
    @werobot.subscribe
    def subscribe(message):
        return '关注'

    message = parse_user_msg(
        """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[subscribe]]></Event>
        </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'关注'


def test_unsubscribe_handler():
    @werobot.unsubscribe
    def unsubscribe(message):
        return '取消关注'

    message = parse_user_msg(
        """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[unsubscribe]]></Event>
        </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'取消关注'


def test_scan_push_handler():
    @werobot.scancode_push
    def scancode_push(message):
        return '扫描推送'

    message = parse_user_msg(
        """
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
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'扫描推送'


def test_scan_waitmsg_handler():
    @werobot.scancode_waitmsg
    def scancode_waitmsg(message):
        return '扫描弹消息'

    message = parse_user_msg(
        """
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
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'扫描弹消息'


def test_pic_sysphoto_handler():
    @werobot.pic_sysphoto
    def pic_sysphoto():
        return '瞧一瞧系统拍照'

    message = parse_user_msg(
        """
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
    """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'瞧一瞧系统拍照'


def test_pic_photo_or_album_handler():
    @werobot.pic_photo_or_album
    def pic_photo_or_album():
        return '瞧一瞧拍照或者相册'

    message = parse_user_msg(
        """
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
    """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'瞧一瞧拍照或者相册'


def test_pic_weixin_handler():
    @werobot.pic_weixin
    def pic_weixin():
        return '瞧一瞧微信相册'

    message = parse_user_msg(
        """
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
    """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'瞧一瞧微信相册'


def test_location_select_handler():
    @werobot.location_select
    def location_select():
        return '瞧一瞧地理位置'

    message = parse_user_msg(
        """
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
    """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'瞧一瞧地理位置'


def test_click_handler():
    @werobot.click
    def scan(message):
        return '喵喵'

    message = parse_user_msg(
        """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[CLICK]]></Event>
            <EventKey><![CDATA[EVENTKEY]]></EventKey>
        </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'喵喵'


def test_view_handler():
    @werobot.view
    def view(message):
        return '汪汪'

    message = parse_user_msg(
        """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[VIEW]]></Event>
            <EventKey><![CDATA[www.qq.com]]></EventKey>
        </xml>"""
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'汪汪'


def test_location_event_handler():
    @werobot.location_event
    def location_event(message):
        return '位置喵喵'

    message = parse_user_msg(
        """
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
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'位置喵喵'


def test_card_pass_check_handler():
    @werobot.card_pass_check
    def card_pass_check():
        return '瞧一瞧通过了'

    message = parse_user_msg(
        """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[card_pass_check]]></Event>
            <CardId><![CDATA[cardid]]></CardId>
            <RefuseReason><![CDATA[非法代制]]></RefuseReason>
        </xml>
    """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'瞧一瞧通过了'


def test_card_not_pass_check_handler():
    @werobot.card_not_pass_check
    def card_pass_not_check():
        return '瞧一瞧没过'

    message = parse_user_msg(
        """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[card_not_pass_check]]></Event>
            <CardId><![CDATA[cardid]]></CardId>
            <RefuseReason><![CDATA[非法代制]]></RefuseReason>
        </xml>
    """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'瞧一瞧没过'


def test_user_get_card_handler():
    @werobot.user_get_card
    def user_get_card():
        return '恭喜入坑'

    message = parse_user_msg(
        """
            <xml>
                <ToUserName> <![CDATA[gh_fc0a06a20993]]> </ToUserName>
                <FromUserName> <![CDATA[oZI8Fj040-be6rlDohc6gkoPOQTQ]]> </FromUserName>
                <CreateTime>1472551036</CreateTime>
                <MsgType> <![CDATA[event]]> </MsgType>
                <Event> <![CDATA[user_get_card]]> </Event>
                <CardId> <![CDATA[pZI8Fjwsy5fVPRBeD78J4RmqVvBc]]> </CardId>
                <IsGiveByFriend>0</IsGiveByFriend>
                <UserCardCode> <![CDATA[226009850808]]> </UserCardCode>
                <FriendUserName> <![CDATA[]]> </FriendUserName>
                <OuterId>0</OuterId>
                <OldUserCardCode> <![CDATA[]]> </OldUserCardCode>
                <OuterStr> <![CDATA[12b]]> </OuterStr>
                <IsRestoreMemberCard>0</IsRestoreMemberCard>
                <IsRecommendByFriend>0</IsRecommendByFriend>
            </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'恭喜入坑'


def test_user_gifting_card_handler():
    @werobot.user_gifting_card
    def user_gifting_card():
        return '锅从天上来'

    message = parse_user_msg(
        """
            <xml>
                <ToUserName><![CDATA[gh_3fcea188bf78]]></ToUserName>
                <FromUserName><![CDATA[obLatjjwDolFjRRd3doGIdwNqRXw]]></FromUserName>
                <CreateTime>1474181868</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[user_gifting_card]]></Event>
                <CardId><![CDATA[pbLatjhU-3pik3d4PsbVzvBxZvJc]]></CardId>
                <UserCardCode><![CDATA[297466945104]]></UserCardCode>
                <IsReturnBack>0</IsReturnBack>
                <FriendUserName><![CDATA[obLatjlNerkb62HtSdQUx66C4NTU]]></FriendUserName>
                <IsChatRoom>0</IsChatRoom>
            </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'锅从天上来'


def test_user_del_card_handler():
    @werobot.user_del_card
    def user_del_card():
        return '摆脱负担'

    message = parse_user_msg(
        """
            <xml>
                <ToUserName><![CDATA[toUser]]></ToUserName>
                <FromUserName><![CDATA[FromUser]]></FromUserName>
                <CreateTime>123456789</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[user_del_card]]></Event>
                <CardId><![CDATA[cardid]]></CardId>
                <UserCardCode><![CDATA[12312312]]></UserCardCode>
            </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'摆脱负担'


def test_user_consume_card_handler():
    @werobot.user_consume_card
    def user_consume_card():
        return '恭喜脱坑'

    message = parse_user_msg(
        """
            <xml>
                <ToUserName> <![CDATA[gh_fc0a06a20993]]> </ToUserName>
                <FromUserName> <![CDATA[oZI8Fj040-be6rlDohc6gkoPOQTQ]]> </FromUserName>
                <CreateTime>1472549042</CreateTime>
                <MsgType> <![CDATA[event]]> </MsgType>
                <Event> <![CDATA[user_consume_card]]> </Event>
                <CardId> <![CDATA[pZI8Fj8y-E8hpvho2d1ZvpGwQBvA]]> </CardId>
                <UserCardCode> <![CDATA[452998530302]]> </UserCardCode>
                <ConsumeSource> <![CDATA[FROM_API]]> </ConsumeSource>
                <LocationName> <![CDATA[]]> </LocationName>
                <StaffOpenId> <![CDATA[oZ********nJ3bPJu_Rtjkw4c]]> </StaffOpenId>
                <VerifyCode> <![CDATA[]]> </VerifyCode>
                <RemarkAmount> <![CDATA[]]> </RemarkAmount>
                <OuterStr> <![CDATA[xxxxx]]> </OuterStr>
            </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'恭喜脱坑'


def test_user_pay_from_pay_cell_handler():
    @werobot.user_pay_from_pay_cell
    def user_pay_from_pay_cell():
        return '冲动消费'

    message = parse_user_msg(
        """
            <xml>
                <ToUserName><![CDATA[gh_e2243xxxxxxx]]></ToUserName>
                <FromUserName><![CDATA[oo2VNuOUuZGMxxxxxxxx]]></FromUserName>
                <CreateTime>1442390947</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[user_pay_from_pay_cell]]></Event>
                <CardId><![CDATA[po2VNuCuRo-8sxxxxxxxxxxx]]></CardId>
                <UserCardCode><![CDATA[38050000000]]></UserCardCode>
                <TransId><![CDATA[10022403432015000000000]]></TransId>
                <LocationId>291710000</LocationId>
                <Fee><![CDATA[10000]]></Fee>
                <OriginalFee><![CDATA[10000]]> </OriginalFee>
            </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'冲动消费'


def test_user_view_card_handler():
    @werobot.user_view_card
    def user_view_card():
        return '我就瞧一瞧，不买'

    message = parse_user_msg(
        """
            <xml>
                <ToUserName> <![CDATA[gh_fcxxxx6a20993]]> </ToUserName>
                <FromUserName> <![CDATA[oZI8Fj040-xxxxx6gkoPOQTQ]]> </FromUserName>
                <CreateTime>1467811138</CreateTime>
                <MsgType> <![CDATA[event]]> </MsgType>
                <Event> <![CDATA[user_view_card]]> </Event>
                <CardId> <![CDATA[pZI8Fj2ezBbxxxxxT2UbiiWLb7Bg]]> </CardId>
                <UserCardCode> <![CDATA[4xxxxxxxx8558]]> </UserCardCode>
                <OuterStr> <![CDATA[12b]]> </OuterStr>
            </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'我就瞧一瞧，不买'


def test_user_enter_session_from_card_handler():
    @werobot.user_enter_session_from_card
    def user_enter_session_from_card():
        return '退货是不可能退货的'

    message = parse_user_msg(
        """
            <xml>
                <ToUserName><![CDATA[toUser]]></ToUserName>
                <FromUserName><![CDATA[FromUser]]></FromUserName>
                <CreateTime>123456789</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[user_enter_session_from_card]]></Event>
                <CardId><![CDATA[cardid]]></CardId>
                <UserCardCode><![CDATA[12312312]]></UserCardCode>
            </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'退货是不可能退货的'


def test_update_member_card_handler():
    @werobot.update_member_card
    def update_member_card():
        return '冲动消费导致余额减少'

    message = parse_user_msg(
        """
            <xml>
                <ToUserName><![CDATA[gh_9e1765b5568e]]></ToUserName>
                <FromUserName><![CDATA[ojZ8YtyVyr30HheH3CM73y7h4jJE]]></FromUserName>
                <CreateTime>1445507140</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[update_member_card]]></Event>
                <CardId><![CDATA[pjZ8Ytx-nwvpCRyQneH3Ncmh6N94]]></CardId>
                <UserCardCode><![CDATA[485027611252]]></UserCardCode>
                <ModifyBonus>3</ModifyBonus>
                <ModifyBalance>0</ModifyBalance>
            </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'冲动消费导致余额减少'


def test_card_sku_remind_handler():
    @werobot.card_sku_remind
    def card_sku_remind():
        return '骗钱大成功'

    message = parse_user_msg(
        """
            <xml>
                <ToUserName><![CDATA[gh_2d62d*****0]]></ToUserName>
                <FromUserName><![CDATA[oa3LFuBvWb7*********]]></FromUserName>
                <CreateTime>1443838506</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[card_sku_remind]]></Event>
                <CardId><![CDATA[pa3LFuAh2P65**********]]></CardId>
                <Detail><![CDATA[the card's quantity is equal to 0]]></Detail>
            </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'骗钱大成功'


def test_card_pay_order_handler():
    @werobot.card_pay_order
    def card_pay_order():
        return '冲动消费的凭证'

    message = parse_user_msg(
        """
            <xml>
                <ToUserName><![CDATA[gh_7223c83d4be5]]></ToUserName>
                <FromUserName><![CDATA[ob5E7s-HoN9tslQY3-0I4qmgluHk]]></FromUserName>
                <CreateTime>1453295737</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[card_pay_order]]></Event>
                <OrderId><![CDATA[404091456]]></OrderId>
                <Status><![CDATA[ORDER_STATUS_FINANCE_SUCC]]></Status>
                <CreateOrderTime>1453295737</CreateOrderTime>
                <PayFinishTime>0</PayFinishTime>
                <Desc><![CDATA[]]></Desc>
                <FreeCoinCount><![CDATA[200]]></FreeCoinCount>
                <PayCoinCount><![CDATA[0]]></PayCoinCount>
                <RefundFreeCoinCount><![CDATA[0]]></RefundFreeCoinCount>
                <RefundPayCoinCount><![CDATA[0]]></RefundPayCoinCount>
                <OrderType><![CDATA[ORDER_TYPE_SYS_ADD]]></OrderType>
                <Memo><![CDATA[开通账户奖励]]></Memo>
                <ReceiptInfo><![CDATA[]]></ReceiptInfo>
            </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'冲动消费的凭证'


def test_submit_membercard_user_info_handler():
    @werobot.submit_membercard_user_info
    def submit_membercard_user_info():
        return '现在醒一醒还来得及'

    message = parse_user_msg(
        """
            <xml>
                <ToUserName> <![CDATA[gh_3fcea188bf78]]></ToUserName>
                <FromUserName><![CDATA[obLatjlaNQKb8FqOvt1M1x1lIBFE]]></FromUserName>
                <CreateTime>1432668700</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[submit_membercard_user_info]]></Event>
                <CardId><![CDATA[pbLatjtZ7v1BG_ZnTjbW85GYc_E8]]></CardId>
                <UserCardCode><![CDATA[018255396048]]></UserCardCode>
            </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'现在醒一醒还来得及'


def test_unknown_event():
    @werobot.unknown_event
    def unknown_event(message):
        return '不知道的事件喵'

    message = parse_user_msg(
        """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[unknown]]></Event>
        </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'不知道的事件喵'


def test_text():
    @werobot.text
    def text(message):
        return '普通的Text喵'

    message = parse_user_msg(
        """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1348831860</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[this is a test]]></Content>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'普通的Text喵'


def test_image():
    @werobot.image
    def image(message):
        return '图片喵'

    message = parse_user_msg(
        """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1348831860</CreateTime>
            <MsgType><![CDATA[image]]></MsgType>
            <PicUrl><![CDATA[this is a url]]></PicUrl>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'图片喵'


def test_location():
    @werobot.location
    def location(message):
        return '地理位置汪'

    message = parse_user_msg(
        """
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
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'地理位置汪'


def test_link():
    @werobot.link
    def link(message):
        return '链接喵'

    message = parse_user_msg(
        """
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
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'链接喵'


def test_voice():
    @werobot.voice
    def voice(message):
        return '声音喵'

    message = parse_user_msg(
        """
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
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'声音喵'


def test_video():
    @werobot.video
    def video():
        return '请收下这一段榴莲的视频'

    message = parse_user_msg(
        """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1357290913</CreateTime>
            <MsgType><![CDATA[video]]></MsgType>
            <MediaId><![CDATA[media_id]]></MediaId>
            <ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>
            <MsgId>1234567890123456</MsgId>
            </xml>"""
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'请收下这一段榴莲的视频'


def test_shortvideo():
    @werobot.shortvideo
    def shortvideo():
        return '请收下这一段榴莲的小视频'

    message = parse_user_msg(
        """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1357290913</CreateTime>
            <MsgType><![CDATA[shortvideo]]></MsgType>
            <MediaId><![CDATA[media_id]]></MediaId>
            <ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>
            <MsgId>1234567890123456</MsgId>
        </xml>
    """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'请收下这一段榴莲的小视频'


def test_user_scan_product():
    @werobot.user_scan_product
    def user_scan_product():
        return '打扰了'

    message = parse_user_msg(
        """
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
    """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'打扰了'


def test_user_scan_product_enter_session():
    @werobot.user_scan_product_enter_session
    def user_scan_product_enter_session():
        return '再次打扰了'

    message = parse_user_msg(
        """
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
    """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'再次打扰了'


def test_user_scan_product_async():
    @werobot.user_scan_product_async
    def user_scan_product_async():
        return '异步的地理位置喵'

    message = parse_user_msg(
        """
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
    """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'异步的地理位置喵'


def test_user_scan_product_verify_action():
    @werobot.user_scan_product_verify_action
    def user_scan_product_verify_action():
        return '审核通过了喵'

    message = parse_user_msg(
        """
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
    """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'审核通过了喵'


def test_unknown():
    @werobot.unknown
    def unknown(message):
        return '不知道喵'

    message = parse_user_msg(
        """
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
        """
    )

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'不知道喵'
