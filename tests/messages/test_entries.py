from werobot.messages.entries import get_value


class FakeIntance:
    pass


def test_get_value():
    instance = FakeIntance()
    instance.b = 6
    instance.a = {'c': 'd'}
    assert get_value(instance, 'd', 'default') == 'default'
    assert get_value(instance, 'b', 'default') == 6
    assert get_value(instance, 'a.c') == 'd'
