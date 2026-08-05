import uvicorn
from fastapi import FastAPI, Depends
import os
from model.model import DataUser
from fastapi.openapi.docs import get_swagger_ui_html
from faststream.rabbit.fastapi import RabbitRouter
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
router = RabbitRouter(os.getenv('RABBITMQ_URL'))

@app.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",  # Указываем правильный путь к схеме с учетом /api
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,

        # Перенаправляем загрузку стилей на стабильный и доступный CDN unpkg
        swagger_js_url="https://unpkg.com",
        swagger_css_url="https://unpkg.com",
    )

@router.post("/send-message/")
async def create_user_event(data: DataUser = Depends(DataUser)):
    playload = { "user": data.user,
        "password": data.password
                }
    await router.broker.publish(playload, queue="my_queue")

    return {"status": "success"}



app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("producer:app", host="127.0.0.1", port=8000, reload=True)
