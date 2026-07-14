import uvicorn
from fastapi import FastAPI, Depends
import os
from model.model import DataUser, RabbitMQService
app = FastAPI()

@app.post("/send-message/")
async def create_user_event(data: DataUser = Depends(DataUser)):
     rabbitmq = RabbitMQService()
     try:
         payload = f"User: {data.user}"
         rabbitmq.send_message(message=payload)
     finally:
         rabbitmq.close()
     return {"status": "success"}






if __name__ == "__main__":
    uvicorn.run("producer:app", host="127.0.0.1", port=8000, reload=True)