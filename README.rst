====================================
WeRoBot
====================================

.. image:: https://img.shields.io/travis/offu/WeRoBot/master.svg?maxAge=3600&label=macOS
    :target: https://travis-ci.org/offu/WeRoBot
.. image:: https://img.shields.io/appveyor/ci/whtsky/WeRoBot/master.svg?maxAge=3600&label=Windows
    :target: https://ci.appveyor.com/project/whtsky/WeRoBot
.. image:: https://img.shields.io/circleci/project/github/offu/WeRoBot.svg
    :target: https://circleci.com/gh/offu/WeRoBot
.. image:: https://codecov.io/gh/offu/WeRoBot/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/offu/WeRoBot
.. image:: https://img.shields.io/badge/QQ%20Group-283206829-brightgreen.svg?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTc5MiIgaGVpZ2h0PSIxNzkyIiB2aWV3Qm94PSIwIDAgMTc5MiAxNzkyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0yNzAgODA2cS04LTE5LTgtNTIgMC0yMCAxMS00OXQyNC00NXEtMS0yMiA3LjUtNTN0MjIuNS00M3EwLTEzOSA5Mi41LTI4OC41dDIxNy41LTIwOS41cTEzOS02NiAzMjQtNjYgMTMzIDAgMjY2IDU1IDQ5IDIxIDkwIDQ4dDcxIDU2IDU1IDY4IDQyIDc0IDMyLjUgODQuNSAyNS41IDg5LjUgMjIgOThsMSA1cTU1IDgzIDU1IDE1MCAwIDE0LTkgNDB0LTkgMzhxMCAxIDEuNSAzLjV0My41IDUgMiAzLjVxNzcgMTE0IDEyMC41IDIxNC41dDQzLjUgMjA4LjVxMCA0My0xOS41IDEwMHQtNTUuNSA1N3EtOSAwLTE5LjUtNy41dC0xOS0xNy41LTE5LTI2LTE2LTI2LjUtMTMuNS0yNi05LTE3LjVxLTEtMS0zLTFsLTUgNHEtNTkgMTU0LTEzMiAyMjMgMjAgMjAgNjEuNSAzOC41dDY5IDQxLjUgMzUuNSA2NXEtMiA0LTQgMTZ0LTcgMThxLTY0IDk3LTMwMiA5Ny01MyAwLTExMC41LTl0LTk4LTIwLTEwNC41LTMwcS0xNS01LTIzLTctMTQtNC00Ni00LjV0LTQwLTEuNXEtNDEgNDUtMTI3LjUgNjV0LTE2OC41IDIwcS0zNSAwLTY5LTEuNXQtOTMtOS0xMDEtMjAuNS03NC41LTQwLTMyLjUtNjRxMC00MCAxMC01OS41dDQxLTQ4LjVxMTEtMiA0MC41LTEzdDQ5LjUtMTJxNCAwIDE0LTIgMi0yIDItNGwtMi0zcS00OC0xMS0xMDgtMTA1LjV0LTczLTE1Ni41bC01LTNxLTQgMC0xMiAyMC0xOCA0MS01NC41IDc0LjV0LTc3LjUgMzcuNWgtMXEtNCAwLTYtNC41dC01LTUuNXEtMjMtNTQtMjMtMTAwIDAtMjc1IDI1Mi00NjZ6IiBmaWxsPSIjZmZmIi8%2BPC9zdmc%2B
    :target: https://jq.qq.com/?_wv=1027&k=449sXsV
.. image:: https://opencollective.com/werobot/backers/badge.svg
    :target: https://opencollective.com/werobot
    :alt: Backers on Open Collective
..  image:: https://opencollective.com/werobot/sponsors/badge.svg
    :target: https://opencollective.com/werobot
    :alt: Sponsors on Open Collective

WeRoBot 是一个微信公众号开发框架，采用MIT协议发布。

文档在这里： https://werobot.readthedocs.org/zh_CN/latest/

安装
========

推荐使用 pip 进行安装 ::

    pip install werobot

Hello World
=============

一个非常简单的 Hello World 微信公众号，会对收到的所有文本消息回复 Hello World ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.text
    def hello_world():
        return 'Hello World!'

    robot.run()
    
Credits 
=======
Contributors
-----------------
Thank you to all the people who have already contributed. 
|occontributorimage|

Backers
-----------------
Thank you to all our backers! 
|ocbackerimage|

Sponsors
-----------------
Support this project by becoming a sponsor. Your logo will show up here with a link to your website. `become_sponsor`_

|ocsponsor0| |ocsponsor1| |ocsponsor2|

.. |ocbackerimage| image:: https://opencollective.com/werobot/backers.svg?width=890
    :target: https://opencollective.com/werobot
    :alt: Backers on Open Collective
.. |occontributorimage| image:: https://opencollective.com/werobot/contributors.svg?width=890&button=false
    :target: https://opencollective.com/werobot
    :alt: Repo Contributors

.. _become_sponsor: https://opencollective.com/werobot#sponsor

.. |ocsponsor0| image:: https://opencollective.com/werobot/sponsor/0/avatar.svg
    :target: https://opencollective.com/werobot/sponsor/0/website
    :alt: Sponsor
.. |ocsponsor1| image:: https://opencollective.com/werobot/sponsor/1/avatar.svg
    :target: https://opencollective.com/werobot/sponsor/1/website
    :alt: Sponsor
.. |ocsponsor2| image:: https://opencollective.com/werobot/sponsor/2/avatar.svg
    :target: https://opencollective.com/werobot/sponsor/2/website
    :alt: Sponsor

