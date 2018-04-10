# -*- coding: utf-8 -*-

import six
from werobot.messages.entries import StringEntry, IntEntry, FloatEntry
from werobot.messages.base import WeRoBotMetaClass


class EventMetaClass(WeRoBotMetaClass):
    pass


@six.add_metaclass(EventMetaClass)
class WeChatEvent(object):
    target = StringEntry('ToUserName')
    source = StringEntry('FromUserName')
    time = IntEntry('CreateTime')
    message_id = IntEntry('MsgID', 0)

    def __init__(self, message):
        self.__dict__.update(message)


class SimpleEvent(WeChatEvent):
    key = StringEntry('EventKey')


class TicketEvent(WeChatEvent):
    key = StringEntry('EventKey')
    ticket = StringEntry('Ticket')


class SubscribeEvent(TicketEvent):
    __type__ = 'subscribe_event'


class UnSubscribeEvent(WeChatEvent):
    __type__ = 'unsubscribe_event'


class ScanEvent(TicketEvent):
    __type__ = 'scan_event'


class ScanCodePushEvent(SimpleEvent):
    __type__ = 'scancode_push_event'
    scan_type = StringEntry('ScanCodeInfo.ScanType')
    scan_result = StringEntry('ScanCodeInfo.ScanResult')


class ScanCodeWaitMsgEvent(ScanCodePushEvent):
    __type__ = 'scancode_waitmsg_event'
    scan_type = StringEntry('ScanCodeInfo.ScanType')
    scan_result = StringEntry('ScanCodeInfo.ScanResult')


class BasePicEvent(SimpleEvent):
    count = IntEntry('SendPicsInfo.Count')

    def __init__(self, message):
        super(BasePicEvent, self).__init__(message)
        self.pic_list = list()
        if self.count > 1:
            for item in message['SendPicsInfo']['PicList'].pop('item'):
                self.pic_list.append({'pic_md5_sum': item['PicMd5Sum']})
        else:
            self.pic_list.append(
                {'pic_md5_sum': message['SendPicsInfo']['PicList'].pop('item')['PicMd5Sum']}
            )


class PicSysphotoEvent(BasePicEvent):
    __type__ = 'pic_sysphoto_event'


class PicPhotoOrAlbumEvent(BasePicEvent):
    __type__ = 'pic_photo_or_album_event'


class PicWeixinEvent(BasePicEvent):
    __type__ = 'pic_weixin_event'


class LocationSelectEvent(SimpleEvent):
    __type__ = 'location_select_event'
    location_x = StringEntry('SendLocationInfo.Location_X')
    location_y = StringEntry('SendLocationInfo.Location_Y')
    scale = StringEntry('SendLocationInfo.Scale')
    label = StringEntry('SendLocationInfo.Label')
    poi_name = StringEntry('SendLocationInfo.Poiname')


class ClickEvent(SimpleEvent):
    __type__ = 'click_event'


class ViewEvent(SimpleEvent):
    __type__ = 'view_event'


class LocationEvent(WeChatEvent):
    __type__ = 'location_event'
    latitude = FloatEntry('Latitude')
    longitude = FloatEntry('Longitude')
    precision = FloatEntry('Precision')


class TemplateSendJobFinishEvent(WeChatEvent):
    __type__ = 'templatesendjobfinish_event'
    status = StringEntry('Status')


class BaseProductEvent(WeChatEvent):
    key_standard = StringEntry('KeyStandard')
    key_str = StringEntry('KeyStr')
    ext_info = StringEntry('ExtInfo')


class UserScanProductEvent(BaseProductEvent):
    __type__ = 'user_scan_product_event'
    country = StringEntry('Country')
    province = StringEntry('Province')
    city = StringEntry('City')
    sex = IntEntry('Sex')
    scene = IntEntry('Scene')


class UserScanProductEnterSessionEvent(BaseProductEvent):
    __type__ = 'user_scan_product_enter_session_event'


class UserScanProductAsyncEvent(BaseProductEvent):
    __type__ = 'user_scan_product_async_event'
    region_code = StringEntry('RegionCode')


class UserScanProductVerifyActionEvent(WeChatEvent):
    __type__ = 'user_scan_product_verify_action_event'
    key_standard = StringEntry('KeyStandard')
    key_str = StringEntry('KeyStr')
    result = StringEntry('Result')
    reason_msg = StringEntry('ReasonMsg')


class UnknownEvent(WeChatEvent):
    __type__ = 'unknown_event'
