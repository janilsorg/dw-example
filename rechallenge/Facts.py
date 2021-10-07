
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np 


# In[2]:


from sqlalchemy import create_engine
import pandas.io.sql as psql

engine = create_engine('postgresql://postgres:leury5@localhost/postgres') 


# In[3]:


all_tickets = pd.read_excel('arquivos/all_tickets_sold.xlsx')
loyalty_sales = pd.read_excel('arquivos/loyalty_sales.xlsx')


# In[113]:


df_users = pd.read_csv('arquivos/loyalty_program_users.csv')
df_users.rename(columns={'User ID': 'user', 'Sex': 'sex', 'Age': 'age'}, inplace=True)


# In[40]:


#Rename columns to be equals
all_tickets.rename(columns={'Projection time': 'proj_time', 'Movie': 'movie', 'sale (Euros)':'sales', 'screen number':'screen_number', 'movie theater':'cinema'}, inplace=True)
loyalty_sales.rename(columns={'User':'user', 'Projection time': 'proj_time', 'number of tickets':'qty_tickets', 'screen number':'screen_number'}, inplace=True)


# In[186]:


df_sql_promotion = psql.read_sql("SELECT type, promotion FROM public.dim_ppromotion", con=engine)
df_sql_format = psql.read_sql("SELECT id_format,format, price FROM public.dim_pformat", con=engine)
df_sql_movie = psql.read_sql("SELECT id_movie, movie FROM public.dim_pmovie", con=engine)
df_sql_cinema = psql.read_sql("SELECT cinema, id_cinema FROM public.dim_pcinema", con=engine) 


# In[50]:


stg_loyalty = pd.merge(loyalty_sales, df_sql_promotion, on='promotion')  


# In[54]:


stg_loyalty = pd.merge(stg_loyalty, df_sql_format, on='format')   


# In[111]:


stg_loyalty.head(2)
#stg_loyalty[(stg_loyalty['proj_time'] == '')].head(2) 


# In[68]:


#Calculate the total paid, checks if there is a free entrance price*(ticket_number - 1) = price*ticket_number - price
#if it is a discount, the calculation are made (price*ticket_number -discount)
for index,row in stg_loyalty.iterrows():
    
    qty = stg_loyalty.loc[index,'qty_tickets'] 
    price = stg_loyalty.loc[index,'price']
    
    if stg_loyalty.loc[index,'type'] == '0':    
        stg_loyalty.loc[index,'total_paid'] = price*(qty - 1)  
    else:
        discount = int(stg_loyalty.loc[index,'type'])
        stg_loyalty.loc[index,'total_paid'] = price*qty - discount 


# In[114]:


stg_loyalty = pd.merge(stg_loyalty, df_users, on='user')


# In[115]:


stg_loyalty['sex'].replace(
    to_replace='male',
    value='m',
    inplace=True
)
stg_loyalty['sex'].replace(
    to_replace='female',
    value='f',
    inplace=True
)   


# In[157]:


stg_loyalty.head(2)


# In[121]:


#We need to get the number of tickets, in order to do so, we must join the format dimension so we have the price
#with the price, we can divide sales and price, after it we get the ticket numer
all_tickets.head(3)


# In[123]:


for index,row in stg_nonloyalty.iterrows():
    stg_nonloyalty.loc[index,'qty_tickets'] = stg_nonloyalty.loc[index,'sales']/stg_nonloyalty.loc[index,'price'] 


# In[170]:


stg_nonloyalty.rename(columns={'sales':'total_paid'}, inplace=True)


# In[194]:


union_all = pd.concat([stg_loyalty, stg_nonloyalty]) 


# In[195]:


union_all[(union_all['qty_tickets'].isnull())].head(4)


# In[196]:


#Now we fix the movie names like before
union_all ['movie'].replace(
    to_replace='Rogue One: A Star Warss Story',
    value='Rogue One: A Star Wars Story',
    inplace=True
) 

union_all ['movie'].replace(
    to_replace='Gods of Ygypt',
    value='Gods of Egypt',
    inplace=True
)  

union_all['movie'].replace(
    to_replace='Warrcraft',
    value='Warcraft',
    inplace=True
)   


# In[197]:


#df_sql_movie.head(1)
#df_sql_cinema.head(1)

union_all = pd.merge(union_all, df_sql_movie, on='movie') 
union_all = pd.merge(union_all, df_sql_cinema, on='cinema')  


# In[198]:


union_all.head(1)


# In[202]:


#Receive a dataframe, column to extract
#Return the dataframe with ids and unique values

union_all_db = union_all                            


# In[204]:


union_all_db['id_fact'] = union_all_db.index+1


# In[207]:


union_all_db.to_sql(name='pfact_sales', con=engine, index=False)

