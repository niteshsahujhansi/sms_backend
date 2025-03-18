from pydantic import BaseModel
from typing import Optional

class CamelCaseModel(BaseModel):
    """Base model with camelCase conversion and ORM support."""
    
    class Config:
        alias_generator = lambda s: ''.join([s.split('_')[0]] + [w.capitalize() for w in s.split('_')[1:]])  # Converts to camelCase
        populate_by_name = True
        from_attributes = True  # No harm in keeping this for all schemas

class AddressBase(CamelCaseModel):
    house_no: str
    street_address: str
    landmark: Optional[str] = None
    city: str
    state: str
    zip_code: str
    country: str


class AddressCreate(AddressBase):
    pass
    # id: int

class AddressResponse(AddressBase):
    id: int

    class Config:
        from_attributes = True
