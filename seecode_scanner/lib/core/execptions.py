# coding: utf-8


class CodeBaseException(Exception):
    pass


class MissingImportantScanParameters(CodeBaseException):
    pass


class DistributedConfigurationInvalid(CodeBaseException):
    pass


class DistributedDoesNotSupportStorage(CodeBaseException):
    pass


class ScanTemplateNotFound(CodeBaseException):
    pass


class ScanDirectoryIsEmpty(CodeBaseException):
    pass


class ScanTemplateMissingContent(CodeBaseException):
    pass


class UnrecognizedScanEngine(CodeBaseException):
    pass


class SystemCommandNotFound(CodeBaseException):
    pass


class ScriptFileNotFound(CodeBaseException):
    pass


class RedisCanNotConnect(CodeBaseException):
    pass


class TaskIdIsNoneException(CodeBaseException):
    pass


class TaskBranchIsNoneException(CodeBaseException):
    pass


class ModulePathIsNoneException(CodeBaseException):
    pass


class CheckoutBranchException(CodeBaseException):
    pass


class GitDoesNotPermissionException(CodeBaseException):
    pass


class ScanFailedException(CodeBaseException):
    pass


class FileLimitSizeException(CodeBaseException):
    pass


class FileLimitSuffixException(CodeBaseException):
    pass


class SonarScannerFailureException(CodeBaseException):
    pass


class SonarScannerNotFoundException(CodeBaseException):
    pass


class SonarScannerCreateIssueFailed(CodeBaseException):
    pass


class SonarQubeAuthenticationFailed(CodeBaseException):
    pass


class HTTPStatusCodeError(CodeBaseException):
    pass


class EngineExecutionTimeoutException(CodeBaseException):
    pass


class TaskExecutionTimeoutException(CodeBaseException):
    pass
