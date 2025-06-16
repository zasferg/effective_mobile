from fastapi import APIRouter, Depends, HTTPException, Query, status
from src.database.database import get_session
from src.crud.trade import TradeCrud
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.dates import get_delta_date_minus
from datetime import date
from src.cache.cache import get_redis
from redis.asyncio import Redis
import json 
from fastapi.encoders import jsonable_encoder


trade = APIRouter(prefix='/trade')


@trade.get("/all")
async def get_all(session: AsyncSession = Depends(get_session),
                  redis_cache: Redis = Depends(get_redis)):

    try:

        if not await redis_cache.get("all_trades"): 
            res = await TradeCrud.get_all(session=session)
            serializable_data = jsonable_encoder(res)

            await redis_cache.set("all_trades",json.dumps(serializable_data))
        res_cache = await redis_cache.get("all_trades")
        return json.loads(res_cache)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=str(e))



@trade.get("/last_trading_dates")
async def get_last_trading_days(days_delta: int,
                                session: AsyncSession = Depends(get_session),
                                redis_cache: Redis = Depends(get_redis)):
    
    try:

        date_delta = get_delta_date_minus(days=days_delta)

        key = f"data_for_date_from_{date_delta}"

        print(date_delta)
        if not await redis_cache.get(key):
            trading_days_result = await TradeCrud.get_last_trading_dates(session=session,
                                                              start_date=date_delta)
            if not trading_days_result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Ничего не  найдено")
        
            serializable_data = jsonable_encoder(trading_days_result)
            await redis_cache.set(key,json.dumps(serializable_data))
            
        res_cache = await redis_cache.get(key)
        return json.loads(res_cache)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=str(e))


@trade.get("/dynamics")    
async def get_dynamics(start_date: date = Query(description='Дата должна быть в формате "YYYY-MM-DD"'),
                       end_date: date = Query(description="Дата должна быть в формате YYYY-MM-DD"),
                       delivery_type_id: str = None,
                       delivery_basis_id: str = None,
                       session: AsyncSession = Depends(get_session),
                       redis_cache: Redis = Depends(get_redis)):

    try:

        key = f"data_for_dynamics_{start_date}_{end_date}_{delivery_type_id}_{delivery_basis_id}"
        print(key)
        if start_date > end_date:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Дата начала не может быть позже даты окончания"
        )
        if not await redis_cache.get(key):
            dynamics_result = await TradeCrud.get_dynamics(
                session=session,
                start_date=start_date,
                end_date=end_date,
                delivery_type_id = delivery_type_id,
                delivery_basis_id = delivery_basis_id
            )
            
            if not dynamics_result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Ничего не  найдено")
            
            serializable_data = jsonable_encoder(dynamics_result)
            await redis_cache.set(key,json.dumps(serializable_data))
            
        res_cache = await redis_cache.get(key)
        return json.loads(res_cache)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=str(e))


@trade.get("/trading_results")
async def get_trading_results(
    start_date: date = Query(description="Дата должна быть в формате YYYY-MM-DD"),
    oil_id: str = None,
    delivery_type: str = None,
    delivery_basis_id: str = None,
    session: AsyncSession = Depends(get_session),
    redis_cache: Redis = Depends(get_redis)
    ):
    
    try:

        key = f"data_for_trading_results_{start_date}_{oil_id}_{delivery_type}_{delivery_basis_id}"

        if not await redis_cache.get(key):
            trading_results = await TradeCrud.get_trading_results(
                session=session,
                start_date=start_date,
                oil_id=oil_id,
                delivery_type = delivery_type,
                delivery_basis_id = delivery_basis_id, 
                )
            if not trading_results:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Ничего не  найдено")

            serializable_data = jsonable_encoder(trading_results)
            await redis_cache.set(key,json.dumps(serializable_data))
            
        res_cache = await redis_cache.get(key)
        return json.loads(res_cache)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=str(e))