# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit your want in your custom smoothie!
    """
)

name_txt = st.text_input('Name on you Smoothie:')
st.write("Name on you smoothie will be : ",name_txt)



cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
ingrediant_list = st.multiselect('Choose upto 5 Ingredient',my_dataframe, max_selections=5)



if ingrediant_list:
   
    ingrediant_string=''
    for fruit_chosen in ingrediant_list:
        ingrediant_string+=fruit_chosen +' '
        st.subheader(fruit_chosen + ' Nutrion Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        

    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingrediant_string + """','""" + name_txt + """')"""
    time_to_submit = st.button("Submit")
    
    
    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered! "+name_txt +" :cup_with_straw:", icon="✅" )





