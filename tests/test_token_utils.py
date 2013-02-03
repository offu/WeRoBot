from werobot.utils import generate_token, check_token


def test_token_generator():
    assert not check_token('AA C')
    assert check_token(generate_token())
