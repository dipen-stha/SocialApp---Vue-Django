from django.utils.crypto import get_random_string

def generate_token()-> str:
    return get_random_string(length=64)