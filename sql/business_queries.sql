
-- SALES INTELLIGENCE & BUSINESS ANALYTICS
-- Reusable Business Queries
-- Database: sales_intelligence.db


-- 1. Overall Business KPIs

SELECT
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    SUM(Quantity) AS Total_Quantity,
    COUNT(DISTINCT "Order ID") AS Total_Orders,
    COUNT(DISTINCT "Customer ID") AS Total_Customers,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Profit_Margin
FROM sales;



-- 2. Category Performance

SELECT
    Category,
    ROUND(SUM(Sales), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit,
    SUM(Quantity) AS Quantity,
    COUNT(DISTINCT "Order ID") AS Orders,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Profit_Margin
FROM sales
GROUP BY Category
ORDER BY Sales DESC;



-- 3. Regional Performance

SELECT
    Region,
    ROUND(SUM(Sales), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit,
    COUNT(DISTINCT "Order ID") AS Orders,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Profit_Margin
FROM sales
GROUP BY Region
ORDER BY Sales DESC;



-- 4. Monthly Sales and Profit Trend

SELECT
    strftime('%Y-%m', "Order Date") AS Month,
    ROUND(SUM(Sales), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit,
    COUNT(DISTINCT "Order ID") AS Orders
FROM sales
GROUP BY strftime('%Y-%m', "Order Date")
ORDER BY Month;



-- 5. Sub-Category Performance

SELECT
    "Sub-Category",
    ROUND(SUM(Sales), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit,
    SUM(Quantity) AS Quantity,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Profit_Margin
FROM sales
GROUP BY "Sub-Category"
ORDER BY Profit DESC;



-- 6. Top 10 Profitable Products

SELECT
    "Product ID",
    "Product Name",
    ROUND(SUM(Sales), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit,
    SUM(Quantity) AS Quantity,
    ROUND(AVG(Discount), 3) AS Avg_Discount
FROM sales
GROUP BY "Product ID", "Product Name"
ORDER BY Profit DESC
LIMIT 10;



-- 7. Top 10 Loss-Making Products

SELECT
    "Product ID",
    "Product Name",
    ROUND(SUM(Sales), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit,
    ROUND(AVG(Discount), 3) AS Avg_Discount
FROM sales
GROUP BY "Product ID", "Product Name"
HAVING SUM(Profit) < 0
ORDER BY Profit ASC
LIMIT 10;



-- 8. Top 10 Customers by Profit

SELECT
    "Customer ID",
    "Customer Name",
    ROUND(SUM(Sales), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit,
    COUNT(DISTINCT "Order ID") AS Orders,
    ROUND(AVG(Discount), 3) AS Avg_Discount
FROM sales
GROUP BY "Customer ID", "Customer Name"
ORDER BY Profit DESC
LIMIT 10;



-- 9. Discount and Profitability Analysis

SELECT
    Discount,
    ROUND(SUM(Sales), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Profit_Margin
FROM sales
GROUP BY Discount
ORDER BY Discount;

