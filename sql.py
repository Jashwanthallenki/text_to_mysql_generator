import sqlite3
import random
import datetime

connection = sqlite3.connect("orders.db")

cursor = connection.cursor()

cursor.execute("CREATE TABLE ecom(OrderID INT,CustomerID INT,OrderCreatedDateTime DATE,OrderValue INT,OrderStatus VARCHAR(20),RefundStatus VARCHAR(20),SellerName VARCHAR(20));")

def generate_random_order():
    customer_id = random.randint(1, 100)
    order_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
    order_value = random.randint(10, 10000)
    order_status = random.choice(["Pending", "Shipped", "Delivered", "Cancelled", "Returned"])
    refund_status = random.choice(["None", "Pending", "Processed", "Completed"])
    seller_name = random.choice(["Rahul", "Vishnu", "Ram", "Suresh", "Eshwar"])
    return (customer_id, order_date.strftime('%Y-%m-%d'), order_value, order_status, refund_status, seller_name)

for _ in range(100):
    order_data = generate_random_order()
    insert_query = """
    INSERT INTO ecom(CustomerID, OrderCreatedDateTime, OrderValue, OrderStatus, RefundStatus, SellerName)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insert_query, order_data)

print("Table rows:")
data = cursor.execute('''select * from ecom''')

for row in data:
    print(row)
    
connection.commit()
connection.close()
