from pydantic import BaseModel, Field


class PaginationSchema(BaseModel):
    page: int = Field(0, ge=0)
    page_size: int = Field(10, ge=1)
