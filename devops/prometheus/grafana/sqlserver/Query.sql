USE [Business];
GO

SELECT 
	S.SalesDateTime
	, P.Name
	, SUM(S.Amount) as Total
FROM Product AS P
INNER JOIN Sales as S
On P.Id = S.ProductId
GROUP BY S.SalesDateTime, P.Name

