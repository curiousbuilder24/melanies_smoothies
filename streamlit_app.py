# Import python packages
import streamlit as st
# Import REQUESTS Python Package Library to build REST APIs
import requests
#Add a new python library called "PANDAS" 
import pandas as pd
#to connect App to OG_Streamlit_SniS you do not need this inport of active Snowflake session
#from snowflake.snowpark.context import get_active_session
#Syntax for Snowpark COLUMN function 
from snowflake.snowpark.functions import col


# Write directly to the app
#Badge-3-Building Data App for Mel's Diner Customer Intake Form
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your **cusotm** Smoothie!"""
)

#Add new text box for Mel's Order Intake form
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

#connect to the OG_Streamlit_SniS. two lines added below to connect to SniS
cnx = st.connection("snowflake")
session = cnx.session()

#Display the Fruit Options List loaded from STAGE in SiS App
#Add the New SEARCH_ON Column to the Dataframe that feeds the Multiselect
#my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_Name') ,col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the Snowpark Dataframe into a PANDAS Dataframe so we can use the LOC function
#Make a Version of my_dataframe, but call it pd_df
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_Name') ,col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

#Using Multiselect Widget
ingredients_list = st.multiselect (
    'Choose up to 5 ingredients:', my_dataframe,
max_selections=5,   
)

    
#defining ingredients_string variable as string
ingredients_string = ""


#Improving the STRING output. Delete old write statemetns we dont need.
if ingredients_list:
       
   ingredients_string = ''

   for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen + ' '
       #Access values from SEACH_ON column using LOC[] and iLOC[] properties
       search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0] 
       #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
       
       st.subheader(fruit_chosen + ' Nutrition Information')
       smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
       fv_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
     

   
#Build a SQL Insert Statement & Test It. Adsed second variable for name on order.
my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#this write statement helps us check our SQL query outpot 
#st.write(my_insert_stmt)

#STOP command for troubleshooting SQL before SiS app writes in database.
#st.stop()

#adding a new button on UI
time_to_insert = st.button ('Submit Order')

#Insert the Order from SiS into Snowflake database
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

# New section to display infromation from SMOOTHIEFROOT Nutrition API
#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
# putting JSON into a Dataframe
#sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


