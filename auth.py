from requests import post
import logging


class ReCaptcha:
    def __init__(self, token):
        self.token = token
        self.url_api = 'https://www.google.com/recaptcha/api/siteverify'
        self.token_recaptcha = ""

    def check(self) -> bool:
        """
        Check recaptcha result
        :return: Bool result
        """
        data = {
            'secret': self.token_recaptcha,
            'response': self.token,
        }
        try:
            return post(self.url_api, data=data).json()['success']
        except Exception as e:
            logging.error("ReCaptcha error: %s" % e)
