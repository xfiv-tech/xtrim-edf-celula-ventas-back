from pydantic import BaseModel
from typing import List, Optional



class SubmenuBase(BaseModel):
    id_menus: Optional[int]
    submenu: Optional[str]
    path: Optional[str]
    icon: Optional[str]


class MenuBase(BaseModel):
    id: Optional[int] = 0
    id_roles: int
    menu: str
    path: Optional[str]
    icon: Optional[str]
    submenus: List[SubmenuBase]


