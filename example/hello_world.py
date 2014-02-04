import werobot

robot = werobot.WeRoBot(token='tokenhere')

@robot.text
def hello_world(message):
    return 'Hello World!'

robot.run()