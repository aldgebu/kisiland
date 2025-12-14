from enum import StrEnum


class CustomerStatusEnum(StrEnum):
    SUCCESSFUL = 'successful'
    DELETED = 'deleted'


class CustomerVisitTypeEnum(StrEnum):
    HOURLY = 'hourly'
    UNLIMITED = 'unlimited'
