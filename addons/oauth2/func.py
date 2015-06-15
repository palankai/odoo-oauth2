import random

import conf


def create_token(token_length=conf.DEFAULT_TOKEN_LENGTH):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    res = ""
    while len(res) < token_length:
        res += random.choice(chars)
    return res
