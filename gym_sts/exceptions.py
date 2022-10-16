class StSError(Exception):
    """
    General class of StS exceptions.
    """

    pass


class StSTimeoutError(TimeoutError, StSError):
    """
    Typically indicates a CommunicationMod response was not received in time.
    """

    pass
