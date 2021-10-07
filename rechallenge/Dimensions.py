
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


def getMovieInfo(query):

    import http.client
    import json

    conn = http.client.HTTPSConnection("api.themoviedb.org")

    payload = "{}"

    payload2 = "{}"

    conn.request("GET", "/3/search/movie?include_adult=false&page=1&language=en-US&api_key=36c1aef1dac39d6f2522547134eb7e0e&query="+query, payload)
    res = conn.getresponse()
    data = res.read() 
    
    json_result = json.loads(data)

    if len(json_result['results']) == 0:
        movie_info = pd.Series([0, 0, 0])
    else:
        movie_id = str(json_result['results'][0]['id'])

        conn.request("GET", "/3/movie/"+movie_id+"?api_key=36c1aef1dac39d6f2522547134eb7e0e&language=en-US", payload2)
        res_details = conn.getresponse()
        data_movie = res_details.read() 

        json_result = json.loads(data_movie)
        movie_budget = str(json_result['budget'])
        movie_runtime = str(json_result['runtime'])
        movie_vote_average = str(json_result['vote_average'])

        movie_info = pd.Series([movie_budget,movie_runtime, movie_vote_average])

    return movie_info 


# In[3]:


#loyalty_users = pd.read_csv('arquivos/loyalty_program_users.csv')
#tickets_list = pd.read_csv('arquivos/tickets_list.csv')

all_tickets = pd.read_excel('arquivos/all_tickets_sold.xlsx')
loyalty_sales = pd.read_excel('arquivos/loyalty_sales.xlsx')


# In[4]:


#Rename columns to be equals
all_tickets.rename(columns={'Projection time': 'proj_time', 'Movie': 'movie', 'sale (Euros)':'sales', 'screen number':'screen_number', 'movie theater':'cinema'}, inplace=True)
loyalty_sales.rename(columns={'User':'user', 'Projection time': 'proj_time', 'number of tickets':'qty_tickets', 'screen number':'screen_number'}, inplace=True)


#Union both sources
all_sales = pd.concat([loyalty_sales, all_tickets ]) 


# In[5]:


#Receive a dataframe, column to extract
#Return the dataframe with ids and unique values
def extract_dimension(df, df_column, column_name):
    df = pd.DataFrame(df[df_column].unique(), columns=[df_column])
    df['id_'+column_name] = df.index+1
    return df


# In[47]:


#Extract format
df_format = extract_dimension(all_sales, 'format', 'format')


# In[48]:


csv_format = pd.read_csv('arquivos/tickets_list.csv', sep=';') 
csv_format


# In[49]:


csv_format.rename(columns={'projection_format':'format', 'ticket price (Euros)':'price', }, inplace=True)

csv_format


# In[54]:


df_format = pd.merge(csv_format, df_format, on='format') 
df_format


# In[56]:


from sqlalchemy import create_engine
import pandas.io.sql

engine = create_engine('postgresql://postgres:leury5@localhost/postgres') 


# In[57]:


#write to the database
df_format.to_sql(name='dim_pformat', con=engine, index=False)


# In[13]:


#Extract cinema
df_cinema = extract_dimension(all_sales, 'cinema', 'cinema')

df_cinema


# In[14]:


df_cinema.to_sql(name='dim_pcinema', con=engine, index=False) 


# In[15]:


#Extract Promotion
df_promotion = extract_dimension(loyalty_sales, 'promotion', 'promotion')

for index,row in df_promotion.iterrows():
    if 'free' in df_promotion.loc[index,'promotion']:
        df_promotion.loc[index,'type'] = 0
    else:
        df_promotion.loc[index,'type'] = df_promotion.loc[index,'promotion'][0:1]


# In[17]:


df_promotion.head(2)


# In[58]:


df_promotion.to_sql(name='dim_ppromotion', con=engine, index=False)                                 


# In[18]:


df_movie = extract_dimension(all_sales, 'movie', 'movie')


# In[23]:


#Run this cell after errors corrections
for index,row in df_movie.iterrows():
        df_movie.loc[index,'query'] = df_movie.loc[index,'movie'].replace(' ', '+')
        v_query = df_movie.loc[index,'movie'].replace(' ', '+')
        movie_info = getMovieInfo(v_query)
        df_movie.loc[index,'budget'] = movie_info[0]
        df_movie.loc[index,'runtime'] = movie_info[1]
        df_movie.loc[index,'vote_average'] = movie_info[2]


# In[31]:


df_movie.head(2)


# In[25]:


#Verification if there's any movie without from the API
df_movie_errors = df_movie[(df_movie['budget'] == 0) & (df_movie['runtime'] == 0) & (df_movie['vote_average'] == 0)]
df_movie_errors


# In[22]:


#Movie names were wrong, now we can correct them

df_movie['movie'].replace(
    to_replace='Rogue One: A Star Warss Story',
    value='Rogue One: A Star Wars Story',
    inplace=True
) 

df_movie['movie'].replace(
    to_replace='Gods of Ygypt',
    value='Gods of Egypt',
    inplace=True
)  

df_movie['movie'].replace(
    to_replace='Warrcraft',
    value='Warcraft',
    inplace=True
)  


# In[30]:


df_movie.drop('query', axis=1).to_sql(name='dim_pmovie', con=engine, index=False)

