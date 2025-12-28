# Data overview

Dataset Description
This project uses a real-world retail transactional dataset containing customer purchase records over time. Each row represents a product-level transaction linked to an invoice, customer, and timestamp. The dataset supports longitudinal analysis of customer behavior.

Data type: Retail transactional data
Granularity: Product-level transactions grouped by invoices
Primary entities: Customers, invoices, products
Temporal coverage: Multi-month time span suitable for behavior change analysis

Dataset Structure
The dataset includes the following core columns:

`InvoiceNo` – Identifier for each purchase invoice
`StockCode` – Product identifier
`Description` – Product description
`Quantity` – Number of units purchased (negative values indicate cancellations or returns)
`InvoiceDate` – Date and timee of transaction
`UnitPrice` – Price per unit
`CustomerID` – Unique customer identifier
`Country` – Customer country

This structure enables analysis at customer, invoice, and product levels.

 Initial Observations

Initial inspection revealed the following characteristics:

 Customers appear multiple times, enabling repeat-purchase analysis
 Transaction timestamps allow ordering of customer behavior over time
 Some rows contain missing `CustomerID`, preventing customer-level tracking for those entries
 Negative values in `Quantity` represent cancellations or returns
 Unit prices and quantities show skewed distributions, common in retail data
 Invoices may contain multiple products, enabling basket-size and diversity analysis

 Suitability for DRIFT-MINER
The dataset is well suited for the objectives of DRIFT-MINER

 Supports temporal behavior analysis required for drift detection
 Enables identification of gradual behavioral changes
 Allows detection of silent-risk customers through weakening activity patterns
 Provides sufficient detail for behavior-chain and breakpoint analysis

The absence of explicit churn labels aligns with the research goal of inferring churn behaviorally rather than relying on predefined outcomes.

Scope Notes

External factors such as promotions, pricing strategies, or marketing campaigns are not explicitly included
All behavioral conclusions are derived from observed transactional patterns

These limitations are acknowledged as part of the research scope.
