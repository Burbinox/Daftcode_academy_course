import sqlite3

from fastapi import FastAPI

app = FastAPI()


@app.get("/categories")
async def categories():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific
    category_id = app.db_connection.execute("SELECT CategoryID, CategoryName FROM Categories ").fetchall()
    ready_data = [{"id": item[0], "name": item[1]}for item in category_id]
    return {
        "categories": ready_data
    }


@app.get("/customers")
async def customers():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific
    customers_id = app.db_connection.execute("SELECT CustomerID, CompanyName FROM Customers ").fetchall()
    ready_data = [{"id": item[0], "name": item[1]}for item in customers_id]
    return {
        "categories": ready_data
    }
