import random
import string

from django.core.mail import EmailMessage


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


def send_random_code_email(email, code, username):
    title = 'Pepsi-Event 비밀번호 초기화'
    body = f'''
    "{username}" 계정의 비밀번호가 "{code}" 으로 변경 되었습니다. 
    비밀번호 재설정: <비밀번호 재설정 URL>
    '''

    EmailMessage(title, body, to=[email]).send()
