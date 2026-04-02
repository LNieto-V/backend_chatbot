"""Ingestion script to load knowledge base into Supabase vector store."""

import asyncio
import os
import sys

# Ensure the root directory is accessible for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import get_settings
from app.services.supabase_service import get_supabase_client
from app.utils.prompt_loader import load_markdown_file
from app.utils.text_processing import chunk_markdown


async def ingest_knowledge_base() -> None:
    """Read knowledge.md, generate embeddings, and insert into Supabase."""
    settings = get_settings()

    print("🚀 Iniciando ingesta de conocimientos...")

    # 1. Leer el archivo
    print("📖 Leyendo knowledge.md...")
    try:
        knowledge_text = load_markdown_file("knowledge.md")
    except Exception as e:
        print(f"❌ Error al leer knowledge.md: {e}")
        return

    # 2. Chunking
    print("🔪 Dividiendo el texto en fragmentos (chunks)...")
    chunks = chunk_markdown(knowledge_text, chunk_size=500, chunk_overlap=50)
    print(f"✅ Se generaron {len(chunks)} fragmentos.")

    # 3. Preparar Embeddings model
    # Note: models/embedding-001 has 768 dimensions
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=settings.google_api_key
    )

    # 4. Obtener cliente de Supabase
    supabase = get_supabase_client()

    # 5. Generar embeddings e insertar
    print("🧠 Generando embeddings y subiendo a Supabase...")

    success_count = 0
    error_count = 0

    # Iterar uno por uno (o en batch si es soportado)
    for i, chunk in enumerate(chunks):
        try:
            # Generar embedding para el chunk
            embedding = embeddings_model.embed_query(chunk)

            # Insertar en Supabase
            data = {
                "content": chunk,
                "embedding": embedding,
                "metadata": {"source": "knowledge.md", "chunk_index": i},
            }

            # Asume que la tabla se llama 'documents' en Supabase
            supabase.table("documents").insert(data).execute()
            success_count += 1
            print(
                f"  → Progreso: {success_count}/{len(chunks)} chunks subidos.", end="\r"
            )
        except Exception as e:
            print(f"\n❌ Error subiendo el chunk {i}: {e}")
            error_count += 1

    print("\n✅ Ingesta finalizada.")
    print(f"Resumen: {success_count} exitosos, {error_count} fallidos.")


if __name__ == "__main__":
    # Correr el loop asíncrono
    asyncio.run(ingest_knowledge_base())
