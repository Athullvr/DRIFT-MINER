import pandas as pd

# Loading the raw dataset used encoding to handle special characters
data = pd.read_csv(
    r"C:\Users\Athul VR\OneDrive\Desktop\DRIFT-MINER\Data set and analysis\online_retail.csv",
    encoding="ISO-8859-1"
)

print(data.head())

# Converting 'InvoiceDate' column to datetime format
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'], errors='coerce')

df_clean = data.dropna(subset=['CustomerID']).copy()

# Converting 'CustomerID' to integer type after dropping Null values
df_clean['CustomerID'] = df_clean['CustomerID'].astype(int)

# Removing rows with non-positive 'Quantity' and 'UnitPrice'
df_clean = df_clean[df_clean['UnitPrice'] > 0]

# Creating a new column 'is_cancellation' (flag cancellation)
df_clean['is_cancellation'] = df_clean['Quantity'] < 0

# Creating a new column 'abs_quantity' with absolute values of 'Quantity'
df_clean['abs_quantity'] = df_clean['Quantity'].abs()

# Sorting the DataFrame by 'CustomerID' and 'InvoiceDate'
df_clean = df_clean.sort_values(
    by=['CustomerID', 'InvoiceDate']
).reset_index(drop=True)

print("Rows after cleaning:", df_clean.shape[0])
print("Unique customers:", df_clean['CustomerID'].nunique())
print("Cancellations:", df_clean['is_cancellation'].sum())
print("Date range:",
      df_clean['InvoiceDate'].min(),
      "to",
      df_clean['InvoiceDate'].max())

