from database import get_db_connection

def main():
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        print("Connected database:", cursor.fetchone()[0])
        cursor.execute("SHOW TABLES")
        print("Tables:")
        for row in cursor.fetchall():
            print("-", row[0])
        for table in ("Customers", "Gadgets", "Rentals", "Payments", "Returns", "Maintenance"):
            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
            print(f"{table}: {cursor.fetchone()[0]} rows")
        print("Connection test passed.")
    except Exception as exc:
        print("Connection test failed:", exc)
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    main()
