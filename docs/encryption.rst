消息加解密
==========

WeRoBot 支持对消息的加解密，即微信公众号的安全模式。
为 WeRoBot 开启消息加密功能，首先需要安装 ``cryptography`` ::

    pip install cryptography

之后， 你只需要将你在微信公众平台后台设置的 `EncodingAESKey` 加到 WeRoBot 的 :ref:`Config` 里面就可以了 ::

    from werobot import WeRoBot
    robot = WeRoBot()
    robot.config['ENCODING_AES_KEY'] = 'Your Encoding AES Key'

WeRoBot 之后会自动进行消息的加解密工作。
