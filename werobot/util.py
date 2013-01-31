import random
import string


def generate_token(length=''):
    if not length:
        length = random.randint(3, 32)
    length = int(length)
    assert 3 <= length <= 32
    token = []
    letters = string.letters + string.digits
    for _ in range(length):
        token.append(random.choice(letters))
    return ''.join(token)
