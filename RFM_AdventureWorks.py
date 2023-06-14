#!/usr/bin/env python
# coding: utf-8

# # Import library

# In[46]:


import pandas as pd
import matplotlib.pyplot as plt
import sklearn as skt
import seaborn as sns


# # Read data

# In[258]:


df = pd.read_excel("D:\\chứng chỉ\\chung_chi\\b.xlsx")


# In[184]:


df.head()


# In[185]:


df.describe()


# In[186]:


df.columns


# # Clean data

# In[187]:


df.info()


# In[188]:


df.isnull().sum()


# In[189]:


df.duplicated()


# In[190]:


df_product = ['EnglishProductCategoryName', 'Model']
df_product_nm = df[df_product]
df_product_nm.describe()


# In[191]:


Q1 = df_product_nm.quantile(0.25)
Q3 = df_product_nm.quantile(0.75)
IQR = Q3 - Q1
IQR


# In[192]:


((df_product_nm < (Q1 -1.5*IQR))|(df_product_nm > (Q3 + 1.5*IQR))).any()


# In[193]:


df_demographic = ['Age']
df_demographic_nm = df[df_demographic]
df_demographic_nm.describe()


# In[194]:


Q1 = df_demographic_nm.quantile(0.25)
Q3 = df_demographic_nm.quantile(0.75)
IQR = Q3 - Q1
IQR


# In[195]:


((df_demographic_nm < (Q1 -1.5*IQR))|(df_demographic_nm > (Q3 + 1.5*IQR))).any()


# In[236]:


reference_date = pd.to_datetime('2014-2-01')   # reference date

df1 = df.loc[(df['OrderDate'] < '2014-2-01')]


# # Exploratory Data Analysis (EDA)

# In[237]:


# danh mục sản phẩm theo doanh thu và số lượng bán ra
product_df = df1[['EnglishProductCategoryName', 'ExtendedAmount']]
product_df1 = df1[['EnglishProductCategoryName', 'OrderQuantity']]
fig, axarr = plt.subplots(1, 2, figsize = (15,5))
product_df.groupby('EnglishProductCategoryName').sum().plot(kind='bar',ax=axarr[0])
product_df1.groupby('EnglishProductCategoryName').sum().plot(kind='bar',ax=axarr[1])


# In[ ]:





# Xe đạp (Bikes) mang lại doanh thu lớn nhất cho công ty nhưng số lượng bán ra chỉ xếp thứ 2 sau phụ kiện (Accessories) => xe đạp (Bikes) có giá cao hơn.

# In[238]:


#lượng khách hàng theo khu vực
fig, axarr = plt.subplots(figsize = (13,8))
customer_region = df1.groupby('Region')['CustomerKey'].nunique().sort_values(ascending=False).reset_index()
sns.barplot(data=customer_region, x='Region', y='CustomerKey',palette='Blues')


# Khách hàng chủ yếu ở vùng United States

# # RFM

# In[265]:


#Calculating Recency
df_recency = df1.groupby(by='CustomerKey',as_index=False)['OrderDate'].max()
df_recency.columns = ['CustomerKey','max_date']
df_recency['Recency'] = df_recency['max_date'].apply(lambda row: (reference_date - row).days)
df_recency.drop('max_date',inplace=True,axis=1)
df_recency.head()


# In[266]:


#Calculating Frequency
df_frequency = df1.groupby(by=['CustomerKey'],as_index=False)['SalesOrderLineNumber'].nunique()
df_frequency.columns = ['CustomerKey','Frequency']
df_frequency.head()


# In[267]:


#Calculating Monetary
df_monetary = df1.groupby(by='CustomerKey', as_index=False)['ExtendedAmount'].sum()
df_monetary.columns = ['CustomerKey', 'Monetary']
df_monetary.head()


# In[268]:


#Calculating RFM score
rf_df = df_recency.merge(df_frequency, on='CustomerKey')
rfm_df = rf_df.merge(df_monetary, on='CustomerKey')
rfm_df.head()


# In[269]:


def R_Class(x):
    if x['Recency'] <= 100:
        recency = 3
    elif x['Recency'] > 100 and x['Recency'] <= 200:
        recency = 2
    else:
        recency = 1
    return recency
rfm_df['R'] = rfm_df.apply(R_Class,axis=1)

def F_Class(x):
    if x['Frequency'] <= 3:
        recency = 3
    elif x['Frequency'] > 3 and x['Frequency'] <= 5:
        recency = 2
    else:
        recency = 1
    return recency
rfm_df['F'] = rfm_df.apply(F_Class,axis=1)

M_Class = pd.qcut(rfm_df['Monetary'],q=3,labels=range(1,4))
rfm_df = rfm_df.assign(M = M_Class.values)
rfm_df.head()


# In[271]:


def RFM_Score(row):
    return str(row['R']) + str(row['F']) + str(row['M'])
rfm_df['RFM_Score'] = rfm_df.apply(RFM_Score,axis=1)
rfm_df.head()


# Khách hàng 11001 có số điểm RFM là 313 điều này chứng tỏ gần đây khách hàng này đã truy cập mua hàng với tần suất tốt, doanh số mang lại cho cửa hàng cao.
# Trong khi đó khách hàng 11002 và 11004 tùy có tần suất mua nhiều và chi trả một số tiền lớn để mua hàng tuy nhiên thời gian gần đây lại không quay lại mua hàng => công ty có thể liên lạc bằng cách gửi mail nhắc nhở khác hàng.

# In[ ]:




