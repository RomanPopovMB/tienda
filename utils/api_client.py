import httpx
from models.catalog import dict_to_catalog

async def fetch_catalog():
    url=f"https://dummyjson.com/products"
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            products = dict_to_catalog(response.json())
            return products
    except httpx.RequestError as e:
        raise Exception(f"Connection error consulting the API: {str(e)}.")
    except httpx.HTTPStatusError as e:
        raise Exception(f"Invalid API response: {e.response.status_code}.")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}.")
