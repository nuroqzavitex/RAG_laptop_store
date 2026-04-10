from __future__ import annotations
import time
from typing import Any
from config.settings import cfg
from core.logger import get_logger
from core.models import RetrievedDoc
from embedding.embedder import embed_texts
from vector_store import search as vector_search
from retriever.intent_parser import parse_intent
from retriever.filter_builder import build_where_clause, build_metadata_filter, post_filter_results
from retriever.bm25_reranker import bm25_rerank
from retriever.hybrid_scorer import compute_hybrid_scores

log = get_logger(__name__)

def retrieve_knowledge(query: str, top_k: int | None = None, final_top_k: int | None = None) -> tuple[list[RetrievedDoc], dict[str, Any], float]:
  # query: câu hỏi user, top_k: số doc lấy từ vector db ban đầu, final_top_k: số doc cuối cùng trả về
  start = time.time()
  top_k = top_k or cfg.retrieval.top_k
  final_top_k = final_top_k or cfg.retrieval.final_top_k

  # 1. Parse intent
  intent = parse_intent(query)
  where = build_where_clause(intent)
  meta_filter = build_metadata_filter(intent)

  # 2. Embed query
  query_emb = embed_texts(query)

  # 3. Vector search 
  raw = vector_search(
    collection_name=cfg.qdrant.knowledge_collection,
    query_embedding= query_emb,
    top_k=top_k,
    where=where
  )

  ids = raw['ids'][0] if raw['ids'] else [] # trong raw thuộc tính ids có dạng [[id1, id2,...]]
  

  


