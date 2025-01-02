import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set up Streamlit page layout
st.set_page_config(page_title="Transaction Data Dashboard", layout="wide")

# Load the dataset
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.sidebar.title("Options")

    # Sidebar filters
    regions = data['Region'].unique()
    selected_region = st.sidebar.selectbox("Select Region", ["All"] + list(regions))

    # Filter data by selected region
    if selected_region != "All":
        data = data[data['Region'] == selected_region]

    # Task 1: Account Type Distribution
    st.subheader("1. Account Type Distribution")
    account_type_distribution = data['Account Type'].value_counts(normalize=True)
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    account_type_distribution.plot.pie(
        autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, ax=ax1
    )
    ax1.set_ylabel('')
    ax1.set_title("Distribution of Account Types")
    st.pyplot(fig1)

    # Task 2: Transaction Flow by Beneficiary Bank
    st.subheader("2. Top 5 Beneficiary Banks by Region")
    transaction_flow = data.groupby(['Region', 'Transaction To'])['Credit'].sum().reset_index()
    top_beneficiary_banks = transaction_flow.groupby('Region').apply(
        lambda x: x.nlargest(5, 'Credit')).reset_index(drop=True)

    fig2, ax2 = plt.subplots(figsize=(12, 8))
    sns.barplot(data=top_beneficiary_banks, x='Region', y='Credit', hue='Transaction To', ax=ax2)
    ax2.set_title('Top 5 Beneficiary Banks by Region (Credit Transactions)')
    ax2.set_ylabel('Credit Amount')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    ax2.legend(title='Beneficiary Bank', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig2)

    # Task 3: Geographic Heatmap of Transactions
    st.subheader("3. Geographic Heatmap of Transactions")
    transaction_intensity = data.groupby('Region')[['Credit', 'Debit']].sum().reset_index()
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.heatmap(transaction_intensity.set_index('Region')[['Credit', 'Debit']],
                annot=True, fmt=".2f", cmap='Blues', ax=ax3)
    ax3.set_title('Geographic Heatmap of Transaction Intensity')
    st.pyplot(fig3)

    # Task 4: Anomalies in Transactions
    st.subheader("4. Anomalies in Transactions")
    data['Credit_Z'] = (data['Credit'] - data['Credit'].mean()) / data['Credit'].std()
    data['Debit_Z'] = (data['Debit'] - data['Debit'].mean()) / data['Debit'].std()
    anomalies = data[(data['Credit_Z'].abs() > 3) | (data['Debit_Z'].abs() > 3)]

    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=data, x='Credit', y='Debit', alpha=0.5, label='Normal', ax=ax4)
    sns.scatterplot(data=anomalies, x='Credit', y='Debit', color='red', label='Anomaly', s=50, ax=ax4)
    ax4.set_title('Anomalies in Transactions')
    ax4.set_xlabel('Credit')
    ax4.set_ylabel('Debit')
    ax4.legend()
    st.pyplot(fig4)

    # Task 5: Comparative Analysis of Transaction Types
    st.subheader("5. Comparative Analysis of Transaction Types")
    fig5, ax5 = plt.subplots(figsize=(12, 8))
    sns.boxplot(data=data.melt(id_vars=['Account Type'], value_vars=['Credit', 'Debit']),
                x='Account Type', y='value', hue='variable', ax=ax5)
    ax5.set_yscale('log')
    ax5.set_title('Comparative Analysis of Credit and Debit Transactions by Account Type')
    ax5.set_ylabel('Transaction Amount (log scale)')
    ax5.set_xlabel('Account Type')
    ax5.legend(title='Transaction Type')
    st.pyplot(fig5)

    # Footer
    st.markdown("**Note:** Tasks involving time-based analysis and customer insights were skipped due to missing relevant columns.")
