#WeRoBot

[![Build Status](https://travis-ci.org/whtsky/WeRoBot.png)](https://travis-ci.org/whtsky/WeRoBot)
[![Coverage Status](https://coveralls.io/repos/whtsky/WeRoBot/badge.png)](https://coveralls.io/r/whtsky/WeRoBot)


WeRoBot 是一个微信机器人框架，采用MIT协议发布。

文档在这里：https://werobot.readthedocs.org/en/latest/

##安装
```bash
pip install werobot
```

##Hello World
```python
import werobot

robot = werobot.WeRoBot(token='tokenhere')

@robot.handler
def echo(message):
    return 'Hello World!'

robot.run()
```
