"""Custom error types for saverbot."""


class AssumeError(Exception):
    """Error raised when STS assume role fails."""

    def __init__(self, code: str, message: str) -> None:
        """Initialize AssumeError.

        Args:
            code: Error code (e.g., 'AccessDenied', 'InvalidParameter')
            message: Human-readable error message
        """
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")

    def __repr__(self) -> str:
        """Return string representation."""
        return f"AssumeError(code={self.code!r}, message={self.message!r})"

