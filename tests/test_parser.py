# -*- coding: utf-8 -*-

from werobot.parser import parse_user_msg


def test_none_message():
    assert not parse_user_msg("")


def test_text_message():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 1348831860
    assert message.type == "text"
    assert message.content == "this is a test"
    assert message.message_id == 1234567890123456


def test_image_message():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 1348831860
    assert message.type == "image"
    assert message.img == "this is a url"
    assert message.message_id == 1234567890123456


def test_location_message():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 1351776360
    assert message.type == "location"
    assert message.location == (23.134521, 113.358803)
    assert message.scale == 20
    assert message.label == "Location"
    assert message.message_id == 1234567890123456


def test_link_message():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 1351776360
    assert message.type == "link"
    assert message.title == "WeRoBot"
    assert message.description == "Link to WeRoBot"
    assert message.url == "https://github.com/whtsky/WeRoBot"
    assert message.message_id == 1234567890123456


def test_voice_message():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 1357290913
    assert message.type == "voice"
    assert message.media_id == "media_id"
    assert message.format == "Format"
    assert message.recognition == "Meow~"
    assert message.message_id == 1234567890123456


def test_unknown_message():
    xml = """
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
    message = parse_user_msg(xml)
    assert message.raw == xml
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 1351776360


def test_subscribe_event():
    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
    </xml>
    """)
    assert message.target == "toUser"
    assert message.source == "FromUser"
    assert message.time == 123456789
    assert message.type == "subscribe_event"

    message = parse_user_msg("""
    <xml><ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
        <EventKey><![CDATA[qrscene_123123]]></EventKey>
        <Ticket><![CDATA[TICKET]]></Ticket>
    </xml>
    """)
    assert message.target == "toUser"
    assert message.source == "FromUser"
    assert message.time == 123456789
    assert message.type == "subscribe_event"
    assert message.key == "qrscene_123123"
    assert message.ticket == "TICKET"


def test_unsubscribe_event():
    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[unsubscribe]]></Event>
    </xml>
    """)
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 123456789
    assert message.type == "unsubscribe_event"


def test_scan_event():
    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[SCAN]]></Event>
        <EventKey><![CDATA[SCENE_VALUE]]></EventKey>
        <Ticket><![CDATA[TICKET]]></Ticket>
    </xml>
    """)
    assert message.target == "toUser"
    assert message.source == "FromUser"
    assert message.time == 123456789
    assert message.type == "scan_event"
    assert message.key == "SCENE_VALUE"
    assert message.ticket == "TICKET"


def test_scan_push_event():
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
            <ScanResult><![CDATA[www.qq.com]]></ScanResult>
        </ScanCodeInfo>
    </xml>
    """)
    assert message.target == "toUser"
    assert message.source == "FromUser"
    assert message.time == 123456789
    assert message.type == "scancode_push_event"
    assert message.key == "EVENTKEY"
    assert message.scan_type == "qrcode"
    assert message.scan_result == "www.qq.com"


def test_scan_waitmsg_event():
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
            <ScanResult><![CDATA[www.qq.com]]></ScanResult>
        </ScanCodeInfo>
    </xml>
    """)
    assert message.target == "toUser"
    assert message.source == "FromUser"
    assert message.time == 123456789
    assert message.type == "scancode_waitmsg_event"
    assert message.key == "EVENTKEY"
    assert message.scan_type == "qrcode"
    assert message.scan_result == "www.qq.com"


def test_pic_sysphoto_event():
    # count is 1
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
    assert message.target == "gh_e136c6e50636"
    assert message.source == "oMgHVjngRipVsoxg6TuX3vz6glDg"
    assert message.time == 1408090651
    assert message.type == "pic_sysphoto_event"
    assert message.key == "6"
    assert message.count == 1
    assert message.pic_list == [{'pic_md5_sum': '1b5f7c23b5bf75682a53e7b6d163e185'}]

    # count is more than 1
    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[gh_e136c6e50636]]></ToUserName>
            <FromUserName><![CDATA[oMgHVjngRipVsoxg6TuX3vz6glDg]]></FromUserName>
            <CreateTime>1408090651</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[pic_sysphoto]]></Event>
            <EventKey><![CDATA[6]]></EventKey>
            <SendPicsInfo>
                <Count>2</Count>
                <PicList>
                    <item>
                        <PicMd5Sum><![CDATA[1b5f7c23b5bf75682a53e7b6d163e185]]></PicMd5Sum>
                    </item>
                    <item>
                        <PicMd5Sum><![CDATA[233]]></PicMd5Sum>
                    </item>
                </PicList>
            </SendPicsInfo>
        </xml>
        """)
    assert message.target == "gh_e136c6e50636"
    assert message.source == "oMgHVjngRipVsoxg6TuX3vz6glDg"
    assert message.time == 1408090651
    assert message.type == "pic_sysphoto_event"
    assert message.key == "6"
    assert message.count == 2
    assert message.pic_list == [
        {'pic_md5_sum': '1b5f7c23b5bf75682a53e7b6d163e185'}, {'pic_md5_sum': '233'}
    ]


def test_pic_photo_or_album_event():
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
    assert message.target == "gh_e136c6e50636"
    assert message.source == "oMgHVjngRipVsoxg6TuX3vz6glDg"
    assert message.time == 1408090816
    assert message.type == "pic_photo_or_album_event"
    assert message.key == "6"
    assert message.count == 1
    assert message.pic_list == [{'pic_md5_sum': '5a75aaca956d97be686719218f275c6b'}]


def test_pic_weixin_event():
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
    assert message.target == "gh_e136c6e50636"
    assert message.source == "oMgHVjngRipVsoxg6TuX3vz6glDg"
    assert message.time == 1408090816
    assert message.type == "pic_weixin_event"
    assert message.key == "6"
    assert message.count == 1
    assert message.pic_list == [{'pic_md5_sum': '5a75aaca956d97be686719218f275c6b'}]


def test_location_select_event():
    message = parse_user_msg(u"""
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
    assert message.target == "gh_e136c6e50636"
    assert message.source == "oMgHVjngRipVsoxg6TuX3vz6glDg"
    assert message.time == 1408091189
    assert message.type == "location_select_event"
    assert message.key == "6"
    assert message.location_x == "23"
    assert message.location_y == "113"
    assert message.scale == "15"
    assert message.label == u"广州市海珠区客村艺苑路 106号"
    assert message.poi_name is None


def test_click_event():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 123456789
    assert message.type == "click_event"
    assert message.key == "EVENTKEY"


def test_view_event():
    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[VIEW]]></Event>
        <EventKey><![CDATA[www.qq.com]]></EventKey>
    </xml>""")
    assert message.target == "toUser"
    assert message.source == "FromUser"
    assert message.time == 123456789
    assert message.type == "view_event"
    assert message.key == "www.qq.com"


def test_location_event():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 123456789
    assert message.type == "location_event"
    assert message.latitude == 23.137466
    assert message.longitude == 113.352425
    assert message.precision == 119.385040


def test_template_send_job_finish_event():
    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[gh_7f083739789a]]></ToUserName>
        <FromUserName><![CDATA[oia2TjuEGTNoeX76QEjQNrcURxG8]]></FromUserName>
        <CreateTime>1395658920</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[TEMPLATESENDJOBFINISH]]></Event>
        <MsgID>200163836</MsgID>
        <Status><![CDATA[success]]></Status>
    </xml>
    """)
    assert message.message_id == 200163836
    assert message.status == 'success'

    assert parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[gh_7f083739789a]]></ToUserName>
        <FromUserName><![CDATA[oia2TjuEGTNoeX76QEjQNrcURxG8]]></FromUserName>
        <CreateTime>1395658984</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[TEMPLATESENDJOBFINISH]]></Event>
        <MsgID>200163840</MsgID>
        <Status><![CDATA[failed: system failed]]></Status>
    </xml>
    """).status == 'failed: system failed'


def test_user_scan_product_event():
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
    assert message.target == "gh_4e47c9c9ecad"
    assert message.source == "okkeXs1nI-xU4ql8-5BXkv1f0gDo"
    assert message.time == 1438250110
    assert message.type == "user_scan_product_event"
    assert message.key_standard == "ean13"
    assert message.key_str == "6901481811083"
    assert message.country == u"中国"
    assert message.province == u"广东"
    assert message.city == u"揭阳"
    assert message.sex == 1
    assert message.scene == 2
    assert message.ext_info == "123"


def test_user_scan_product_enter_session_event():
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
    assert message.target == "gh_fbe8a958756e"
    assert message.source == "otAzGjrS4AYCmeJM1GhEOcHXXTAo"
    assert message.time == 1433259128
    assert message.type == "user_scan_product_enter_session_event"
    assert message.key_standard == "ena13"
    assert message.key_str == "6954767461373"
    assert message.ext_info is None


def test_user_scan_product_async_event():
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
    assert message.target == "gh_fbe8a958756e"
    assert message.source == "otAzGjrS4AYCmeJM1GhEOcHXXTAo"
    assert message.time == 1434541327
    assert message.type == "user_scan_product_async_event"
    assert message.key_standard == "qrcode"
    assert message.key_str == "lincolntest2"
    assert message.ext_info == "123"
    assert message.region_code == "440105"


def test_user_scan_product_verify_action_event():
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
    assert message.target == "gh_404e58ec528e"
    assert message.source == "od_ikt8qi21-hVTtYgm8xSfTLH5w"
    assert message.time == 1450429257
    assert message.type == "user_scan_product_verify_action_event"
    assert message.key_standard == "ean13"
    assert message.key_str == "6901481811083"
    assert message.result == "verify_ok"
    assert message.reason_msg is None


def test_unknown_event():
    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[unknown]]></Event>
    </xml>
    """)
    assert message.target == "toUser"
    assert message.source == "FromUser"
    assert message.time == 123456789
    assert message.type == "unknown_event"
