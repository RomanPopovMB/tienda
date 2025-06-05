import datetime
from typing import List, Dict

class Dimensions:
    def __init__(self, width: float, height: float, depth: float):
        self.width = width
        self.height = height
        self.depth = depth

class Review:
    def __init__(self, rating: int, comment: str, date: str, reviewerName: str, reviewerEmail: str):
        self.rating = rating
        self.comment = comment
        self.date = date
        self.reviewerName = reviewerName
        self.reviewerEmail = reviewerEmail

class Meta:
    def __init__(self, createdAt: datetime, updatedAt: datetime, barcode: str, qrCode: str):
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.barcode = barcode
        self.qrCode = qrCode

class Product():
    def __init__(self, id: int, title: str, description: str, category: str, price: float, discountPercentage: float, 
                 rating: float, stock: int, tags: List[str], brand: str, sku: str, weight: float, dimensions: Dimensions, 
                 warrantyInformation: str, shippingInformation: str, availabilityStatus: str, reviews: List[Review], 
                 returnPolicy: str, minimumOrderQuantity: int, meta: Meta, images: List[str], thumbnail: str):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.price = price
        self.discountPercentage = discountPercentage
        self.rating = rating
        self.stock = stock
        self.tags = tags
        self.brand = brand
        self.sku = sku
        self.weight = weight
        self.dimensions = dimensions
        self.warrantyInformation = warrantyInformation
        self.shippingInformation = shippingInformation
        self.availabilityStatus = availabilityStatus
        self.reviews = reviews
        self.returnPolicy = returnPolicy
        self.minimumOrderQuantity = minimumOrderQuantity
        self.meta = meta
        self.images = images
        self.thumbnail = thumbnail

class Catalog():
    def __init__(self, products: List[Product]):
        self.products = products

# Receives a dict and turns it into a catalog. A catalog has
# multiple products.
def dict_to_catalog(data: Dict) -> Catalog:
    products = []
    for product_data in data['products']:
        dimensions = Dimensions(**product_data.get('dimensions', {}))
        reviews = [Review(**review) for review in product_data.get('reviews', [])]
        meta = Meta(**product_data.get('meta', {}))
        product = Product(
            id=product_data.get('id', 0),
            title=product_data.get('title', ''),
            description=product_data.get('description', ''),
            category=product_data.get('category', ''),
            price=product_data.get('price', 0.0),
            discountPercentage=product_data.get('discountPercentage', 0.0),
            rating=product_data.get('rating', 0.0),
            stock=product_data.get('stock', 0),
            tags=product_data.get('tags', []),
            brand=product_data.get('brand', ''),
            sku=product_data.get('sku', ''),
            weight=product_data.get('weight', 0.0),
            dimensions=dimensions,
            warrantyInformation=product_data.get('warrantyInformation', ''),
            shippingInformation=product_data.get('shippingInformation', ''),
            availabilityStatus=product_data.get('availabilityStatus', ''),
            reviews=reviews,
            returnPolicy=product_data.get('returnPolicy', ''),
            minimumOrderQuantity=product_data.get('minimumOrderQuantity', 0),
            meta=meta,
            images=product_data.get('images', []),
            thumbnail=product_data.get('thumbnail', '')
        )
        products.append(product)
    return Catalog(products)