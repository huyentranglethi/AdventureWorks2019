SELECT pc.[EnglishProductCategoryName], g.[EnglishCountryRegionName] as Region
        ,Coalesce(p.[ModelName], p.[EnglishProductName])
        ,CASE
            WHEN Month(GetDate()) < Month(c.[BirthDate])
                THEN DateDiff(yy,c.[BirthDate],GetDate()) - 1
            WHEN Month(GetDate()) = Month(c.[BirthDate])
            AND Day(GetDate()) < Day(c.[BirthDate])
                THEN DateDiff(yy,c.[BirthDate],GetDate()) - 1
            ELSE DateDiff(yy,c.[BirthDate],GetDate())
        END as Age
        ,CASE
            WHEN c.[YearlyIncome] < 40000 THEN 'Low'
            WHEN c.[YearlyIncome] > 60000 THEN 'High'
            ELSE 'Moderate'
        END  as IncomeGroup
        ,c.[CustomerKey],		d.[CalendarYear]		,f.[OrderDate]        ,f.[SalesOrderNumber]
        ,f.SalesOrderLineNumber        ,f.OrderQuantity         ,f.ExtendedAmount
    FROM
        [dbo].[FactInternetSales] f,        [dbo].[DimDate] d,		[dbo].[DimProduct] p,
		[dbo].[DimProductSubcategory] psc,		[dbo].[DimProductCategory] pc,
		[dbo].[DimCustomer] c,		[dbo].[DimGeography] g,		[dbo].[DimSalesTerritory] s
		where
         f.[OrderDateKey] = d.[DateKey]
        and f.[ProductKey] = p.[ProductKey]
        and p.[ProductSubcategoryKey] = psc.[ProductSubcategoryKey]
        and  psc.[ProductCategoryKey] = pc.[ProductCategoryKey]
        and f.[CustomerKey] = c.[CustomerKey]
        and c.[GeographyKey] = g.[GeographyKey]
        and g.[SalesTerritoryKey] = s.[SalesTerritoryKey]
		order by c.CustomerKey

