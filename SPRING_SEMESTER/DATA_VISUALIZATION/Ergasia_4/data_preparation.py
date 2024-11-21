import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("final_demographics_data.csv")

print(df.shape)
print(df.columns)
print(len(df.columns))
print(df.isnull().sum())

missing_values = df.isnull().sum()
missing_cols = missing_values[missing_values > 0].index
missing_df = df[missing_cols]
missing_values = missing_df.isnull().sum()

plt.bar(x=missing_values.index, height=missing_values.values)
plt.xticks(rotation=90)
plt.xlabel("Columns")
plt.ylabel("Number of missing values")
plt.title('Missing Values by Column')
#plt.show()

df_filtered = df.dropna()
print(df_filtered.isnull().sum())
print(df_filtered.shape)
# Although there are null values in the dataset we won't drop the rows that contain,
# these null values because we would end up with no rows at all.
# Instead, we will replace null values with 0
df.fillna(0, inplace=True)
print(df.isnull().sum())

# No we will normalize the values by dividing the values of each column with the biggest value of that column
# let's see what type of data we have in our columns first
print(df.info())
for i in range(len(df.columns)):
    try:
        df.iloc[:, i] = df.iloc[:, i]/df.iloc[:, i].max()
    except:
        continue

print(df["Age dependency ratio, young (% of working-age population)"].head())
#df.to_csv("my_dataframe.csv", index=False)
#df.to_excel("my_dataframe.xlsx", index=False, sheet_name="Dataset")
# GDP Growth annual - Gun Imports
# Hiv of young adults - Smthing else
# population male, population female - GDP
