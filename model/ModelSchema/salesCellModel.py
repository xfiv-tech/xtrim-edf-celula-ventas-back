from pydantic import BaseModel
from typing import List, Optional


class CityModel(BaseModel):
    id: Optional[int]
    name: str
    type: int
    region: int
    status: int
    catalog: int
    manager_region: int
    manager_city: int

class ListCity(BaseModel):
    data: List[CityModel]


class AdministratorModel(BaseModel):
    id: Optional[int]
    city: int
    user: int
    status: int

class ListAdministrator(BaseModel):
    data: List[AdministratorModel]



class DistributorModel(BaseModel):
    id: Optional[int]
    name: str
    city: int
    responsible: str
    status: int
    phone: str
    email: str
    date_in: str
    date_out: str

class ListDistributor(BaseModel):
    data: List[DistributorModel]


class EmployeeModel(BaseModel):
    id: Optional[int]
    name: str
    lastname: str
    id_number: str
    address: str
    residence_city: str
    birth_date: str
    email: str
    phone: str
    operator: int
    phone_optional: str
    operator_optional: int
    gender: int
    status: int

class ListEmployee(BaseModel):
    data: List[EmployeeModel]


class MovementModel(BaseModel):
    id: Optional[int]
    category: int
    employee: int
    previous: int
    current: int
    gender: int
    status: int

class ListMovement(BaseModel):
    data: List[MovementModel]


class SalesBossModel(BaseModel):
    id: Optional[int]
    employee: int
    city: int


class ListSalesBoss(BaseModel):
    data: List[SalesBossModel]


class SellerModel(BaseModel):
    id: Optional[int]
    seller: int
    equifax_user: Optional[str]
    city: int
    channel: int
    is_leader: bool
    modality: int
    goal_volumen: int
    goal_dolars: float
    os: int
    status: int
    date_in_sales_dept: str
    date_out_sales_dept: Optional[str]
    inactive_days: Optional[int]


class ListSeller(BaseModel):
    data: List[SellerModel]

class LeaderSellerModel(BaseModel):
    id: Optional[int]
    leader: int
    seller: int


class ListLeaderSeller(BaseModel):
    data: List[LeaderSellerModel]