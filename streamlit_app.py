# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

#st.text(fruityvice_response).json())


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

#option = st.selectbox( 'What is your favorite fruit?', ('Banana','Strawberries','Peaches'))
#st.write('Your favorite fruit is:',option)


cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('Choose up to 5 ingredientes:', my_dataframe)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string=''

for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen +' '
    st.subheader(fruit_chosen+'Nutrition Information')
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
#st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

time_to_insert=st.button("Submit Order")

#st.write(my_insert_stmt)
#if ingredients_string:
if time_to_insert:
    session.sql(my_insert_stmt).collect()

    st.success('Your Smoothie is ordered')
