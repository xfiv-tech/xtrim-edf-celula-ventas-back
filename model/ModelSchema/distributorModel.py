from pydantic import BaseModel
from typing import List, Optional


class DistributorModel(BaseModel):
    id: Optional[int]
    user: str
    userId: str
    distributor: str
    token: str
    created_at: Optional[str]


class ListDistributor(BaseModel):
    data: List[DistributorModel]


