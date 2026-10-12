select * from (values
    ('RevenueFromContractWithCustomerExcludingAssessedTax', 'revenue', 'period', 1),
    ('SalesRevenueNet', 'revenue', 'period', 2),
    ('Revenues', 'revenue', 'period', 3),
    ('RevenuesNetOfInterestExpense', 'revenue', 'period', 4),
    ('SalesRevenueGoodsNet', 'revenue', 'period', 5),
    ('NetIncomeLoss', 'net_income', 'period', 1),
    ('OperatingIncomeLoss', 'operating_income', 'period', 1),
    ('Assets', 'total_assets', 'instant', 1),
    ('Liabilities', 'total_liabilities', 'instant', 1),
    ('StockholdersEquity', 'shareholders_equity', 'instant', 1)
) as t(tag, metric, period_type, priority)