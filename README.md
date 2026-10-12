# Small Store Management System

## Project Overview

The Small Store Management System is a Python application built using FastAPI and SQLite. It helps store owners manage product names, prices, and stock through an API.

### Purpose

Small stores sometimes use notebooks to record their products, prices, and stock. This can make it difficult to keep records updated. This project helps store owners manage their products using FastAPI and an SQLite database.

### Scope

The system can:

- Add new products.
- View all products or search for a product by ID.
- Update product names, prices, and stock.
- Delete products.
- View products with low stock.
- Check that product names are not empty and prices and stock are not negative.
- Show a 404 error when a product does not exist.

The system uses FastAPI for the API, SQLite for the database, and Pydantic to check input data.

## How to Run (Windows)

Open the VS Code terminal in the project folder and run these commands:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

After running the application, open this link in your browser:

http://127.0.0.1:8000/docs

The database file `products.db` is created automatically the first time the app runs.

## Typical Workflow

Open `/docs`, click an endpoint, press **Try it out**, then **Execute**.

1. **Add a product.** Use `POST /product` with this body:

   ```json
   {
     "name": "Rice 1kg",
     "price": 55.5,
     "stock": 3
   }
   ```

   The response returns the saved product with its new `id`:

   ```json
   {
     "product": {
       "id": 1,
       "name": "Rice 1kg",
       "price": 55.5,
       "stock": 3
     }
   }
   ```

2. **View the products.** Use `GET /products` to see all products, or `GET /products/1` to see one by its id.
3. **Check what is running out.** Use `GET /products/low-stock`. It lists products with stock at or below the limit (default 5), so Rice 1kg appears here. To use another limit, set it in the request, for example `GET /products/low-stock?limit=10`.
4. **Update the stock.** After a delivery, use `PUT /product/1` with the new name, price, and stock.
5. **Remove a product.** Use `DELETE /product/1` when the store stops selling it.

To see the error handling, try `GET /products/999` (returns 404) or add a product with a negative price (returns 422).

## Project Structure

```text
project/
├── app/
│   ├── database.py
│   └── models.py
├── main.py
├── products.db
├── requirements.txt
└── README.md
```

- `main.py` – Creates the API and its endpoints.
- `app/database.py` – Connects to the database and creates the products table.
- `app/models.py` – Defines the product data and database operations.
- `products.db` – Stores the product records.
- `requirements.txt` – Lists the required Python packages.

## How It Works

1. `main.py` receives the request.
2. Pydantic checks the input data.
3. `app/models.py` handles the product operation.
4. `app/database.py` connects to SQLite and manages the data.
5. FastAPI returns the result as JSON.

### Data Classes

`ProductInput` holds the fields a client sends and the rules for them. `Product` adds the `id` and contains the methods that run the SQL queries.

```python
class ProductInput(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    stock: int = Field(ge=0)


class Product(ProductInput):
    id: int
```

### Database Table: `products`

The products table stores each product's ID, name, price, and stock.

```sql
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    stock INTEGER NOT NULL CHECK (stock >= 0)
)
```

| Column | Type | Rule |
|---|---|---|
| `id` | INTEGER | Unique product ID |
| `name` | TEXT | Product name |
| `price` | REAL | Price must be 0 or higher |
| `stock` | INTEGER | Quantity must be 0 or higher |

### Error Handling

- **404:** The product does not exist. The response body is:

  ```json
  {
    "detail": "Product not found"
  }
  ```

- **422:** The input is invalid, such as an empty name or negative price or stock. FastAPI returns this automatically and describes which field is wrong.

## Concepts Used

- **Object-oriented programming:** `Product` and `ProductInput` are classes used to manage product data. `Product` inherits the fields of `ProductInput`.
- **Conditional statements:** `if` checks decide whether a product exists before returning, updating, or deleting it.
- **Iteration and lists:** a list comprehension loops through the database rows and builds a list of products.
- **Database:** SQLite stores product information and supports adding, viewing, updating, and deleting products.
- **Connection handling:** `database_connection()` opens the connection, saves changes, rolls back on errors, and always closes it.
- **Input validation:** Pydantic checks that product names are not empty and prices and stock are not negative.
- **Error handling:** The API returns 404 if a product is not found and 422 if the input is invalid.
- **User interface:** Swagger UI at `/docs` allows users to test the API.

## Endpoint Documentation

| Endpoint | Parameters | Purpose |
|---|---|---|
| GET `/` | None | Displays a welcome message. |
| GET `/products` | None | Displays all products. |
| GET `/products/low-stock` | `limit: int` (default 5) | Displays products with stock at or below the limit. |
| GET `/products/{product_id}` | `product_id: int` | Displays a product by ID. |
| POST `/product` | `product: ProductInput` | Adds a new product. |
| PUT `/product/{product_id}` | `product_id: int`, `product: ProductInput` | Updates a product. |
| DELETE `/product/{product_id}` | `product_id: int` | Deletes a product. |

### Example Request Body (POST and PUT)

```json
{
  "name": "Rice 1kg",
  "price": 55.5,
  "stock": 20
}
```

### Example Responses

`GET /products` returns a list of products:

```json
{
  "products": [
    {
      "id": 1,
      "name": "Rice 1kg",
      "price": 55.5,
      "stock": 20
    }
  ]
}
```

`GET /products/1`, `POST /product`, and `PUT /product/1` return one product:

```json
{
  "product": {
    "id": 1,
    "name": "Rice 1kg",
    "price": 55.5,
    "stock": 20
  }
}
```

`DELETE /product/1` returns a confirmation message:

```json
{
  "message": "Product deleted successfully"
}
```

### Limitations and Future Improvements

- The system manages products only. It does not record sales or customer information.
- The system has no login feature, so anyone who can access the API may be able to change product records.
- The /docs page is the only user interface. A custom web page could be added in the future.
- Product names are not checked for duplicates.
- Future improvements could include sales tracking, user login, and a custom interface for easier product management.
