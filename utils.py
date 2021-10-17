from cryptography.fernet import Fernet


class PostProcess:
    @staticmethod
    def number_formatter(num: int) -> str:
        num = float('{:.3g}'.format(num))
        magnitude = 0

        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0

        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    @staticmethod
    def encoder(link: dict, enc_key: bytes) -> str:
        salt_link = Fernet(enc_key)
        data_link = str.encode(str(link))
        return salt_link.encrypt(data_link).decode("utf-8")
