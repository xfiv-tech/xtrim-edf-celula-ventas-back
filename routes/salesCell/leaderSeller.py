from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db

from model.ModelSchema.salesCellModel import LeaderSellerModel
from model.SalesCell.leaderSeller import LeaderSeller

from schemas.searchList import SearchList
from datetime import datetime
from middleware.validacionToken import ValidacionToken
from starlette.status import HTTP_204_NO_CONTENT


leaderSeller = APIRouter(route_class=ValidacionToken)

#LEADER SELLER
@leaderSeller.get("/lideres_por_vendedores", tags=["Lider por Vendedores"])
async def get_leader_sellers():
    try:
        query = LeaderSeller.select()
        data = db.execute(query).fetchall()
        return {
            "list": "Lider por Vendedores",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@leaderSeller.post("/lider_por_vendedor", tags=["Lider por Vendedores"])
async def add_leader_seller(leaderSeller: LeaderSellerModel):
    try:
        result = db.execute(LeaderSeller.insert()
            .values(leader = leaderSeller.leader,
                    seller = leaderSeller.seller,
                    created_at = datetime.now()))
        return {
            "code": "0",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@leaderSeller.put("/lider_por_vendedor", tags=["Lider por Vendedores"])
async def update_leader_seller(leaderSeller: LeaderSellerModel):
    try:
        db.execute(LeaderSeller.update()
            .values(leader = leaderSeller.leader,
                    seller = leaderSeller.seller)
            .where(LeaderSeller.c.id == leaderSeller.id))
        return {
            "code": "0",
            "data": db.execute(LeaderSeller.select()
                        .where(LeaderSeller.c.id == leaderSeller.id))
                        .first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@leaderSeller.delete("/lider_por_vendedor", tags=["Lider por Vendedores"])
async def delete_city(search: SearchList):
    try:
        db.execute(LeaderSeller.delete()
            .where(LeaderSeller.c.id == search.id))
        return {
            "message": "LeaderSeller successfully deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })
