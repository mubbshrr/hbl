import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore

# Load the data
data_path = 'Enhanced_Dummy_HBL_Data(1).csv'  # Update with the correct file path
df = pd.read_csv(data_path)

# Title for the dashboard
st.title("Interactive Dashboard for Transaction Data")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio(
    "Select a Visualization:",
    (
        "Account Type Distribution",
        "Transaction Flow by Beneficiary Bank",
        "Geographic Heatmap of Transactions",
        "Anomalies in Transactions",
        "Comparative Analysis of Transaction Types",
    ),
)

if options == "Account Type Distribution":
    st.header("Account Type Distribution")
    account_type_distribution = df['Account Type'].value_counts()

    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    account_type_distribution.plot.pie(
        autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors, ax=ax
    )
    ax.set_title("Account Type Distribution")
    ax.set_ylabel('')
    st.pyplot(fig)

elif options == "Transaction Flow by Beneficiary Bank":
    st.header("Top 5 Beneficiary Banks by Region")
    # Group and sort data
    top_beneficiary_banks = (
        df.groupby(['Region', 'Transaction To'])['Credit']
        .sum()
        .reset_index()
        .sort_values(by='Credit', ascending=False)
    )
    top_5_per_region = top_beneficiary_banks.groupby('Region').head(5)

    # Plot the bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    for region in top_5_per_region['Region'].unique():
        region_data = top_5_per_region[top_5_per_region['Region'] == region]
        ax.bar(region_data['Transaction To'], region_data['Credit'], label=region)

    ax.set_title("Top 5 Beneficiary Banks with Highest Credit Transactions by Region")
    ax.set_xlabel("Beneficiary Bank")
    ax.set_ylabel("Total Credit (in currency units)")
    ax.legend(title="Region")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

elif options == "Geographic Heatmap of Transactions":
    st.header("Geographic Heatmap of Transactions")
    # Aggregate transaction intensity
    transaction_intensity = df.groupby('Region')[['Credit', 'Debit']].sum().reset_index()
    transaction_intensity['Total Transactions'] = (
        transaction_intensity['Credit'] + transaction_intensity['Debit']
    )

    # Plot the heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    heatmap_data = transaction_intensity.set_index('Region')[['Total Transactions']]
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt='.2f',
        cmap='YlGnBu',
        cbar_kws={'label': 'Transaction Intensity'},
        ax=ax,
    )
    ax.set_title("Geographic Heatmap of Transaction Intensity by Region")
    st.pyplot(fig)

elif options == "Anomalies in Transactions":
    st.header("Anomalies in Transactions")
    # Calculate Z-scores and identify outliers
    df['Credit Z-Score'] = zscore(df['Credit'])
    df['Debit Z-Score'] = zscore(df['Debit'])
    outliers = df[(df['Credit Z-Score'].abs() > 3) | (df['Debit Z-Score'].abs() > 3)]

    # Plot anomalies
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(df.index, df['Credit'], label='Credit', alpha=0.5)
    ax.scatter(df.index, df['Debit'], label='Debit', alpha=0.5)
    ax.scatter(outliers.index, outliers['Credit'], color='red', label='Credit Outliers', edgecolor='k')
    ax.scatter(outliers.index, outliers['Debit'], color='orange', label='Debit Outliers', edgecolor='k')
    ax.set_title("Anomalies in Credit and Debit Transactions")
    ax.set_xlabel("Transaction Index")
    ax.set_ylabel("Transaction Amount")
    ax.legend()
    st.pyplot(fig)

elif options == "Comparative Analysis of Transaction Types":
    st.header("Comparative Analysis of Transaction Types")
    # Melt the data for visualization
    melted_df = df.melt(
        id_vars=['Account Type'], value_vars=['Credit', 'Debit'],
        var_name='Transaction Type', value_name='Amount'
    )

    # Plot the boxplot
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=melted_df, x='Account Type', y='Amount', hue='Transaction Type', ax=ax)
    ax.set_yscale('log')
    ax.set_title("Comparative Analysis of Credit and Debit Transactions by Account Type")
    ax.set_xlabel("Account Type")
    ax.set_ylabel("Transaction Amount (log scale)")
    ax.legend(title="Transaction Type")
    st.pyplot(fig)

st.sidebar.info("Use the navigation panel to explore different visualizations.")
