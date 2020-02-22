# -*- coding: utf-8 -*-

from werobot.messages.entries import StringEntry, IntEntry, FloatEntry
from werobot.messages.base import WeRoBotMetaClass


class EventMetaClass(WeRoBotMetaClass):
    pass


class WeChatEvent(object, metaclass=EventMetaClass):
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
                {
                    'pic_md5_sum': message['SendPicsInfo']
                    ['PicList'].pop('item')['PicMd5Sum']
                }
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


class BaseCardCheckEvent(WeChatEvent):
    card_id = StringEntry('CardId')
    refuse_reason = StringEntry('RefuseReason')


class CardPassCheckEvent(BaseCardCheckEvent):
    __type__ = 'card_pass_check_event'


class CardNotPassCheckEvent(BaseCardCheckEvent):
    __type__ = 'card_not_pass_check_event'


class BaseCardEvent(WeChatEvent):
    card_id = StringEntry('CardId')
    user_card_code = StringEntry('UserCardCode')


class UserGetCardEvent(BaseCardEvent):
    __type__ = 'user_get_card_event'
    is_give_by_friend = IntEntry('IsGiveByFriend')
    friend_user_name = StringEntry('FriendUserName')
    outer_id = IntEntry('OuterId')
    old_user_card_code = StringEntry('OldUserCardCode')
    outer_str = StringEntry('OuterStr')
    is_restore_member_card = IntEntry('IsRestoreMemberCard')
    is_recommend_by_friend = IntEntry('IsRecommendByFriend')


class UserGiftingCardEvent(BaseCardEvent):
    __type__ = 'user_gifting_card_event'
    is_return_back = IntEntry('IsReturnBack')
    friend_user_name = StringEntry('FriendUserName')
    is_chat_room = IntEntry('IsChatRoom')


class UserDelCardEvent(BaseCardEvent):
    __type__ = 'user_del_card_event'


class UserConsumeCardEvent(BaseCardEvent):
    __type__ = 'user_consume_card_event'
    consume_source = StringEntry('ConsumeSource')
    location_name = StringEntry('LocationName')
    staff_open_id = StringEntry('StaffOpenId')
    verify_code = StringEntry('VerifyCode')
    remark_amount = StringEntry('RemarkAmount')
    outer_str = StringEntry('OuterStr')


class UserPayFromPayCellEvent(BaseCardEvent):
    __type__ = 'user_pay_from_pay_cell_event'
    trans_id = StringEntry('TransId')
    location_id = IntEntry('LocationId')
    fee = StringEntry('Fee')
    original_fee = StringEntry('OriginalFee')


class UserViewCardEvent(BaseCardEvent):
    __type__ = 'user_view_card_event'
    outer_str = StringEntry('OuterStr')


class UserEnterSessionFromCardEvent(BaseCardEvent):
    __type__ = 'user_enter_session_from_card_event'


class UpdateMemberCardEvent(BaseCardEvent):
    __type__ = 'update_member_card_event'
    modify_bonus = IntEntry('ModifyBonus')
    modify_balance = IntEntry('ModifyBalance')


class CardSkuRemindEvent(WeChatEvent):
    __type__ = 'card_sku_remind_event'
    card_id = StringEntry('CardId')
    detail = StringEntry('Detail')


class CardPayOrderEvent(WeChatEvent):
    __type__ = 'card_pay_order_event'
    order_id = StringEntry('OrderId')
    status = StringEntry('Status')
    create_order_time = IntEntry('CreateOrderTime')
    pay_finish_time = IntEntry('PayFinishTime')
    desc = StringEntry('Desc')
    free_coin_count = StringEntry('FreeCoinCount')
    pay_coin_count = StringEntry('PayCoinCount')
    refund_free_coin_count = StringEntry('RefundFreeCoinCount')
    refund_pay_coin_count = StringEntry('RefundPayCoinCount')
    order_type = StringEntry('OrderType')
    memo = StringEntry('Memo')
    receipt_info = StringEntry('ReceiptInfo')


class SubmitMembercardUserInfoEvent(BaseCardEvent):
    __type__ = 'submit_membercard_user_info_event'


class UnknownEvent(WeChatEvent):
    __type__ = 'unknown_event'
