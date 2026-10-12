"""Create the FastAPI app and connect its route modules."""

from fastapi import FastAPI, HTTPException

from app.database import database_connection, initialize_database
from app.models import Product, ProductInput

app = FastAPI(title="Small Store Management System")


@app.get("/")
def home():
    return {"message": "Welcome! Visit /docs to try the API."}


@app.get("/products")
def get_products():
    result = Product.list_products(database_connection=database_connection)
    return {"products": result}


# Keep this route above the product ID route.
@app.get("/products/low-stock")
def get_low_stock_products(limit: int = 5):
    return {"products": Product.list_low_stock(limit, database_connection)}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    result = Product.get_product(
        product_id=product_id, database_connection=database_connection
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product": result}


@app.post("/product", status_code=201)
def create_product(product: ProductInput):
    result = Product.create_product(
        product_input=product, database_connection=database_connection
    )
    return {"product": result}


@app.put("/product/{product_id}")
def edit_product(product_id: int, product: ProductInput):
    result = Product.update_product(
        product_id=product_id,
        product_input=product,
        database_connection=database_connection,
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product": result}


@app.delete("/product/{product_id}")
def delete_product(product_id: int):
    deleted = Product.delete_product(
        product_id=product_id, database_connection=database_connection
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


initialize_database()