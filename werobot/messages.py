class WeChatMessage(object):
    pass


class TextMessage(WeChatMessage):
    def __init__(self, touser, fromuser, create_at, content):
        self.target = touser
        self.source = fromuser
        self.time = int(create_at)
        self.content = content


class ImageMessage(WeChatMessage):
    def __init__(self, touser, fromuser, create_at, img):
        self.target = touser
        self.source = fromuser
        self.time = int(create_at)
        self.img = img


class LocationMessage(WeChatMessage):
    def __init__(self, touser, fromuser, create_at,
                 location_x, location_y, scale, label):
        self.target = touser
        self.source = fromuser
        self.time = create_at
        self.location = (location_x, location_y)
        self.scale = scale
        self.label = label
