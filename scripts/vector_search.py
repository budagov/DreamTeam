#!/usr/bin/env python3
"""Semantic search over indexed codebase. Uses Qdrant (local or server).
Requires: pip install dreamteam[vector] (sentence-transformers, numpy, qdrant-client)."""

import sys

import project
DEFAULT_TOP_K = 5
COLLECTION_NAME = "dreamteam_code"


def _get_qdrant_client():
    """Create Qdrant client (server or local path)."""
    try:
        from qdrant_client import QdrantClient
    except ImportError:
        print("Install: pip install dreamteam[vector]", file=sys.stderr)
        sys.exit(1)

    url = project.get_qdrant_url()
    if url:
        return QdrantClient(url=url)
    path = project.get_qdrant_path()
    return QdrantClient(path=path)


def search(query: str, top_k: int = DEFAULT_TOP_K) -> list[tuple[str, str, float]]:
    """Return list of (path, chunk, score) sorted by relevance."""
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Install: pip install dreamteam[vector]", file=sys.stderr)
        return []

    client = _get_qdrant_client()

    try:
        info = client.get_collection(COLLECTION_NAME)
    except Exception:
        print("No index. Run: dreamteam vector-index", file=sys.stderr)
        return []

    if info.points_count == 0:
        print("Index is empty. Run: dreamteam vector-index", file=sys.stderr)
        return []

    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_emb = model.encode([query], convert_to_numpy=True).tolist()[0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_emb,
        limit=top_k,
        with_payload=True,
    )

    out = []
    for pt in results.points:
        payload = pt.payload or {}
        path = payload.get("path", "")
        chunk = payload.get("chunk", "")
        score = float(pt.score if pt.score is not None else 0.0)
        out.append((path, chunk, score))
    return out


def main() -> None:
    """CLI: python vector_search.py <query> [--top N]"""
    if len(sys.argv) < 2:
        print("Usage: python vector_search.py <query> [--top N]", file=sys.stderr)
        sys.exit(1)

    args = sys.argv[1:]
    top_k = DEFAULT_TOP_K
    if "--top" in args:
        idx = args.index("--top")
        if idx + 1 < len(args):
            try:
                top_k = int(args[idx + 1])
            except ValueError:
                pass
        args = args[:idx] + args[idx + 2:]
    query = " ".join(args)

    results = search(query, top_k)
    for path, chunk, score in results:
        preview = chunk[:200].replace("\n", " ") + ("..." if len(chunk) > 200 else "")
        print(f"[{score:.3f}] {path}")
        print(f"  {preview}")
        print()


if __name__ == "__main__":
    main()
