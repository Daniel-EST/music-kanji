class InvalidCountry(Exception):
    pass


class InvalidRecurrence(Exception):
    pass


class InvalidDate(Exception):
    def __init__(self, date):
        self.__date = date

    def __str__(self):
        return f"{self.__date} It's not a valid date"


class InvalidCredentials(Exception):
    pass


# TODO ADD BETTER EXCEPTION MESSAGES
