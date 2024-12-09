from dotenv import load_dotenv
load_dotenv()

import streamlit as st

import os
import sqlite3

import google.generativeai as genai

genai.configure(api_key="AIzaSyD8kwVzeG_EfK20U0U85e7_ijCa-11YCFQ")

def genai_response(prompt,question):
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content([prompt[0],question])

    return response.text

def sql_query(sql,DB):
    con = sqlite3.connect(DB)
    cursor = con.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    con.commit()
    con.close()
    for row in rows:
        print(row)

    return rows

prompt=[
    """

    You are an expert in converting natural language questions into precise SQL queries. Your task is to translate user-friendly questions into executable SQL statements for an e-commerce database named "orders".

    **ecom table with the following columns:

    orderid
    customerid
    ordervalue
    orderdate
    orderstatus
    sellername
    Example:

    Question: How many orders were placed in the month of January 2023?
    SQL Query: SELECT COUNT(*) FROM orders WHERE strftime('%Y-%m', orderdate) = '2023-01';

    Please provide the SQL query without any code blocks or unnecessary formatting.

    Additional Questions and Queries:

    | Question | SQL Query |
    |---|---|
    | What is the total revenue generated by each seller? | SELECT SellerName, SUM(OrderValue) AS TotalRevenue FROM ecom GROUP BY SellerName; |
    | Which customer has placed the most orders? | SELECT CustomerID, COUNT(*) AS OrderCount FROM ecom GROUP BY CustomerID ORDER BY OrderCount DESC LIMIT 1; |
    | What is the average order value for orders placed in the year 2023? | SELECT AVG(OrderValue) FROM ecom WHERE strftime('%Y', OrderDate) = '2023'; |
    | What is the percentage of orders that have been canceled? | SELECT (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ecom)) AS CancellationPercentage FROM ecom WHERE OrderStatus = 'Cancelled'; |
    | What is the average time taken to deliver an order (assuming you have a 'DeliveryDate' column)? | SELECT AVG(JULIANDAY(DeliveryDate) - JULIANDAY(OrderDate)) AS AvgDeliveryTime FROM ecom WHERE DeliveryDate IS NOT NULL; |


    replace the table name with ecom
    replace orderdate with OrderCreatedDateTime

    """

]


st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

if submit:
    response=genai_response(prompt,question)
    print(response)
    response=sql_query(response,r"C:\Users\DELL\OneDrive\Desktop\Groclake\orders.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)