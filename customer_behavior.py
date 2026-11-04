import pandas as pd
import numpy as np

#Reading and storing the dataset in a variable.
df=pd.read_csv('customer_shopping_behavior.csv')
df.head()

#Get the information of data such as colunm names and data type of each column
df.info()

#Checking the null values in data.
df.isnull().sum()

#Removing the null values in Review Rating column by median but category wise.
df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
df.isnull().sum()

#Changing the column names in snake case
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
df.columns

#Feature Engineering
#Creating new age group column
df['age_group']=pd.qcut(df['age'],q=4,labels=['Young Adult','Adult','Middle Aged','Senior'])
df[['age_group','age']]

#Creating purchase_frequency_days column
frequency_mapping={
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Months':90
}
df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)
df[['purchase_frequency_days','frequency_of_purchases']]

#Handling similar columns
(df['promo_code_used']==df['discount_applied']).all
#since both columns carry same information do we'll drop one of the columns
df.drop('promo_code_used',axis=1)
df.info()

from sqlalchemy import create_engine

server = "ANAND_SIRJI\MSSQL"
database = 'customer_behavior'

engine = create_engine(
    f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

table_name="customer_shopping_behavior"
df.to_sql(table_name,engine,if_exists="replace",index='False')
print(f"Data Successfully loaded into table '{table_name}' in database '{database}'.")