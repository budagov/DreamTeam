#!/usr/bin/env python3
"""Index codebase for semantic search. Uses Qdrant (local or server).
Requires: pip install dreamteam[vector] (sentence-transformers, numpy, qdrant-client)."""

import os
import sys
import uuid
import re

import project
PROJECT_ROOT = project.get_project_root()
EXCLUDE_DIRS = {"__pycache__", ".git", "node_modules", "venv", ".venv", "db"}
EXCLUDE_EXT = {".pyc", ".db", ".sqlite", ".png", ".jpg", ".ico"}
TARGET_CHUNK_SIZE = 1000
MAX_CHUNK_SIZE = 1200
MIN_CHUNK_SIZE = 80
OVERLAP_SIZE = 120
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


def _structural_start_regex(path: str) -> re.Pattern[str] | None:
    """Return regex for structural boundaries by file type."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".py":
        return re.compile(r"^\s*(class\s+\w+|def\s+\w+)\b")
    if ext in {".ts", ".tsx", ".js", ".jsx"}:
        return re.compile(
            r"^\s*(class\s+\w+|function\s+\w+|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)\b"
        )
    if ext in {".md", ".mdc"}:
        return re.compile(r"^\s*#{1,3}\s+")
    return None


def _window_chunk_lines(
    lines: list[str], start_line: int, kind: str
) -> list[tuple[str, int, int, str]]:
    """Chunk a list of lines into overlapped windows with line ranges."""
    out: list[tuple[str, int, int, str]] = []
    if not lines:
        return out

    i = 0
    n = len(lines)
    while i < n:
        current: list[str] = []
        cur_len = 0
        start_idx = i
        while i < n:
            ln = lines[i]
            ln_len = len(ln) + 1
            if current and cur_len + ln_len > MAX_CHUNK_SIZE:
                break
            current.append(ln)
            cur_len += ln_len
            i += 1
            if cur_len >= TARGET_CHUNK_SIZE:
                break

        text = "\n".join(current).strip()
        if len(text) >= MIN_CHUNK_SIZE:
            abs_start = start_line + start_idx
            abs_end = start_line + i - 1
            out.append((text, abs_start, abs_end, kind))

        if i >= n:
            break

        # Move back to create overlap (by characters, approximated via lines).
        back_chars = 0
        j = i - 1
        while j > start_idx and back_chars < OVERLAP_SIZE:
            back_chars += len(lines[j]) + 1
            j -= 1
        i = max(j + 1, start_idx + 1)

    return out


def chunk_content(path: str, content: str) -> list[tuple[str, str, int, int, str]]:
    """Split content into structural chunks, fallback to overlapped windows."""
    all_lines = content.split("\n")
    if not all_lines:
        return []

    boundary_re = _structural_start_regex(path)
    boundaries: list[int] = []
    if boundary_re:
        for idx, line in enumerate(all_lines):
            if boundary_re.match(line):
                boundaries.append(idx)

    chunks: list[tuple[str, str, int, int, str]] = []

    if boundaries:
        boundaries.append(len(all_lines))
        for b_idx in range(len(boundaries) - 1):
            start = boundaries[b_idx]
            end = boundaries[b_idx + 1]
            block_lines = all_lines[start:end]
            block_chunks = _window_chunk_lines(block_lines, start + 1, "struct")
            for text, s_line, e_line, kind in block_chunks:
                chunks.append((path, text, s_line, e_line, kind))
    else:
        block_chunks = _window_chunk_lines(all_lines, 1, "window")
        for text, s_line, e_line, kind in block_chunks:
            chunks.append((path, text, s_line, e_line, kind))

    if not chunks and content.strip():
        snippet = content[:2000]
        line_count = snippet.count("\n") + 1
        chunks.append((path, snippet, 1, line_count, "fallback"))

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
    chunks: list[tuple[str, str, int, int, str]] = []

    for path, content in get_code_files():
        for p, ch, start_line, end_line, kind in chunk_content(path, content):
            chunks.append((p, ch, start_line, end_line, kind))

    if not chunks:
        print("No code files to index.")
        return

    texts = [c[1] for c in chunks]
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
            payload={
                "path": path,
                "chunk": chunk[:10000],
                "start_line": start_line,
                "end_line": end_line,
                "kind": kind,
            },
        )
        for (path, chunk, start_line, end_line, kind), emb in zip(chunks, embeddings)
    ]

    # Upload in batches (Qdrant recommends ~100-200 per batch)
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i : i + batch_size]
        client.upsert(collection_name=COLLECTION_NAME, points=batch)

    print(f"Indexed {len(chunks)} chunks from {len({c[0] for c in chunks})} files into Qdrant.")


if __name__ == "__main__":
    index_codebase()
