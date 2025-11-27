class BotError(Exception):
    pass


class StreamError(BotError):
    pass


class StreamConnectionError(StreamError):
    pass


class StreamInterruptionError(StreamError):
    pass


class DataParsingError(BotError):
    pass
