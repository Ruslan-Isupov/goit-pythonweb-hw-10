from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from src.api.contacts import routerContacts
from src.api.utils import routerUtils
from src.api.auth import routerAuth
from src.api.users import routerUsers

from src.conf.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": exc.errors(),
        },
    )


app.include_router(routerUtils, prefix="/api")
app.include_router(routerContacts, prefix="/api")
app.include_router(routerAuth, prefix="/api")
app.include_router(routerUsers, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,
    )
