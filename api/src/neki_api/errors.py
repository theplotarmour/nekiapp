class DomainError(Exception):
    """Safe public error; never accepts driver or provider exception text."""

    def __init__(self, code: str, status: int = 400, retry_after: int | None = None) -> None:
        self.code = code
        self.status = status
        self.retry_after = retry_after
        super().__init__(code)
