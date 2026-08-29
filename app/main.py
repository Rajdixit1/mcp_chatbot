from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.chat_service import generate_response
from app.mcp_client import get_mcp_instruction


BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static"


app = FastAPI(
    title="MCP Chatbot API",
    version="1.0.0"
)


# Serve frontend files
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


# Temporary conversation memory
conversations: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):

    session_id: str

    message: str


class ChatResponse(BaseModel):

    session_id: str

    response: str


@app.get("/")
async def root():

    return FileResponse(
        STATIC_DIR / "index.html"
    )


@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(
    request: ChatRequest
):

    try:

        session_id = request.session_id


        if not session_id:

            raise HTTPException(
                status_code=400,
                detail="session_id is required"
            )


        if not request.message.strip():

            raise HTTPException(
                status_code=400,
                detail="message cannot be empty"
            )


        if session_id not in conversations:

            system_instruction = (
                await get_mcp_instruction()
            )


            conversations[session_id] = [

                {
                    "role": "system",

                    "content":
                        system_instruction
                }

            ]


        conversations[session_id].append(

            {
                "role": "user",

                "content":
                    request.message
            }

        )


        answer = await generate_response(

            conversations[session_id]

        )


        conversations[session_id].append(

            {
                "role": "assistant",

                "content":
                    answer
            }

        )


        return ChatResponse(

            session_id=session_id,

            response=answer

        )


    except HTTPException:

        raise


    except Exception as e:

        print(
            "CHAT ERROR:",
            repr(e)
        )


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )