#!/usr/bin/env python3
"""Index codebase for semantic search. Uses Qdrant (local or server).
Requires: pip install dreamteam[vector] (sentence-transformers, numpy, qdrant-client)."""

import os
import sys
import uuid

import project
PROJECT_ROOT = project.get_project_root()
EXCLUDE_DIRS = {"__pycache__", ".git", "node_modules", "venv", ".venv", "db"}
EXCLUDE_EXT = {".pyc", ".db", ".sqlite", ".png", ".jpg", ".ico"}
MAX_CHUNK_SIZE = 500
MIN_CHUNK_SIZE = 50
COLLECTION_NAME = "dreamteam_code"
VECTOR_SIZE = 384  # all-MiniLM-L6-v2


def get_code_files() -> list[tuple[str, str]]:
    """Yield (relative_path, content) for code files."""
    for root, _, files in os.walk(PROJECT_ROOT):
        rel_root = os.path.relpath(root, PROJECT_ROOT)
        if any(ex in rel_root for ex in EXCLUDE_DIRS):
            continue
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext in EXCLUDE_EXT:
                continue
            if ext in (".py", ".ts", ".tsx", ".js", ".jsx", ".md", ".mdc"):
                path = os.path.join(root, f)
                try:
                    with open(path, encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                    rel = os.path.relpath(path, PROJECT_ROOT)
                    yield rel, content
                except OSError:
                    pass


def chunk_content(path: str, content: str) -> list[tuple[str, str]]:
    """Split content into chunks (by function/class or by size)."""
    chunks = []
    lines = content.split("\n")
    current = []
    current_len = 0

    for line in lines:
        current.append(line)
        current_len += len(line) + 1
        if current_len >= MAX_CHUNK_SIZE:
            text = "\n".join(current)
            if len(text) >= MIN_CHUNK_SIZE:
                chunks.append((path, text))
            current = []
            current_len = 0

    if current and current_len >= MIN_CHUNK_SIZE:
        chunks.append((path, "\n".join(current)))

    if not chunks and content:
        chunks.append((path, content[:2000]))

    return chunks


def _get_qdrant_client():
    """Create Qdrant client (server or local path)."""
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, VectorParams
    except ImportError:
        print("Install: pip install dreamteam[vector]", file=sys.stderr)
        sys.exit(1)

    url = project.get_qdrant_url()
    if url:
        return QdrantClient(url=url)
    path = project.get_qdrant_path()
    os.makedirs(path, exist_ok=True)
    return QdrantClient(path=path)


def _ensure_collection(client) -> None:
    """Create collection if not exists."""
    from qdrant_client.models import Distance, VectorParams

    collections = client.get_collections().collections
    names = [c.name for c in collections]
    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print(f"Created collection '{COLLECTION_NAME}'.")


def index_codebase() -> None:
    """Index all code files and store embeddings in Qdrant."""
    try:
        from sentence_transformers import SentenceTransformer
        from qdrant_client.models import PointStruct
    except ImportError:
        print("Install: pip install dreamteam[vector]", file=sys.stderr)
        sys.exit(1)

    client = _get_qdrant_client()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunks: list[tuple[str, str]] = []

    for path, content in get_code_files():
        for p, ch in chunk_content(path, content):
            chunks.append((p, ch))

    if not chunks:
        print("No code files to index.")
        return

    texts = [c[1] for c in chunks]
    paths = [c[0] for c in chunks]
    embeddings = model.encode(texts)

    # Delete and recreate for full reindex
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    _ensure_collection(client)

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=emb.tolist(),
            payload={"path": path, "chunk": chunk[:10000]},
        )
        for (path, chunk), emb in zip(zip(paths, texts), embeddings)
    ]

    # Upload in batches (Qdrant recommends ~100-200 per batch)
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i : i + batch_size]
        client.upsert(collection_name=COLLECTION_NAME, points=batch)

    print(f"Indexed {len(chunks)} chunks from {len(set(paths))} files into Qdrant.")


if __name__ == "__main__":
    index_codebase()
