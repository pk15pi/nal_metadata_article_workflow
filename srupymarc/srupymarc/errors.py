class SrupymarcError(Exception):
    """
    General sruthi error class to provide a superclass for all other errors
    """


class ServerIncompatibleError(SrupymarcError):
    """
    The error raised from sru.search/sru.explain when the server doesn't behave
    like a SRU endpoint.
    """


class SruError(SrupymarcError):
    """
    The error raised from sru.search/sru.explain when the SRU response contains
    an error
    """


class NoMoreRecordsError(SrupymarcError):
    """
    This error is raised if all records have been loaded (or no records are
    present)
    """


class SrupymarcWarning(Warning):
    """
    General sruthi warning class to provide a superclass for all warnings
    """


class WrongNamespaceWarning(SrupymarcWarning):
    """
    A warning to indicate, that a server uses the wrong SRU namespace.
    """
