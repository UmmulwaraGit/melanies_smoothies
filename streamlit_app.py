# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit your want in your custom smoothie!
    """
)

name_txt = st.text_input('Name on you Smoothie:')
st.write("Name on you smoothie will be : ",name_txt)



session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingrediant_list = st.multiselect('Choose upto 5 Ingredient',my_dataframe, max_selections=5)



if ingrediant_list:
   
    ingrediant_string=''
    for fruit_chosen in ingrediant_list:
        ingrediant_string+=fruit_chosen +' '

    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingrediant_string + """','""" + name_txt + """')"""
    time_to_submit = st.button("Submit")
    
    
    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered! "+name_txt +" :cup_with_straw:", icon="✅" )
