import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

file_path = '/mnt/data/Enhanced_Dummy_HBL_Data(1).csv'
data = pd.read_csv(file_path)

account_type_distribution = data['Account Type'].value_counts(normalize=True)
plt.figure(figsize=(8, 6))
account_type_distribution.plot.pie(autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.title('Distribution of Account Types')
plt.ylabel('')
plt.show()

transaction_flow = data.groupby(['Region', 'Transaction To'])['Credit'].sum().reset_index()
top_beneficiary_banks = transaction_flow.groupby('Region').apply(
    lambda x: x.nlargest(5, 'Credit')).reset_index(drop=True)

plt.figure(figsize=(12, 8))
sns.barplot(data=top_beneficiary_banks, x='Region', y='Credit', hue='Transaction To')
plt.title('Top 5 Beneficiary Banks by Region (Credit Transactions)')
plt.ylabel('Credit Amount')
plt.xticks(rotation=45)
plt.legend(title='Beneficiary Bank', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

transaction_intensity = data.groupby('Region')[['Credit', 'Debit']].sum().reset_index()
transaction_intensity['Total'] = transaction_intensity['Credit'] + transaction_intensity['Debit']

plt.figure(figsize=(10, 6))
sns.heatmap(transaction_intensity.set_index('Region')[['Credit', 'Debit']], annot=True, fmt=".2f", cmap='Blues')
plt.title('Geographic Heatmap of Transaction Intensity')
plt.ylabel('Region')
plt.tight_layout()
plt.show()

data['Credit_Z'] = (data['Credit'] - data['Credit'].mean()) / data['Credit'].std()
data['Debit_Z'] = (data['Debit'] - data['Debit'].mean()) / data['Debit'].std()

anomalies = data[(data['Credit_Z'].abs() > 3) | (data['Debit_Z'].abs() > 3)]

plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='Credit', y='Debit', alpha=0.5, label='Normal')
sns.scatterplot(data=anomalies, x='Credit', y='Debit', color='red', label='Anomaly', s=50)
plt.title('Anomalies in Transactions')
plt.xlabel('Credit')
plt.ylabel('Debit')
plt.legend()
plt.show()

plt.figure(figsize=(12, 8))
sns.boxplot(data=data.melt(id_vars=['Account Type'], value_vars=['Credit', 'Debit']),
            x='Account Type', y='value', hue='variable')
plt.yscale('log')
plt.title('Comparative Analysis of Credit and Debit Transactions by Account Type')
plt.ylabel('Transaction Amount (log scale)')
plt.xlabel('Account Type')
plt.legend(title='Transaction Type')
plt.tight_layout()
plt.show()

