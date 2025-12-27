from pydantic import BaseModel, Field


class PaginationSchema(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(15, ge=1)
