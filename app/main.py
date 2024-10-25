import os
from fastapi import APIRouter
from fastapi import Response
from creyPY.fastapi.app import generate_unique_id
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

ENV = os.getenv("ENV", "local").lower()
VERSION = os.getenv("VERSION", "Alpha")

# App Setup
app = FastAPI(
    title="ServerCrow Pong API",
    description="A really simple FastAPI service to return the request with code and content specified in the parameters. No logging, no nothing.",
    version=VERSION,
    docs_url="/",
    redoc_url=None,
    debug=ENV != "prod",
    swagger_ui_parameters={
        "docExpansion": "list",
        "displayOperationId": True,
        "defaultModelsExpandDepth": 5,
        "defaultModelExpandDepth": 5,
        "filter": True,
        "displayRequestDuration": True,
        "defaultModelRendering": "model",
        "persistAuthorization": True,
    },
    generate_unique_id_function=generate_unique_id,
)

# CORS Setup
origins = ["http://localhost:5173", "https://pong.servercrow.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# App Routers
router = APIRouter(prefix="/pong", tags=["public"])


@router.get("/", operation_id="get_pong")
async def get_status(code: int, response_text: str = "OK") -> Response:
    """Get the ping to your pong. Returns the code that is specified and a response if provided."""
    return Response(status_code=code, content=response_text)


app.include_router(router)
