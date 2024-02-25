import asyncio
import json
from typing import Set, Dict, List, Any
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Body
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from datetime import datetime
from pydantic import BaseModel, field_validator
from config import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# Session model
class Base(DeclarativeBase):
    pass
class ProcessedAgentDataToPost(Base):
    __tablename__ = 'processed_agent_data'
    id: Mapped[int] = mapped_column(primary_key=True)
    road_state: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int]
    x: Mapped[float]
    y: Mapped[float]
    z: Mapped[float]
    latitude: Mapped[float]
    longitude: Mapped[float]
    timestamp: Mapped[datetime]

    def repr(self) -> str:
        return str("Data(id="+str(self.id)+
            ",road_state="+str(self.road_state)+
            ",user_id="+str(self.user_id)+
            ",x="+str(self.x)+
            ",y="+str(self.y)+
            ",z="+str(self.z)+
            ",latitude="+str(self.latitude)+
            ",longitude="+str(self.longitude)+
            ",timestamp="+str(self.timestamp))

# FastAPI app setup
app = FastAPI()
# SQLAlchemy setup
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
metadata = MetaData()
# Define the ProcessedAgentData table
processed_agent_data = Table(
    "processed_agent_data",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("road_state", String),
    Column("user_id", Integer),
    Column("x", Float),
    Column("y", Float),
    Column("z", Float),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("timestamp", DateTime),
)
SessionLocal = sessionmaker(bind=engine)


# SQLAlchemy model
class ProcessedAgentDataInDB(BaseModel):
    id: int
    road_state: str
    user_id: int
    x: float
    y: float
    z: float
    latitude: float
    longitude: float
    timestamp: datetime


# FastAPI models
class AccelerometerData(BaseModel):
    x: float
    y: float
    z: float


class GpsData(BaseModel):
    latitude: float
    longitude: float


class AgentData(BaseModel):
    user_id: int
    accelerometer: AccelerometerData
    gps: GpsData
    timestamp: datetime

    @classmethod
    @field_validator("timestamp", mode="before")
    def check_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError(
                "Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)."
            )


class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData


# WebSocket subscriptions
subscriptions: Dict[int, Set[WebSocket]] = {}


# FastAPI WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    if user_id not in subscriptions:
        subscriptions[user_id] = set()
    subscriptions[user_id].add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscriptions[user_id].remove(websocket)


# Function to send data to subscribed users
async def send_data_to_subscribers(user_id: int, data):
    if user_id in subscriptions:
        for websocket in subscriptions[user_id]:
            await websocket.send_json(json.dumps(data))


# FastAPI CRUDL endpoints

@app.post("/processed_agent_data/")
async def create_processed_agent_data(data: List[ProcessedAgentData]):
    with SessionLocal() as session:
        currdata = ProcessedAgentDataToPost(
                id = data[0].agent_data.user_id,
                road_state = data[0].road_state,
                user_id = 1,
                x = 1.2,
                y = 1.3,
                z = 1.4,
                latitude = 2.1,
                longitude = 2.2,
                timestamp = datetime.now()
            )
        session.add(currdata)
        session.commit()



@app.get(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB,
)
def read_processed_agent_data(processed_agent_data_id: int):
    # Get data by id
    pass


@app.get("/processed_agent_data/")
async def get_processed_agent_data():
    with SessionLocal() as session:
        try:
            # Query all processed agent data from the database
            result = session.query(processed_agent_data).limit(100).all()
            # processed_data = result.all()
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
# @app.get("/processed_agent_data/", response_model=ProcessedAgentDataInDB,)
# def list_processed_agent_data(db: Session = Depends(get_db)):
#    return db.query(ProcessedAgentDataInDB).all()


@app.put(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB,
)
def update_processed_agent_data(processed_agent_data_id: int, data: ProcessedAgentData):
    # Update data
    pass


@app.delete(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB,
)
def delete_processed_agent_data(processed_agent_data_id: int):
    # Delete by id
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
