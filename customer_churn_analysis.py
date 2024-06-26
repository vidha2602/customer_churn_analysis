# -*- coding: utf-8 -*-
"""Customer Churn Analysis.ipynb

Automatically generated by Colab.


from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
df=pd.read_excel("/content/drive/MyDrive/E Commerce Dataset.xlsx")

df.head(5)

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import plotly.graph_objs as go
import plotly.express as ex
import plotly. figure_factory as ff
from plotly.subplots import make_subplots
import seaborn as sns
from scipy.stats import chi2

df.duplicated().sum()

for i in df.columns:
  if df[i].isnull().sum()>0:
    print(i)
    print(f'The total null values in {i} is', df[i].isnull().sum())
    print('The data type', df[i].dtypes)
    print()

df.shape

#Repacing nan values with the median

for column in df.columns:
  if df[column].isnull().sum()>0:
    df[column].fillna(df[column].median(), inplace=True)

df.isnull().sum()

for column in df.columns:
  if df[column] .dtype=='object':
    print(df[column].value_counts())
    print()
    print()

df['PreferredLoginDevice']=df['PreferredLoginDevice' ].replace("Phone", "Mobile Phone")
df['PreferredPaymentMode']= df[ 'PreferredPaymentMode'].replace(['CC', 'COD'],['Credit Card', 'Cash on Delivery'])
df['PreferedOrderCat']=df[ 'PreferedOrderCat']. replace("Mobile", "Mobile Phone")

"""# **What is the impact of a customer's duration on their chance of leaving?**"""

# Calculate the churn and non-churn counts
churn_count = df[df['Churn'] == 1].CustomerID.nunique()
non_churn_count = df[df['Churn'] == 0].CustomerID.nunique()

# Set up the plot size and title
plt.figure(figsize=(8, 6))
plt.title('Churn Rate')

# Set the colors for the chart section
colors = ['skyblue', 'salmon']

# Create the pie chart
plt.pie([churn_count, non_churn_count], labels=['Churn', 'Non-Churn'], autopct='%1.1f%%', colors=colors)

# Display the plot
plt.show()

# Create a correlation matrix
corr_matrix = df.corr()

# Set up the plot size
sns.set(rc={'figure.figsize':(10,8)})

# Plot the correlation matrix as a heatmap
sns.heatmap(corr_matrix, cmap='coolwarm')
plt.title('Correlation Matrix')

# Display the plot
plt.show()

# Calculate pairwise correlation values between 'churn' column and all other columns
corr_churn = df.corr()['Churn']

# Load your correlation data into a pandas dataframe
corr_df = pd.DataFrame({'Feature': corr_churn.index, 'Correlation': corr_churn.values})

# Remove the 'Churn' feature from the dataframe
corr_df = corr_df[corr_df['Feature'] != 'Churn']

# Sort the dataframe by correlation values
sorted_corr_df = corr_df.sort_values(by='Correlation')

# Extract the feature names and correlation values as numpy arrays
features = sorted_corr_df['Feature'].values
corr_values = sorted_corr_df['Correlation'].values

# Assign colors to the bars based on their values
colors = np.where(corr_values > 0, 'seagreen', 'firebrick')

# Set the figure size
fig, ax = plt.subplots(figsize=(8, 10))

# Plot the horizontal bar chart
ax.barh(features, corr_values, color=colors)

# Add labels and title to the plot
ax.set_xlabel('Correlation')
ax.set_ylabel('Feature')
ax.set_title('Correlation with Churn')

plt.show()

"""The positive correlation of the "Complain" feature with churn means that customers who are having complaints are more likely to churn than customers who don't have any.
The negative correlation of "tenure" with churn means that the longer a customer has been with a provider, the less likely they are to churn.
"""

# Create correlation between Churn and other features ordered
#  by absolute correlation descending

# Load your correlation data into a pandas dataframe
corr_df = pd.DataFrame({'Feature': corr_churn.index, 'Correlation': corr_churn.values})

# Remove the 'Churn' feature from the dataframe
corr_df = corr_df[corr_df['Feature'] != 'Churn']

# Round correlation values
corr_df['Correlation'] = round(corr_df['Correlation'], 2)

# Add a new column with absolute correlation values
corr_df['Abs_Correlation'] = abs(corr_df['Correlation'])

# Sort the dataframe by absolute correlation values
sorted_corr_df = corr_df.sort_values(by='Abs_Correlation', ascending=False).reset_index(drop=True)

# Display the sorted dataframe
sorted_corr_df[['Feature', 'Correlation']].head(10)

df.head(5)

avg_tenure=df.groupby('Churn')['Tenure'].mean ()
plt.figure(figsize=(8,5))
sns.barplot(x=avg_tenure.index, y=avg_tenure. values)
# Adding the text on the bars
for index, value in enumerate(avg_tenure) :
  plt.text(index, value, f'{value: 2f}', ha='center', va='bottom')
plt.title('Average Customer Tenure by Churn')
plt.xlabel ('Churn')
plt.ylabel('Average Tenure')
plt.xticks([0,1],['Retained', 'Churned' ])
plt. show()

"""*Customers who remain with the service normally have a longer tenure, but those that depart (churn) usually do so after a shorter term. This contrast
is clearly illustrated by the bar chart.*

*This suggests that consumers who use the service for a longer amount of time are less likely to churn because there is a strong correlation between tenure and churn.*

*This knowledge can be extremely helpful in creating strategies to improve customer retention, like emphasising early engagement and retention initiatives for more recent clients.*

# **Is there a relationship between the preferred login device and churn rate?**
"""

# Cross-tabulation
cross_tab = pd.crosstab(df[ 'PreferredLoginDevice'], df[ 'Churn' ])
# Chi-square test of independence to see if there is a significant relationship
from scipy.stats import chi2_contingency
chi2, p, dof, expected = chi2_contingency(cross_tab)
# Visualizing the cross-tabulation
plt.figure(figsize=(8, 6))
sns.heatmap(cross_tab, annot=True, fmt='d', cmap='viridis')
plt.title('Cross-Tabulation of PreferredLoginDevice and Churn')
plt.xlabel ('Churn')
plt.ylabel('Preferred Login Device')
plt.show()

device_churn_percentage = pd.crosstab(df['PreferredLoginDevice'],df['Churn'],normalize='index') * 100
device_churn_percentage = device_churn_percentage.round(2)
device_churn_percentage

"""*These figures imply that:*

*In comparison to customers who prefer mobile phones (15.62%), those who prefer using a computer for login have a significantly higher turnover rate (19.83%).*
*On the other hand, users of mobile phones exhibit a greater retention rate.*

# **Is there a relationship between the city tier and churn rate?**
"""

city_churn_percentage = pd.crosstab(df['CityTier'],df['Churn'],normalize='index') * 100
city_churn_percentage = city_churn_percentage.round(2)
city_churn_percentage

"""*The greatest rate of customer retention and the lowest percentage of customer churn are seen in City Tier 1.*

*The retention rate falls and the churn rate increases as the city tier reaches 2 and 3.*

# **Does the preferred payment mode have any correlation with customer churn?**
"""

payment_mode_churn_percentage = pd.crosstab(df['PreferredPaymentMode'], df['Churn'], normalize='index') * 100
payment_mode_churn_percentage = payment_mode_churn_percentage.round(2)

plt.figure(figsize=(16, 10))
ax = payment_mode_churn_percentage.plot(kind='bar', color=['skyblue', 'salmon'], width=0.8)

# Adding percentage values on top of the bars
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}%',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10),
                textcoords='offset points')

plt.title('Churn Percentage by Preferred Payment Mode', size=16)
plt.xlabel('Preferred Payment Mode', size=14)
plt.ylabel('Percentage (%)', size=14)
plt.xticks(rotation=45)
plt.legend(title='Churn', labels=['Not Churned', 'Churned'], loc='upper left', bbox_to_anchor=(1, 1), fontsize='medium')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

"""*This visualisation makes it clear that:*

*The biggest churn rate is seen among Cash on Delivery users (24.90%), E wallet users (22.80%), and UPI users (17.39%).
Users of debit and credit cards have reduced churn rates—14.21% and 15.38%, respectively.*

# **Is there a gender disparity in the churn rates?**
"""

gender_percentage = pd.crosstab(df['Gender'], df['Churn'], normalize='index') * 100
gender_percentage = gender_percentage.round(2)

plt.figure(figsize=(16, 10))
ax = gender_percentage.plot(kind='bar', color=['skyblue', 'salmon'], width=0.8)

# Adding percentage values on top of the bars
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}%',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10),
                textcoords='offset points')

plt.title('Churn Percentage by Gender', size=16)
plt.xlabel('Gender', size=14)
plt.ylabel('Percentage (%)', size=14)
plt.xticks(rotation=45)
plt.legend(title='Churn', labels=['Not Churned', 'Churned'], loc='upper left', bbox_to_anchor=(1, 1), fontsize='medium')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

"""*The churn rate for male customers is slightly greater (17.73%) than that of female customers (15.49%).*

*This insight can be important for developing gender-specific customer engagement and retention strategies.*

# **How does marital status impact the likelihood of churn?**
"""

marital_status_percentage = pd.crosstab(df['MaritalStatus'], df['Churn'], normalize='index') * 100
marital_status_percentage = marital_status_percentage.round(2)

plt.figure(figsize=(16, 10))
ax = marital_status_percentage.plot(kind='bar', color=['skyblue', 'salmon'], width=0.8)

# Adding percentage values on top of the bars
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}%',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10),
                textcoords='offset points')

plt.title('Churn Percentage by Marital Status', size=16)
plt.xlabel('Gender', size=14)
plt.ylabel('Percentage (%)', size=14)
plt.xticks(rotation=45)
plt.legend(title='Churn', labels=['Not Churned', 'Churned'], loc='upper left', bbox_to_anchor=(1, 1), fontsize='medium')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

"""*This suggests that marital status is a relevant factor in customer churn, with different marital statuses showing distinct churn behaviours.*

*Single customers have a significantly higher churn rate (26.73%) compared to married (11.52%) and divorced (14.62%) customers.*

# **Are the satisfaction ratings of churning and non-churning consumers significantly different?**
"""

# Analyzing the difference in satisfaction scores between customers who churn and those who don't
satisfaction_churn_comparison = df.groupby('Churn') ['SatisfactionScore']. mean()
satisfaction_churn_comparison = satisfaction_churn_comparison.round(2)

# Conducting a t-test to determine if the difference is statistically significant
from scipy.stats import ttest_ind

# Separating the data into two groups: churned and not churned
satisfaction_churned = df[df[ 'Churn'] == 1][ 'SatisfactionScore']
satisfaction_not_churned = df[df[ 'Churn'] == 0]['SatisfactionScore']

# Performing the t-test
t_stat, p_value = ttest_ind(satisfaction_churned, satisfaction_not_churned)
satisfaction_churn_comparison, p_value

plt. figure(figsize=(12, 6))
# Plot for customers who did not churn
plt.subplot (1, 2, 1)
sns.countplot(x='SatisfactionScore', data=df[df[ 'Churn'] == 0], palette='Set2')
plt.title('Satisfaction Scores for Non-Churned Customers')
plt.xlabel( 'Satisfaction Score')
plt.ylabel('Count')
# Plot for customers who churned
plt.subplot (1, 2, 2)
sns.countplot(x='SatisfactionScore', data=df[df['Churn'] == 1], palette='Set1')
plt.title('Satisfaction Scores for Churned Customers')
plt.xlabel('Satisfaction Score')
plt.ylabel( 'Count')
plt.tight_layout()
plt.show()

"""*Surprisingly, the average satisfaction score is higher for customers who churned compared to those who didn’t. This might suggest that factors other than satisfaction scores are influencing the decision to churn, or that the satisfaction scores may not fully capture the customer’s experience or likelihood to remain with the service.*

# **Do customers who complain have a higher churn rate?**
"""

Complain_percentage = pd.crosstab(df['Complain'], df['Churn'], normalize='index') * 100
Complain_percentage = Complain_percentage.round(2)

plt.figure(figsize=(16, 10))
ax = Complain_percentage.plot(kind='bar', color=['skyblue', 'salmon'], width=0.8)

# Adding percentage values on top of the bars
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}%',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10),
                textcoords='offset points')

plt.title('Churn Percentage by Complains', size=16)
plt.xlabel('Complain', size=14)
plt.ylabel('Percentage (%)', size=14)
plt.xticks(rotation=45)
plt.legend(title='Churn', labels=['Not Churned', 'Churned'], loc='upper left', bbox_to_anchor=(1, 1), fontsize='medium')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

"""*This shows that complaints from customers are a strong predictor of churn risk and emphasises how crucial it is to successfully handle customer concerns in order to increase retention.*

# **Does the duration since a customer’s last order predict churn?**
"""

# Analyzing the relationship between the duration since a customer's last order and churn
# Grouping data by 'DaySinceLastOrder' and calculating the churn rate for each group
last_order_churn_rate = df.groupby('DaySinceLastOrder')['Churn'].mean () * 100
# Creating a plot to visualize the relationship
plt. figure(figsize=(12, 6))
last_order_churn_rate.plot(kind='bar', color='orange')
plt.title('Churn Rate bv Davs Since Last Order',size=16)
plt.xlabel('Days Since Last Order', size=14)
plt.ylabel('Churn Rate (%)', size=14)
plt.xticks(rotation=90)
plt.grid(axis='y', alpha=0.7)
plt. show()

#last_order_churn_rate

"""*These observations suggest that the duration since a customer’s last order can be a predictor of churn, particularly in the immediate days following an order. The trend indicates that customers are more likely to churn shortly after placing an order, with the likelihood decreasing as more time passes. This insight can inform strategies for engaging customers at critical times to reduce the likelihood of churn.*

# **Are certain product categories (PreferredOrderCat) more prone to leading to churn?**
"""

PreferredOrderCat_percentage = pd.crosstab(df['PreferedOrderCat'], df['Churn'], normalize='index') * 100
PreferredOrderCat_percentage = PreferredOrderCat_percentage.round(2)

plt.figure(figsize=(16, 10))
ax = PreferredOrderCat_percentage.plot(kind='bar', color=['skyblue', 'salmon'], width=0.8)

# Adding percentage values on top of the bars
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}%',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10),
                textcoords='offset points')

plt.title('Churn Percentage by product categories', size=16)
plt.xlabel('Product Category', size=14)
plt.ylabel('Percentage (%)', size=14)
plt.xticks(rotation=45)
plt.legend(title='Churn', labels=['Not Churned', 'Churned'], loc='upper left', bbox_to_anchor=(1, 1), fontsize='medium')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

"""*Customers who prefer ordering Mobile Phones have the highest churn rate (27.40%), which is significantly higher compared to other categories.
The Grocery category shows the lowest churn rate (4.88%), suggesting high customer retention in this category.*

# **How do various cashback amounts influence churn behaviour?**
"""

# Since 'CashbackAmount' is a continuous variable, we'll create bins to categorize the data for analysis
df['CashbackAmountBin'] = pd.cut(df['CashbackAmount'], bins=[0, 50, 100, 150, 200, 250, 300, df['CashbackAmount'].max()])

# Grouping data by these cashback amount bins and calculating the churn rate for each bin
cashback_churn_rate = pd.crosstab(df[ 'CashbackAmountBin'], df['Churn'], normalize='index') * 100
cashback_churn_rate = cashback_churn_rate.round(2)

# Creating a bar plot to visualize the relationship
plt. figure(figsize=(12, 6))
cashback_churn_rate.plot(kind='bar', stacked=False, color=['lightblue', 'coral'], ax=plt.gca())
plt.title('Churn Rate by Cashback Amount', size=16)
plt.xlabel('Cashback Amount Bin', size=14)
plt.ylabel( 'Percentage (%)', size=14)
plt.xticks(rotation=45)
plt.legend(title='Churn', labels=['Not Churned', 'Churned'], loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(axis='y', linestyle='--' , alpha=0.7)
plt. show()

"""*The increase in churn rate for cashback amounts between $100 and $150 is particularly notable. Higher cashback amounts (above $300) are associated with lower churn rates, indicating that more generous cashback offers might contribute to higher customer retention.*

"""

#Creating a crosstab to analyze churn rate by the combination of gender and marital status

gender_marital_status_churn = pd.crosstab(index=[df[ 'Gender'], df['MaritalStatus']],columns=df['Churn'],normalize='index') * 100
gender_marital_status_churn=gender_marital_status_churn.round(2)
gender_marital_status_churn

# Creating a stacked bar plot to visualize this relationship
gender_marital_status_churn.plot(kind='bar',stacked=False, figsize =(12,6),color=['skyblue','salmon'])
plt.title('Churn rate by Gender and Marital status' ,size=16)
plt.xlabel('Gender and Marital Status', size=14)
plt.ylabel('Percentage (%)', size=14)
plt.xticks (rotation=45)
plt.legend(title='Churn', labels=['Not Churned', 'Churned'])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

"""*In general, single customers (both male and female) have higher churn rates compared to married and divorced customers.
There is a noticeable difference in churn rates between genders within the same marital status category, particularly among single customers.*

# **Are there patterns of churn when considering both the number of hours spent on the app and the satisfaction score?**
"""

# Creating bins for hours spent on the app for easier analysis
df['HourSpendOnAppBin'] = pd.cut(df['HourSpendOnApp'], bins=[0, 1, 2, 3, 4, df['HourSpendOnApp'].max()],include_lowest=True, right=False)

# Creating a crosstab to analyze churn rate by the combination of hours spent on the app and satisfaction score
hours_satisfaction_churn = pd.crosstab(index=[df['HourSpendOnAppBin'],df['SatisfactionScore']], columns=df['Churn'], normalize='index') * 100
hours_satisfaction_churn = cashback_churn_rate.round(2)

# Creating a visualization for this relationship
hours_satisfaction_churn.plot(kind='bar', stacked=False, figsize=(14, 8), color=['lightblue', 'coral'])
plt.title('Churn Rate by Hours Spent on App and Satisfaction Score', size=16)
plt.xlabel('Hours spent and Satisfaction score', size=14)
plt.ylabel( 'Percentage (%)', size=14)
plt.xticks(rotation=90)

"""*Each bar represents a specific combination, such as “0–1 hours & Satisfaction Score 1” or “3–4 hours & Satisfaction Score 5”.
It is clear that people who spent more than hour and irrespective of Satisfaction score observe Churning*

# **Does the duration since the last order and the number of complaints lodged have a combined effect on churn?**
"""

# Grouping data by 'DaySinceLastOrder' and 'Complain' and calculating the churn rate for each group
duration_complaints_churn = pd.crosstab(index=[df['DaySinceLastOrder'], df['Complain']],columns=df[ 'Churn'],normalize='index') * 100
duration_complaints_churn = duration_complaints_churn.round(2)
# Displaying the results in a tabular format
duration_complaints_churn

"""*Immediate post-order periods combined with customer complaints are critical windows where churn risk is heightened, highlighting the importance of prompt and effective complaint resolution and customer engagement strategies.*"""

# Creating bins for cashback amounts for easier analysis
df['CashbackAmountBin'] = pd.cut(df['CashbackAmount'], bins=[0, 50, 100, 150, 200, 250, 300, df['CashbackAmount'].max()], include_lowest=True, right=False)

# Creating a crosstab to analyze churn rate by the combination of preferred order category and cashback amount bin
order_cat_cashback_churn = pd.crosstab(index=[df['PreferedOrderCat'],df['CashbackAmountBin']],columns=df['Churn'],normalize='index') * 100
order_cat_cashback_churn = order_cat_cashback_churn.round(2)

# Displaying the results in a tabular format
order_cat_cashback_churn

"""*Fashion Category:*
*Customers receiving cashback between 100 and 150 have a 0% churn rate.
Churn rates increase slightly with higher cashback amounts, reaching 16.47% for the $150 to $200 range.*

*Grocery Category:*

*Churn is nonexistent (0%) for cashback amounts below 50 and above 300.
*Moderate churn rates are observed for cashback amounts between 200 and 250 (13.19%).*

*Laptop & Accessory Category:*
*No churn for cashback amounts below $50.*
*Churn rates range from 10.46% to 14.81% for higher cashback amounts.*

*Mobile Phone Category:*
*Churn rate is 0% for cashback amounts below 100.*
*A notable increase in churn rate is observed for cashback amounts between 100 and 150 (30.10%).*

*Others Category:*
*Churn rates are relatively low, around 7.58% to 7.69% for cashback amounts between 250 and 325.*

These figures indicate that the churn rate varies significantly across different combinations of preferred order categories and cashback amount bins. In some categories, such as Mobile Phones, higher cashback amounts correlate with higher churn rates, while in others, such as Fashion and Grocery, the pattern is less clear. This suggests that the impact of cashback on churn may depend on the type of products customers are purchasing, and different strategies might be needed for different categories to optimize customer retention.

# **Does the combination of customer tenure and satisfaction score lead to varying churn rates?**
"""

# Creating bins for cashback amounts for easier analysis
df['TenureBin'] = pd.cut(df['Tenure'], bins=[0, 1, 2, 3, 4, 5, df['Tenure'].max()], include_lowest=True, right=False)

# Creating a crosstab to analyze churn rate by the combination of preferred order category and cashback amount bin
tenure_satisfaction_churn = pd.crosstab(index=[df['TenureBin'],df['SatisfactionScore']],columns=df['Churn'],normalize='index') * 100
tenure_satisfaction_churn = tenure_satisfaction_churn.round(2)

# Displaying the results in a tabular format
tenure_satisfaction_churn

"""*In general, lower churn rates across all satisfaction metrics are correlated with longer tenure.*
*Increased customer happiness scores are correlated with increased churn, suggesting that customer satisfaction has a more noticeable effect on attrition in shorter tenure bins.*

*These findings indicate that customer tenure greatly impacts retention, showing that longer-tenured customers tend to have lower churn rates regardless of satisfaction levels. Conversely, shorter-tenured customers are more likely to churn, emphasizing the importance of early satisfaction and engagement strategies.*

# **What are the churn rates for different combinations of Gender, City Tier, and Marital Status?**
"""

gender_citytier_marital_grouped=df.groupby(['Gender','CityTier','MaritalStatus'])

# Total customers in each group
total_customers = gender_citytier_marital_grouped.size().reset_index(name='Total Customers')

# Total churn numbers in each group (where Churn=1 indicates churned customers)
churn_numbers = gender_citytier_marital_grouped['Churn'].sum().reset_index(name='Churn Numbers')

# Merging the total customers and churn numbers
merged_data = total_customers.merge(churn_numbers, on=['Gender', 'CityTier', 'MaritalStatus'])

# Calculating churn ratio
merged_data ['Churn Ratio']= merged_data[ 'Churn Numbers'] / merged_data['Total Customers']

# Calculating not churn numbers (Total - Churn)
merged_data['Not Churn Numbers'] = merged_data['Total Customers'] - merged_data[ 'Churn Numbers']
merged_data

"""*This table shows churn ratios for different combinations of Gender, City Tier, and Marital Status.*
*Churn rates vary across different groups:*

*For females in City Tier 1, the highest churn ratio is among singles (17.21%).*

*Among males in City Tier 1, singles also show the highest churn ratio (26.87%).*

*In City Tier 2, females who are married exhibit the highest churn ratio (45.83%).*

*For males in City Tier 3, singles have the highest churn ratio (32.14%).*

# **Modelling**
"""

pip install shap

# Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
import xgboost as xgb
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix, f1_score, roc_curve, auc
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
import shap
import joblib

# Drop the column and save it to a variable
#   If you need to bring the column back later, simply reassign it to the DataFrame
#   df['customerID'] = customer_id
customer_id = df.pop('CustomerID')

# Separate the target variable (Churn) from the rest of the dataset
X = df.drop('Churn', axis=1)
y = df['Churn']

"""**Balancing our training dataset**

*   SMOTE (Synthetic Minority Over-sampling Technique) - used for data upsampling in machine learning. It creates synthetic samples of the minority class by creating new observations that are similar to existing observations, thus balancing the class distribution. We can perform data upsampling using SMOTE in Python with the imbalanced-learn library. Balancing your dataset with SMOTE should be performed on the training set only.



"""

df.head(5)

unique_entries = df['PreferredLoginDevice'].unique()
unique_entries

y = df["Churn"]  # Target variable

# One-hot encode categorical variables
X = pd.get_dummies(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply SMOTE to upsample the minority class (Churn = 1) on the training set only
oversample = SMOTE(random_state=42)
X_resampled_train, y_resampled_train = oversample.fit_resample(X_train, y_train)

resampled_df_train = pd.concat([X_resampled_train, y_resampled_train], axis=1)

# Calculate the churn and non-churn counts
churn_count = resampled_df_train[resampled_df_train['Churn'] == 1].shape[0]
non_churn_count = resampled_df_train[resampled_df_train['Churn'] == 0].shape[0]

# Set up the plot size and title
plt.figure(figsize=(8, 6))
plt.title('Churn Rate')

# Set the colors for the pie chart sections
colors = ['lightcoral', 'lightgreen']

# Create the pie chart
plt.pie([churn_count, non_churn_count], labels=['Churn', 'Non-Churn'], autopct='%1.1f%%', colors=colors)

# Display the plot
plt.show()

"""
#   **Split the dataset**
  Dividing the dataset into training, validation, and test sets. The typical split is 70-80% for training, 10-15% for validation, and 10-15% for testing. The validation set helps in model selection and hyperparameter tuning."""

X, y = X_resampled_train, y_resampled_train

# Split the data into training, validation, and test sets
X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.15, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.1765, random_state=42, stratify=y_train_val)

"""# Model Selection"""

# Define a list of models including additional choices
models = [
    LogisticRegression(max_iter=1000),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    SVC(probability=True),
    XGBClassifier(),
    MLPClassifier(max_iter=1000)
]

# Iterate over the models
for model in models:
    # Train the model on the resampled training set
    model.fit(X_train, y_train)

    # Make predictions on the validation set
    y_pred_val = model.predict(X_val)

    # Calculate prediction probabilities on the validation set
    y_prob_val = model.predict_proba(X_val)[:, 1] # Probability of the positive class (churn)

    # Evaluate the model performance on the validation set
    accuracy_val = accuracy_score(y_val, y_pred_val)
    recall_val = recall_score(y_val, y_pred_val)
    precision_val = precision_score(y_val, y_pred_val)
    f1_val = f1_score(y_val, y_pred_val)
    cm_val = confusion_matrix(y_val, y_pred_val)
    tn_val, fp_val, fn_val, tp_val = cm_val.ravel()
    specificity_val = tn_val / (tn_val + fp_val)

    # Print evaluation metrics on the validation set for each model
    print(f"Model: {type(model).__name__}")
    print("Model classification report")
    print(f"Accuracy: {accuracy_val:.4f}")
    print(f"Recall: {recall_val:.4f}")
    print(f"Precision: {precision_val:.4f}")
    print(f"F1 Score: {f1_val:.4f}")
    print(f"Confusion Matrix: \n{cm_val}")
    print(f"Specificity: {specificity_val:.4f}")
    print("\n")

# Create an XGBoost classifier object
xgb_clf = XGBClassifier()

