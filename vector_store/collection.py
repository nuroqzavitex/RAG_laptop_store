from __future__ import annotations
from qdrant_client.models import Distance, VectorParams
from config.settings import cfg
from core.logger import get_logger
from vector_store.client import _get_client

log = get_logger(__name__)

def _ensure_collection(name: str, vector_size: int | None = None) -> None:
  #Đảm bảo rằng collection đã tồn tại, nếu không sẽ tạo mới
  client = _get_client()
  size = vector_size or cfg.qdrant.vector_size

  if not client.collection_exists(name):
    client.create_collection(
      collection_name=name,
      vectors_config = VectorParams(
        size = size,
        distance = Distance.COSINE
      )
    )
    log.info(f"Collection '{name}' created with vector size {size}.")
  else:
    log.debug(f"Collection '{name}' already exists.")

def get_collection_count(collection_name: str)-> int:
  client = _get_client()
  if not client.collection_exists(collection_name):
    log.info(f"Collection '{collection_name}' does not exist. Returning count as 0.")
    return 0
  info = client.get_collection(collection_name)
  return info.points_count

def delete_collection(collection_name: str) -> None:
  client = _get_client()
  if client.collection_exists(collection_name):
    client.delete_collection(collection_name)
    log.info(f"Collection '{collection_name}' deleted successfully.")
  else:
    log.warning(f"Collection '{collection_name}' does not exist. Cannot delete.")

def get_all_product_ids(collection_name: str) -> list[str]:
  client = _get_client()
  if not client.collection_exists(collection_name):
    log.info(f'Collection {collection_name} does not exist, returning empty ids')
    return []
  
  all_ids = []
  offset = None

  while True:
    results, offset = client.scroll(
      collection_name=collection_name,
      limit = 100,
      offset=offset,
      with_payload=['_doc_id']
    )

    for point in results:
      doc_id = point.payload.get('_doc_id', str(point.id)) if point.payload else str(point.id)
      all_ids.append(doc_id)
    if offset is None:
      break

  return all_ids