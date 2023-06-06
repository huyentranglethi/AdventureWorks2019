--popular products
select top 10
p.Name, sum(s.OrderQty) as number_order
from Production.Product p
join Sales.SalesOrderDetail s
on p.ProductID = s.ProductID
group by p.Name
order by number_order desc

--the best selling item by value
select p.Name as Product_Name, sum(s.OrderQty*s.UnitPrice) as total_value
from Production.Product p
join Sales.SalesOrderDetail s
on p.ProductID = s.ProductID
group by p.Name
order by total_value desc
offset 0 rows fetch first 1 rows only

--the region with the highest revenue
select top 10
st.Name as Product_Name, sum(soh.TotalDue) as total_sale,
sum(s.OrderQty) as total_order
from Sales.SalesTerritory st
join Sales.SalesOrderHeader soh
on st.TerritoryID = soh.TerritoryID
join Sales.SalesOrderDetail s
on s.SalesOrderID = soh.SalesOrderID
group by st.Name
order by total_sale desc

--prospect file
select top 10
sc.AccountNumber, sum(soh.TotalDue) as Customer_sale,
sum(s.OrderQty) as Customer_order
from Sales.Customer sc
join Sales.SalesOrderHeader as soh
on sc.CustomerID = soh.CustomerID
join Sales.SalesOrderDetail s
on s.SalesOrderID = soh.SalesOrderID
group by sc.AccountNumber
order by Customer_sale desc

--revenue by year
select year(OrderDate) as Year,
round(sum(TotalDue),0) as Total_sale
from Sales.SalesOrderHeader
group by year(OrderDate)
order by Total_sale desc

--revenue by month
select month(OrderDate) as Month,
round(sum(TotalDue),0) as Total_sale
from Sales.SalesOrderHeader
group by month(OrderDate)
order by Total_sale desc

--totalorder by range $
with temp1 as (select SalesOrderID, round(sum(OrderQty*UnitPrice),0) as total_order
from Sales.SalesOrderDetail
group by SalesOrderID),
temp2 as (select SalesOrderID, total_order, 
case
when total_order between 0 and 99 then '0-99'
when total_order between 100 and 999 then '100-999'
when total_order between 1000 and 9999 then '1000-9999'
when total_order >= 10000 then '10000'
else 'error'
end as rng
from temp1)
select rng 'range', count(total_order) as number_order, round(sum(total_order),2) as total_order
from temp2
group by rng
order by total_order 

--campaign
with temp(Sales_Month, Month_Revenue, Promotion_Running) as(
select convert(char(7), soh.OrderDate, 120) as Sales_Month,
sum(sod.LineTotal) as Month_Revenue,
case 
when exists (select SpecialOfferID from Sales.SpecialOffer as so
where soh.SalesOrderID in (select SalesOrderID from Sales.SalesOrderDetail
where SpecialOfferID = so.SpecialOfferID)
and getdate() between so.StartDate and so.EndDate)
then 'yes'
else 'no'
end as Promotion_Running
from Sales.SalesOrderDetail sod
inner join Sales.SalesOrderHeader soh
on sod.SalesOrderID = soh.SalesOrderID
group by convert(char(7), soh.OrderDate, 120), soh.SalesOrderID)
select Sales_Month,
round(sum(Month_Revenue),0) as Month_Revenue,
max(Promotion_Running) as Promotion_Running
from temp
group by Sales_Month
order by Sales_Month desc

