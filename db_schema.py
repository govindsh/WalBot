import sqlite3 as sqllite
import sys
import os
import uuid

print(os.getcwd())

conn = sqllite.connect('walbot.db')


def create_table():
    with conn:
        cursor = conn.cursor()

        # Product table
        cursor.execute("CREATE TABLE IF NOT EXISTS products ("
                       "id INTEGER PRIMARY KEY, "
                       "name TEXT,"
                       "image TEXT,"
                       " cost REAL"
                       ")")
        conn.commit()
        print("Created table products")

        # Users table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY, "
            "fullname TEXT, "
            "email TEXT, "
            "password TEXT, "
            "image TEXT"
            ")")
        conn.commit()
        print("Created table users")

        # User faces
        cursor.execute("CREATE table IF NOT EXISTS faces ("
                       "face_id TEXT PRIMARY KEY,"
                       "image TEXT,"
                       "user_id INTEGER,"
                       "FOREIGN KEY(user_id) REFERENCES users(id));")
        conn.commit()

        # Item status
        cursor.execute("CREATE TABLE IF NOT EXISTS item_status ("
                       "status_num INTEGER PRIMARY KEY, "
                       "item_status TEXT,"
                       "item_id INTEGER,"
                       "user_id INTEGER,"
                       "FOREIGN KEY(item_id) REFERENCES products(id),"
                       "FOREIGN KEY(user_id) REFERENCES users(id));")
        conn.commit()

        # Store Locations
        cursor.execute("CREATE TABLE IF NOT EXISTS store_locations "
                       "(store_id TEXT PRIMARY KEY, address TEXT, city TEXT);")
        conn.commit()

        # Store user status
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_store_status ("
            "user_id INTEGER,"
            "store_id TEXT, "
            "user_in_store INTEGER,"
            "FOREIGN KEY(user_id) REFERENCES users(id));")


def insert_query(query):
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()


def run_select_query(query):
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        content = cursor.fetchall()
    return content


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(sys.argv)
        if sys.argv[1] == "create":
            print("Creating tables ")
            create_table()
    run_select_query("select count(*) from users")

    # Insert products
    # insert_query("insert into products (name,image,cost) values ('{}','{}',{})".format("Godiva Chocolate Pack 220",
    #                                                                           "/static/product_images/prd-123-5675.jpg",
    #                                                                           7.99))
    #
    # insert_query("insert into products (name,image,cost) VALUES ('{}','{}',{})".format("Walgreens Eye Drops",
    #                                                                                "/static/product_images/prd-123-5676.jpg",
    #                                                                                4.99))
    # insert_query("insert into products (name,image,cost) VALUES ('{}','{}',{})".format("Walgreens Cough Syrup",
    #                                                                                "/static/product_images/prd-123-5677.jpg",
    #                                                                                5.00))
    # insert_query("insert into products (name,image,cost) VALUES ('{}','{}',{})".format("Walgreens Heating Pad",
    #                                                                                "/static/product_images/prd-123-5678.jpg",
    #                                                                                2.99))

    # Insert item status
    insert_query("insert into item_status (item_status,item_id,user_id) VALUES ('{}', {}, {})".format("PICKED", 0, 2))
    insert_query("insert into item_status (item_status,item_id,user_id) VALUES ('{}', {}, {})".format("PICKED", 1, 2))
    insert_query("insert into item_status (item_status,item_id,user_id) VALUES ('{}', {}, {})".format("PICKED", 2, 2))
    insert_query("insert into item_status (item_status,item_id,user_id) VALUES ('{}', {}, {})".format("PICKED", 3, 2))
