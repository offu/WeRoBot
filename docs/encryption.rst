消息加解密
==========

WeRoBot 支持对消息的加解密，即微信公众号的安全模式。
在开启消息加解密功能之前，请先阅读微信官方的 `消息加解密说明 <https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1434696670>`_
为 WeRoBot 开启消息加密功能，首先需要安装 ``cryptography`` ::

    pip install cryptography

之后， 你只需要将开发者 ID(`AppID`) 和微信公众平台后台设置的 `EncodingAESKey` 加到 WeRoBot 的 :ref:`Config` 里面就可以了 ::

    from werobot import WeRoBot
    robot = WeRoBot()
    robot.config["APP_ID"] = "Your AppID"
    robot.config['ENCODING_AES_KEY'] = 'Your Encoding AES Key'

WeRoBot 之后会自动进行消息的加解密工作。
