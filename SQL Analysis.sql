CREATE DATABASE ecommerce_db;
USE ecommerce_db;

CREATE TABLE orders_cleaned (
    Order_ID VARCHAR(20),
    Order_Date VARCHAR(10),
    Customer_ID VARCHAR(20),
    First_Purchase_Month VARCHAR(7),
    Product_ID VARCHAR(20),
    `Product Name` VARCHAR(100),
    Category VARCHAR(50),
    Quantity INT,
    Discount VARCHAR(10),
    Shipping_Cost DECIMAL(15,4),
    Shipping_Cost_Clean DECIMAL(15,4),
    Payment_Method VARCHAR(50),
    Order_Status VARCHAR(20),
    Unit_Price DECIMAL(15,4),
    Unit_Cost DECIMAL(15,4),
    Gross_Sales DECIMAL(15,4),
    Discount_Amount DECIMAL(15,4),
    Revenue DECIMAL(15,4),
    Product_Cost DECIMAL(15,4),
    Total_Cost DECIMAL(15,4),
    Profit DECIMAL(15,4),
    Completed_Profit DECIMAL(15,4),
    Profit_Margin VARCHAR(10),
    Completed_Profit_Margin VARCHAR(10),
    Order_Month VARCHAR(7),
    Order_Year SMALLINT,
    Order_Quarter VARCHAR(2),
    Age TINYINT UNSIGNED,
    Gender VARCHAR(20),
    City VARCHAR(100),
    State VARCHAR(100),
    Age_Groups VARCHAR(10),
    Completed_Order_Flag TINYINT,
    Completed_Revenue DECIMAL(15,4)
);

-- UPDATE
UPDATE orders_cleaned -- not executed
SET Shipping_Cost = NULL
WHERE Shipping_Cost = 99.999;

-- CHECK
SELECT * FROM orders_cleaned
LIMIT 29990;

-- CHECK
SELECT COUNT(*)
FROM orders_cleaned
WHERE Shipping_Cost IS NULL;

-- CHECK
SELECT
    COUNT(*) AS Total_Rows,
    COUNT(Shipping_Cost) AS Original_Shipping_Cost_Values,
    COUNT(*) - COUNT(Shipping_Cost) AS Missing_Shipping_Cost,
    COUNT(Shipping_Cost_Clean) AS Clean_Shipping_Cost_Values,
    SUM(Completed_Revenue) AS Total_Revenue,
    SUM(Completed_Profit) AS Total_Profit
FROM orders_cleaned;

-- REVENUE AND PROFIT BY CATEGORY
SELECT Category,ROUND(SUM(Completed_Revenue)/10000000,2) AS Total_Revenue,ROUND(SUM(Completed_Profit)/10000000,2) AS Total_Profit
FROM orders_cleaned
GROUP BY Category
ORDER BY Total_Revenue DESC;

-- MONTHLY REVENUE TRENDS
SELECT Order_Month,Order_Year,ROUND(SUM(Completed_Revenue)/10000000,2) AS Monthly_Revenue,ROUND(SUM(Completed_Profit)/10000000,2) AS Monthly_Profit
FROM orders_cleaned
WHERE Order_Status = "Delivered"
GROUP BY Order_Month,Order_Year
ORDER BY Monthly_Revenue DESC;

-- TOP10 PRODUCTS BY COMPLETED REVENUE
SELECT `Product Name`,Category,ROUND(SUM(Completed_Revenue)/10000000,2) AS Total_Revenue,ROUND(SUM(Completed_Profit)/10000000,2) AS Total_Profit,
SUM(Quantity) AS Total_Quantity_Sold
FROM orders_cleaned
WHERE Order_Status = "Delivered"
GROUP BY `Product Name`,Category
ORDER BY Total_Revenue DESC
LIMIT 10;

-- TOP10 CUSTOMERS BY COMPLETED SPENDING
SELECT Customer_ID,COUNT(*) AS Completed_Orders,ROUND(SUM(Completed_Revenue)/10000000,2) AS Total_Revenue,ROUND(SUM(Completed_Profit)/10000000,2) AS Total_Profit
FROM orders_cleaned
WHERE Order_Status = 'Delivered'
GROUP BY Customer_ID
ORDER BY Total_Revenue DESC
LIMIT 10;

-- REVENUE BY STATE
SELECT State,COUNT(*) AS Completed_Orders,ROUND(SUM(Completed_Revenue)/10000000,2) AS Total_Revenue,ROUND(SUM(Completed_Profit)/10000000,2) AS Total_Profit
FROM orders_cleaned
WHERE Order_Status = 'Delivered'
GROUP BY State
ORDER BY Total_Revenue DESC;

-- ORDER STATUS ANALYSIS
SELECT Order_Status,COUNT(*) AS Total_Orders,ROUND(COUNT(*) * 100 /(SELECT COUNT(*) FROM orders_cleaned),2) AS Percentage
FROM orders_cleaned
GROUP BY Order_Status
ORDER BY Total_Orders DESC;

-- PAYMENT METHOD ANALYSIS
SELECT Payment_Method,COUNT(*) AS Completed_Orders,ROUND(SUM(Completed_Revenue)/10000000,2) AS Total_Revenue,
ROUND(SUM(Completed_Profit)/10000000,2) AS Total_Profit,
ROUND(AVG(Completed_Revenue),2) AS Average_Order_Value 
FROM orders_cleaned
WHERE Order_Status = "Delivered"
GROUP BY Payment_Method
ORDER BY Total_Revenue DESC;

-- ONETIME VS REPEAT CUSTOMERS
SELECT Customer_type,COUNT(*) AS Total_Customers,SUM(Total_Orders) AS Total_Completed_Orders,
ROUND(SUM(Total_Revenue), 2) AS Total_Revenue,
ROUND(SUM(Total_Profit), 2) AS Total_Profit,
ROUND(AVG(Total_Revenue), 2) AS Avg_Revenue_Per_Customer
FROM 
(SELECT Customer_ID,COUNT(*) AS Total_Orders,SUM(Completed_Revenue) AS Total_Revenue,SUM(Completed_Profit) AS Total_Profit,
CASE 
   WHEN COUNT(*) = 1 THEN 'One-time'
   ELSE 'Repeat'
   END AS Customer_type
FROM orders_cleaned
WHERE Order_Status = "Delivered"
GROUP BY Customer_ID) AS customer_summary
GROUP BY Customer_type
ORDER BY Total_Revenue DESC;

-- CATEGORY-WISE PROFIT MARGIN

SELECT Category, ROUND(SUM(Completed_Revenue)/10000000, 2) AS Total_Revenue, ROUND(SUM(Completed_Profit)/10000000, 2) AS Total_Profit,
    ROUND(
        SUM(Completed_Profit) * 100.0 /
        NULLIF(SUM(Completed_Revenue), 0),
        2
    ) AS Profit_Margin_Percentage
FROM orders_cleaned
WHERE Order_Status = 'Delivered'
GROUP BY Category
ORDER BY Profit_Margin_Percentage DESC;

-- YEAR OVER YEAR REVENUE COMPARISON
SELECT Order_Year,ROUND(SUM(Completed_Revenue)/10000000,2) AS Total_Revenue,ROUND(SUM(Completed_Profit)/10000000,2) AS Total_Profit,COUNT(*) AS Completed_Orders
FROM orders_cleaned
WHERE Order_Status = "Delivered"
GROUP BY Order_Year
ORDER BY Order_Year;

-- AVERAGE ORDER VALUE BY YEAR
SELECT Order_Year,ROUND(SUM(Completed_Revenue)/10000000,2) AS Total_Revenue,COUNT(*) AS Completed_Orders,
ROUND(AVG(Completed_Revenue),2) AS Average_Order_Value
FROM orders_cleaned
WHERE Order_Status = "Delivered"
GROUP BY Order_Year
ORDER BY Order_Year;