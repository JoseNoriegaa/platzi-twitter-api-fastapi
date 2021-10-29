from datetime import datetime

# Pydantic
from pydantic import BaseModel
from pydantic import Field


class IDMixin(BaseModel):
    """ID Model Mixin.

    This mixin is used to add a unique ID field to a model.
    """

    id: int = Field(...,
                     description='Unique ID of the document.')


class TimestampMixin(BaseModel):

    created_at: datetime = Field(default_factory=datetime.utcnow,
                                 description='The time the document was created.')

    updated_at: datetime = Field(default=None,
                                 description='The time the document was last updated.')
