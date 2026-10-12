"""Data models used to validate API input and output."""

from pydantic import BaseModel, ConfigDict, Field


class ProductInput(BaseModel):
    """Fields a client can send when creating or updating a product."""

    # Remove extra spaces and reject empty product names.
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    stock: int = Field(ge=0)


class Product(ProductInput):
    """A product record returned by the API."""

    id: int

    @staticmethod
    def list_products(database_connection):
        """Return every product as a list of dictionaries."""
        with database_connection() as connection:
            rows = connection.execute(
                "SELECT id, name, price, stock FROM products ORDER BY id"
            ).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def list_low_stock(limit, database_connection):
        """Return products whose stock is at or below the given limit."""
        with database_connection() as connection:
            rows = connection.execute(
                "SELECT id, name, price, stock FROM products "
                "WHERE stock <= ? ORDER BY stock, id",
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def create_product(product_input, database_connection):
        """Insert a new product and return the saved record."""
        with database_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
                (product_input.name, product_input.price, product_input.stock),
            )
            row = connection.execute(
                "SELECT id, name, price, stock FROM products WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        return dict(row)

    @staticmethod
    def get_product(product_id, database_connection):
        """Return one product, or None if the id does not exist."""
        with database_connection() as connection:
            row = connection.execute(
                "SELECT id, name, price, stock FROM products WHERE id = ?",
                (product_id,),
            ).fetchone()
        if row is None:
            return None
        return dict(row)

    @staticmethod
    def update_product(product_id, product_input, database_connection):
        """Update a product and return it, or None if the id does not exist."""
        with database_connection() as connection:
            cursor = connection.execute(
                "UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?",
                (product_input.name, product_input.price, product_input.stock, product_id),
            )
            if cursor.rowcount == 0:
                return None
            row = connection.execute(
                "SELECT id, name, price, stock FROM products WHERE id = ?",
                (product_id,),
            ).fetchone()
        return dict(row)

    @staticmethod
    def delete_product(product_id, database_connection):
        """Delete a product. Return True if a row was removed, else False."""
        with database_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM products WHERE id = ?", (product_id,)
            )
        return cursor.rowcount > 0