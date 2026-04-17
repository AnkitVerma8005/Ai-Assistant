class LearningAssistantException(Exception):
    """Base class for exceptions in this project."""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class InvalidVideoURLError(LearningAssistantException):
    """Raised when a video URL is invalid."""
    pass

class TranscriptRetrievalError(LearningAssistantException):
    """Raised when the transcript cannot be retrieved."""
    pass

class ConfigurationError(LearningAssistantException):
    """Raised when a configuration setting is missing or invalid."""
    def __init__(self, message):
        super().__init__(message, status_code=500)

class AIAPIError(LearningAssistantException):
    """Raised when an external AI API call fails."""
    def __init__(self, message):
        super().__init__(message, status_code=502)
