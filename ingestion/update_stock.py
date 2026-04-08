from __future__ import annotations
from config.settings import cfg
from core.logger import get_logger
from vector_store import update_stock as _update_stock

log = get_logger(__name__)

def update_stock_single(product_id: str, new_stock: int) -> bool:
  log.info(f'Updating stock: {product_id} -> {new_stock}')
  return _update_stock(cfg.qdrant.knowledge_collection, product_id, new_stock)

def update_stock_batch(updates: dict[str, int]) -> dict[str, bool]:
  "updates: {product_id: new_stock}"
  results = {}
  for pid, stock in updates.items():
    results[pid] = update_stock_single(pid, stock)
  return results #results: {product_id, True}