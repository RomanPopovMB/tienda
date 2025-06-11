
# Tienda online
Esta práctica tiene un front muy simple hecho con Jinja2. Recoge la información de la API y la muestra con un formato más apañado. Las demás interacciones se gestionan mediante Swagger. El propio front proporciona un botón para acceder a Swagger.
## Modelos
| Modelo | Descripción |
| :---: | :---: |
| `user` | Clientes de la aplicación. Se indica el nombre, rol, email y contraseña. |
| `catalog` | Contiene toda la información devuelta por la API (https://dummyjson.com/products). |
| `order` | Pedido. Se indica el ID del usuario que lo crea. |
| `order_content` | Contenido del pedido. Haciendo referencia al pedido, guarda referencias a los productos y la cantidad de cada uno. |

## Tecnologías usadas
| Tecnología | Uso |
| :---: | :---: |
| `Uvicorn` | Implementación de web server en Python. |
| `FastAPI` | Framework para construir APIs. |
| `SQLModel` | Librería para interactuar con bases de datos SQL. |
| `Redis` | Librería para interactuar con bases de datos Redis. |
| `Jose` | Framework para transferir información de manera segura. En este caso usamos JSON Web Token (JWT). |
| `Dotenv` | Para leer valores de un archivo .env y guardarlas como variables de entorno. |
| `Bcrypt` | Permite hashear contraseñas. |
| `Jinja2` | Parte de FastAPI, motor de plantillas. |
| `OAuth2` | Parte de FastAPI, protocolo para autorizar usuarios de forma segura. |
| `HTTPException` | Parte de FastAPI, excepciones HTTP para manejar excepciones y poder dar errores más descriptivos. |
| `Front end stack` | HTML, CSS y JavaScript. Empleados en las plantillas de Jinja2. |

## Instalar y lanzar la aplicación
1. Clonar el repositorio desde GitHub.
2. Lanzar la build en Docker
`docker-compose up --build`
Si se tienen imágenes antiguas, lanzar la build con el siguiente comando
`docker-compose up --build --remove-orphans`

## Flujo básico
### Construir la aplicación
Para construir la aplicación, simplemente se lanza el archivo `docker-compose.yml` mediante el comando `docker-compose up --build`. Esto va a hacer tres cosas:
1. Levantar la base de datos PostgreSQL en el puerto 5432.
2. Levantar la base de datos Redis en el puerto 6379.
3. Levantar la aplicación en el puerto 8000. Para instalar todo lo necesario, se utiliza el archivo Dockerfile, que copia el archivo `requirements.txt` y ejecuta el comando `pip  install  -r  requirements.txt`. Finalmente expone el puerto 8000 y lanza la aplicación.
### Lanzar la aplicación
Al lanzar la aplicación, se incluyen en el router todas las rutas que se van a ofrecer al usuario.
Si no existe la base de datos, se llama al seeder.
### Flujo de uso
El usuario accede a la aplicación mediante la URL `http://localhost:8000/`. Aquí puede ver el catálogo ofrecido por la API, y además tiene un botón para acceder a Swagger.
Desde Swagger se puede interactuar de forma completa con la aplicación, interactuando con la información de usuario, pedidos, o haciendo consultas sobre los productos.
Nota: los productos nunca se guardan en la base de datos ni se pueden modificar; sólo se pueden leer de la API.
### Ejemplos
La mayoría de interacciones requieren de autorización. Los valores para usuarios de ejemplo son:
| ID | Usuario | Contraseña | Rol |
| :---: | :---: | :---: | :---: |
| 1 | client | 123 | client |
| 2 | client2 | 123 | client |
| 3 | admin | 123 | admin |
| 4 | admin2 | 123 | admin |

Obtener todos los usuarios:
`http://localhost:8000/api/user/`
```json
[
  {
    "hashed_password": "$2b$12$p3KDVraBw2PjyR5cFIVP..r/arzIr3AyHlYX8XqGNZgT3TSNsswFS",
    "role": "client",
    "name": "client",
    "id": 1,
    "email": "client@email.com",
    "refresh_token": null
  },
  {
    "hashed_password": "$2b$12$vecQl1mnnI2PJJnqwBTusuciIeBoKpVp7r6LNNlcKAxn.h.mFs5Qu",
    "role": "client",
    "name": "client2",
    "id": 2,
    "email": "client2@email.com",
    "refresh_token": null
  },...
 ]
 ```
Obtener productos de forma paginada:
`http://localhost:8000/api/product/1,2`
```json
[
  {
    "id": 1,
    "title": "Essence Mascara Lash Princess",
    "description": "The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.",
    "category": "beauty",
    "price": 9.99,
    "discountPercentage": 10.48,
    "rating": 2.56,
    "stock": 99,
    "tags": [
      "beauty",
      "mascara"
    ],
    "brand": "Essence",
    "sku": "BEA-ESS-ESS-001",
    "weight": 4,
    "dimensions": {
      "width": 15.14,
      "height": 13.08,
      "depth": 22.99
    },
    "warrantyInformation": "1 week warranty",
    "shippingInformation": "Ships in 3-5 business days",
    "availabilityStatus": "In Stock",
    "reviews": [
      {
        "rating": 3,
        "comment": "Would not recommend!",
        "date": "2025-04-30T09:41:02.053Z",
        "reviewerName": "Eleanor Collins",
        "reviewerEmail": "eleanor.collins@x.dummyjson.com"
      },
      {
        "rating": 4,
        "comment": "Very satisfied!",
        "date": "2025-04-30T09:41:02.053Z",
        "reviewerName": "Lucas Gordon",
        "reviewerEmail": "lucas.gordon@x.dummyjson.com"
      },
      {
        "rating": 5,
        "comment": "Highly impressed!",
        "date": "2025-04-30T09:41:02.053Z",
        "reviewerName": "Eleanor Collins",
        "reviewerEmail": "eleanor.collins@x.dummyjson.com"
      }
    ],
    "returnPolicy": "No return policy",
    "minimumOrderQuantity": 48,
    "meta": {
      "createdAt": "2025-04-30T09:41:02.053Z",
      "updatedAt": "2025-04-30T09:41:02.053Z",
      "barcode": "5784719087687",
      "qrCode": "https://cdn.dummyjson.com/public/qr-code.png"
    },
    "images": [
      "https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/1.webp"
    ],
    "thumbnail": "https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/thumbnail.webp"
  },
  {
    "id": 2,
    "title": "Eyeshadow Palette with Mirror",
    "description": "The Eyeshadow Palette with Mirror offers a versatile range of eyeshadow shades for creating stunning eye looks. With a built-in mirror, it's convenient for on-the-go makeup application.",
    "category": "beauty",
    "price": 19.99,
    "discountPercentage": 18.19,
    "rating": 2.86,
    "stock": 34,
    "tags": [
      "beauty",
      "eyeshadow"
    ],
    "brand": "Glamour Beauty",
    "sku": "BEA-GLA-EYE-002",
    "weight": 9,
    "dimensions": {
      "width": 9.26,
      "height": 22.47,
      "depth": 27.67
    },
    "warrantyInformation": "1 year warranty",
    "shippingInformation": "Ships in 2 weeks",
    "availabilityStatus": "In Stock",
    "reviews": [
      {
        "rating": 5,
        "comment": "Great product!",
        "date": "2025-04-30T09:41:02.053Z",
        "reviewerName": "Savannah Gomez",
        "reviewerEmail": "savannah.gomez@x.dummyjson.com"
      },
      {
        "rating": 4,
        "comment": "Awesome product!",
        "date": "2025-04-30T09:41:02.053Z",
        "reviewerName": "Christian Perez",
        "reviewerEmail": "christian.perez@x.dummyjson.com"
      },
      {
        "rating": 1,
        "comment": "Poor quality!",
        "date": "2025-04-30T09:41:02.053Z",
        "reviewerName": "Nicholas Bailey",
        "reviewerEmail": "nicholas.bailey@x.dummyjson.com"
      }
    ],
    "returnPolicy": "7 days return policy",
    "minimumOrderQuantity": 20,
    "meta": {
      "createdAt": "2025-04-30T09:41:02.053Z",
      "updatedAt": "2025-04-30T09:41:02.053Z",
      "barcode": "9170275171413",
      "qrCode": "https://cdn.dummyjson.com/public/qr-code.png"
    },
    "images": [
      "https://cdn.dummyjson.com/product-images/beauty/eyeshadow-palette-with-mirror/1.webp"
    ],
    "thumbnail": "https://cdn.dummyjson.com/product-images/beauty/eyeshadow-palette-with-mirror/thumbnail.webp"
  }
]
```
Obtener los pedidos creados:
`http://localhost:8000/api/order/`
```json
[
  {
    "user_id": 1,
    "id": 1
  },
  {
    "user_id": 2,
    "id": 2
  },
  {
    "user_id": 3,
    "id": 3
  },
  {
    "user_id": 4,
    "id": 4
  }
]
```
Obtener los datos dentro de los pedidos, es decir, por cada ID de pedido, las IDs de los productos en cada pedido y la cantidad:
`http://localhost:8000/api/order_content/`
```json
[
  {
    "product_id": 1,
    "product_amount": 1,
    "id": 1,
    "order_id": 1
  },
  {
    "product_id": 3,
    "product_amount": 2,
    "id": 2,
    "order_id": 1
  },
  {
    "product_id": 4,
    "product_amount": 1,
    "id": 3,
    "order_id": 1
  },
  {
    "product_id": 6,
    "product_amount": 1,
    "id": 4,
    "order_id": 2
  },
  {
    "product_id": 7,
    "product_amount": 1,
    "id": 5,
    "order_id": 2
  },
  {
    "product_id": 11,
    "product_amount": 1,
    "id": 6,
    "order_id": 3
  },
  {
    "product_id": 12,
    "product_amount": 2,
    "id": 7,
    "order_id": 3
  },
  {
    "product_id": 16,
    "product_amount": 6,
    "id": 8,
    "order_id": 4
  },
  {
    "product_id": 17,
    "product_amount": 2,
    "id": 9,
    "order_id": 4
  },
  {
    "product_id": 19,
    "product_amount": 1,
    "id": 10,
    "order_id": 4
  },
  {
    "product_id": 21,
    "product_amount": 3,
    "id": 11,
    "order_id": 4
  },
  {
    "product_id": 23,
    "product_amount": 12,
    "id": 12,
    "order_id": 4
  }
]
```