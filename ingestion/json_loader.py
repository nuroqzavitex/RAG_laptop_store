from __future__ import annotations
import json
from pathlib import Path
from config.settings import cfg
from core.logger import get_logger
from core.models import Product

log = get_logger(__name__)

REQUIRED_FIELDS = {'id', 'name', 'brand', 'price', 'specs'}

def load_products(json_path: Path | None = None) -> list[Product]:
  path = json_path or cfg.paths.json_path
  if not path.exists():
    log.error(f"JSON file not found at {path}.")
    raise FileNotFoundError(f"JSON file not found at {path}.")
  
  log.info(f"Loading products from {path}...")
  
  try:
    with open(path, 'r', encoding='utf-8') as f:
      raw: list = json.load(f)
      log.info(f"Successfully loaded {len(raw)} products from JSON.")
  except json.JSONDecodeError as e:
    log.error(f"Error decoding JSON: {e}")
    return []
  
  except Exception as e:
    log.error(f"Unexpected error while loading JSON: {e}")
    return []
  
  products: list[Product] = []

  for idx, item in enumerate(raw):
    missing = REQUIRED_FIELDS - set(item.keys())
    if missing:
      log.warning(f"Product at index {idx} is missing fields: {missing}. Skipping.")
      continue
    try:
      product = Product.model_validate(item)
      products.append(product)
    except Exception as e:
      log.error(f"Error validating product at index {idx}: {e}. Skipping.")
    
  log.info(f"Loaded {len(products)} valid products after validation.")
  return products
