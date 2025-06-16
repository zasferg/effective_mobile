from fastapi import FastAPI
from src.routers.trade import trade
import uvicorn
from src.scheduler.apscheduler import lifespan



app = FastAPI(lifespan=lifespan)
app.include_router(trade)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
