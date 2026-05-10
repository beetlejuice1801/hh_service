class NoTokenFound(Exception):
    def __init__(
        self,
        message="Токен отсутствует, пройдите авторизацию",
    ):
        self.message = message
