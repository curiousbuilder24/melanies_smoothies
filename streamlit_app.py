# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
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


#Display the Fruit Options List loaded from STAGE in SiS App
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

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
