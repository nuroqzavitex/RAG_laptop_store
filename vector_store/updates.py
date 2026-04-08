from __future__ import annotations
from typing import Any
from qdrant_client.models import FieldCondition, Filter, MatchValue
from core.logger import get_logger
from vector_store.client import _get_client

log = get_logger(__name__)

def _find_point_by_doc_id(collection_name: str, product_id: str) -> int | None:
  # tìm sản phẩm theo id
  client = _get_client()
  try:
    results, _ = client.scroll(
      collection_name=collection_name,
      scroll_filter=Filter(
        must=[
          FieldCondition(
            key='_doc_id',
            value=MatchValue(value=product_id)
          ),
          FieldCondition(
            key='type',
            value=MatchValue(value='product')
          )
        ]
      ),
      limit=1,
      with_payload=False
    )
    if results:
      return results[0].id
    log.warning(f'No product document found with _doc_id = {product_id}')
    return None
  except Exception as e:
    log.error(f'Error finding point for {product_id}: {e}')
    return None
  
def update_metadata(collection_name: str, product_id: str, updates: dict[str, Any])-> bool:
  # Chỉ update metadata không embedding lại
  client = _get_client()
  if not client.collection_exists(collection_name):
    log.warning(f'Collection {collection_name} does not exist')
    return False
  
  point_id = _find_point_by_doc_id(collection_name, product_id)
  if point_id is None:
    log.warning(f'Product {product_id} not found in collection')
    return False
  
  try:
    # Ghi đè thuộc tính updates vào payload, nếu chưa có thì tạo mới, giữ nguyên các thuộc tính còn lại
    client.set_payload(
      collection_name=collection_name,
      payload=updates,
      points=[point_id]
    )
    log.info(f'Updated metadata for {product_id}: {updates}')
    return True
  except Exception as e:
    log.error(f'Failed to update metadata for {product_id}: {e}')
    return False
  
def update_stock(collection_name: str, product_id: str, new_stock: int) -> bool:
  return update_metadata(collection_name, product_id, {"stock": new_stock})

def update_price(collection_name: str, product_id: str, new_price: int) -> bool:
  return update_metadata(collection_name, product_id, {"price": new_price})