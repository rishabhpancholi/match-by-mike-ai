from contextlib import asynccontextmanager
from fastapi import FastAPI
from supabase import create_async_client, AsyncClient
from core import config
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

@asynccontextmanager
async def lifespan(app: FastAPI):
    supabase_client: AsyncClient = await create_async_client(
        supabase_url=config.supabase_url, supabase_key=config.supabase_key
    )

    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=config.openai_api_key)

    embedding = OpenAIEmbeddings(openai_api_key=config.openai_api_key)

    app.state.supabase_client = supabase_client
    app.state.llm_client = llm
    app.state.embedding = embedding

    yield
