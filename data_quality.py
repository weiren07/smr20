# -*- coding: utf-8 -*-
"""data quality.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fVPy3U0AfOeVzpm9EM6lfCzkEVABcuge
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import pyplot
from pandas import read_csv
# Load the sales dataset into a pandas dataframe
df = pd.read_csv('sample.csv')
# replaced dataset it with a file hosted on Eileen's github so there's no need to upload the dataset every time.

# print the DataFrame to confirm that the header row was used correctly
print(df.head())

# Check the data types and missing values
df.info()

# print the number of null values in each column
print(df.isnull().sum())

#review dimension of data
shape = df.shape
print(shape)

#Data Types for Each Attribute
types = df.dtypes
print(types)

# remove rows with missing values
df = df.dropna()

#review dimension of data
shape = df.shape
print(shape)

from prettytable import PrettyTable




# create a list of numeric column names
numeric_cols = ['usd/rm price', 'wti price','SMR20']

# create a table for numeric columns
numeric_table = PrettyTable()
numeric_table.field_names = ['Column', 'Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max']
for col in numeric_cols:
    numeric_table.add_row([col, df[col].count(), df[col].mean(), df[col].std(), df[col].min(), df[col].quantile(0.25), df[col].quantile(0.5), df[col].quantile(0.75), df[col].max()])

# create a table for categorical columns
table = PrettyTable()
table.field_names = ['Column', 'Count', 'Unique']
for col in df.columns:
    if col not in numeric_cols:
        table.add_row([col, df[col].count(), df[col].nunique()])

# display tables for categorical and numeric columns
print("Categorical columns:")
print(table)
print("Numeric columns:")
print(numeric_table)

# check if all dates are unique
if len(df['date'].unique()) == len(df):
    print("All dates are unique")
else:
    duplicates = df[df.duplicated(['date'])]['date'].unique()
    print("The following dates are not unique:", duplicates)

# remove duplicates
df.drop_duplicates(subset='date', inplace=True)

#review dimension of data
shape = df.shape
print(shape)

from prettytable import PrettyTable




# create a list of numeric column names
numeric_cols = ['usd/rm price', 'wti price','SMR20']

# create a table for numeric columns
numeric_table = PrettyTable()
numeric_table.field_names = ['Column', 'Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max']
for col in numeric_cols:
    numeric_table.add_row([col, df[col].count(), df[col].mean(), df[col].std(), df[col].min(), df[col].quantile(0.25), df[col].quantile(0.5), df[col].quantile(0.75), df[col].max()])

# create a table for categorical columns
table = PrettyTable()
table.field_names = ['Column', 'Count', 'Unique']
for col in df.columns:
    if col not in numeric_cols:
        table.add_row([col, df[col].count(), df[col].nunique()])

# display tables for categorical and numeric columns
print("Categorical columns:")
print(table)
print("Numeric columns:")
print(numeric_table)

# remove rows that contain negative values in any of the three columns
df = df[(df[['usd/rm price', 'wti price', 'SMR20']] >= 0).all(axis=1)]

import matplotlib.pyplot as plt

# Plot histograms for each numerical column
fig, axs = plt.subplots(3, figsize=(5,10))

# USD/RM price
axs[0].hist(df['usd/rm price'], bins=50, color='blue', alpha=0.7)
axs[0].set_title('USD/RM Price Distribution')

# WTI price
axs[1].hist(df['wti price'], bins=50, color='green', alpha=0.7)
axs[1].set_title('WTI Price Distribution')

# SMR20
axs[2].hist(df['SMR20'], bins=50, color='red', alpha=0.7)
axs[2].set_title('SMR20 Price Distribution')

plt.tight_layout()
plt.show()

# Function to calculate outliers using the IQR method
def calculate_outliers_iqr(df):
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1

    # Define the upper and lower bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify the outliers
    outliers = df[(df < lower_bound) | (df > upper_bound)]
    return outliers

# Calculate outliers for each numerical column
outliers_usd_rm_price = calculate_outliers_iqr(df['usd/rm price'])
outliers_wti_price = calculate_outliers_iqr(df['wti price'])
outliers_smr20 = calculate_outliers_iqr(df['SMR20'])

# Print the number of outliers in each column
len(outliers_usd_rm_price), len(outliers_wti_price), len(outliers_smr20)

df.to_csv('modi_data.csv', index=False)

import pandas as pd
from scipy.stats import boxcox

# apply the Box-Cox transformation to the selected columns
for col in numeric_cols:
    transformed_data, lambda_value = boxcox(df[col])
    df[col] = transformed_data

# print the transformed dataframe
print(df)

#Univariate Histogram
df.hist(bins=10, figsize=(15,10))
plt.show()

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
df.plot(kind='density', subplots=True, layout=(4, 3), sharex=False, figsize=(14, 10))
plt.show()

# correlation matrix
corr_matrix = df.corr()
sns.heatmap(corr_matrix, annot=True)
plt.title('Correlation Matrix')
plt.show()