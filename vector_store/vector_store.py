import chromadb
from chromadb.config import Settings
from core.load_settings import cfg
import logging

logger = logging.getLogger('vector_store')

class VectorStore:
  def __init__(self):
    self.client = chromadb.PersistentClient(
      path = cfg.CHROMA_DB_PATH,
      settings = Settings(anonymized_telemetry=False)
    )
    self.collection = self.client.get_or_create_collection(
      name=cfg.COLLECTION_NAME,
      metadata = {'hnsw:space': 'cosine'}
    )
    logger.info(f'Initialized ChromaDB at {cfg.CHROMA_DB_PATH}, collection: {cfg.COLLECTION_NAME}')
    logger.info(f'Current collection size: {self.collection.count()} items')

  def upsert(self, ids: list[str], embeddings: list[list[float]], texts: list[str], metadatas: list[dict]):
    if not ids:
      return
    self.collection.upsert(
      ids = ids,
      embeddings = embeddings,
      documents = texts,
      metadatas = metadatas
    )
    logger.info(f'Upserted {len(ids)} items to vector store. New collection size: {self.collection.count()}')

  def update_stock(self, product_id: str, new_stock:int):
    try:
      existing = self.collection.get(ids=[product_id], include=['metadata'])
      if not existing['ids']:
        logger.warning(f'Product ID {product_id} not found in vector store for stock update')
        return

      meta = existing['metadatas'][0]
      meta['stock'] = new_stock
      meta['in_stock'] = new_stock > 0

      self.collection.update(ids=[product_id], metadatas=[meta])
    except Exception as e:
      logger.error(f'Error updating stock for product ID {product_id}: {e}')
  
  def update_price(self, product_id: str, new_price:float):
    try:
      existing = self.collection.get(ids=[product_id], include=['metadata'])
      if not existing['ids']:
        logger.warning(f'Product ID {product_id} not found in vector store for price update')
        return
      
      meta = existing['metadatas'][0]
      meta['price'] = new_price

      self.collection.update(ids=[product_id], metadatas=[meta])
    except Exception as e:
      logger.error(f'Error updating price for product ID {product_id}: {e}')

  



  