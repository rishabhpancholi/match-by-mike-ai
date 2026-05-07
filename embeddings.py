import os
import asyncio
from dotenv import load_dotenv
from supabase import create_async_client, AsyncClient
from langchain_openai import OpenAIEmbeddings

semaphore = asyncio.Semaphore(10)

load_dotenv()


async def update_embeddings(
    candidate: dict, supabase: AsyncClient, embeddings: OpenAIEmbeddings
):
    async with semaphore:
        text_str = f"""
        Skills: {", ".join(candidate["skills"])}
        """

        response = await embeddings.aembed_query(text_str)

        await (
            supabase.table("candidates")
            .update({"embedding": response})
            .eq("id", candidate["id"])
            .execute()
        )

        print(f"Updated embeddings for {candidate['name']}")


async def main():
    supabase = await create_async_client(
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_KEY"),
    )

    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )

    candidates = await supabase.table("candidates").select("*").execute()

    tasks = [update_embeddings(c, supabase, embeddings) for c in candidates.data]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
