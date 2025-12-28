import pandas as pd

# Loading the raw dataset used encoding to handle special characters
data = pd.read_csv(
    r"C:\Users\Athul VR\OneDrive\Desktop\DRIFT-MINER\Data set and analysis\online_retail.csv",
    encoding="ISO-8859-1"
)

# Fix numeric columns
data['Quantity'] = pd.to_numeric(data['Quantity'], errors='coerce')
data['UnitPrice'] = pd.to_numeric(data['UnitPrice'], errors='coerce')
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'], errors='coerce')

# Drop rows with missing critical values
data = data.dropna(subset=['Quantity', 'UnitPrice', 'InvoiceDate'])



data['is_cancellation'] = data['InvoiceNo'].astype(str).str.startswith('C')
data['obs_quantity'] = data['Quantity'].abs()



# grouping by 'InvoiceNo' and 'CustomerID' to create invoice-level features
# features: invoice_date, basket_size, num_products, order_value, has_cancellation
#essentially creating a summary of each invoice per customer
invoice_df = (
    data.groupby(['InvoiceNo', 'CustomerID'])
    .agg(
        invoice_date=('InvoiceDate', 'min'),
        basket_size=('obs_quantity', 'sum'),
        num_products=('StockCode', 'nunique'),
        order_value=('UnitPrice', lambda x: (x * data.loc[x.index, 'obs_quantity']).sum()),
        has_cancellation=('is_cancellation', 'max')
    )
    .reset_index()
)



#sorting the invoice-level DataFrame by 'CustomerID' and 'invoice_date'
invoice_df = invoice_df.sort_values(
    by=['CustomerID', 'invoice_date']
).reset_index(drop=True)


#customer featuring

# calculating the days between consecutive purchases for each customer
invoice_df['purchase_gap_days'] = (
    invoice_df
    .groupby('CustomerID')['invoice_date']
    .diff()
    .dt.days
)

# calculating the purchase index for each customer
invoice_df['purchase_index'] = (
    invoice_df
    .groupby('CustomerID')
    .cumcount() + 1
)

# calculating the rolling average spend over the last 3 purchases for each customer
invoice_df['rolling_avg_spend'] = (
    invoice_df
    .groupby('CustomerID')['order_value']
    .rolling(window=3, min_periods=1)
    .mean()
    .reset_index(level=0, drop=True)
)

# calculating the rolling average basket size over the last 3 purchases for each customer
invoice_df['rolling_basket_size'] = (
    invoice_df
    .groupby('CustomerID')['basket_size']
    .rolling(window=3, min_periods=1)
    .mean()
    .reset_index(level=0, drop=True)
)


# calculating the rolling average product diversity over the last 3 purchases for each customer
invoice_df['rolling_product_diversity'] = (
    invoice_df
    .groupby('CustomerID')['num_products']
    .rolling(window=3, min_periods=1)
    .mean()
    .reset_index(level=0, drop=True)
)

# calculating the cumulative count of cancellations for each customer
invoice_df['cancellation_count'] = (
    invoice_df
    .groupby('CustomerID')['has_cancellation']
    .cumsum()
)

print(invoice_df[
    ['CustomerID', 'invoice_date', 'purchase_gap_days',
     'rolling_avg_spend', 'rolling_basket_size']
].head(10))
