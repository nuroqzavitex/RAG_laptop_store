from __future__ import annotations
from config.settings import cfg
from core.logger import get_logger
from vector_store import update_price as _update_price

log = get_logger(__name__)

def update_price_single(product_id: str, new_price: int) -> bool:
  log.info(f'Updating price: {product_id} -> {new_price} VNĐ')
  return _update_price(cfg.qdrant.knowled_collection, product_id, new_price)

def update_price_batch(updates: dict[str, int]) -> dict[str, bool]:
  "updates: {product_id: new_price}"
  results = {}
  for pid, price in updates.items():
    results[pid] = update_price_single(pid, price)
  return results #results: {product_id, True}
