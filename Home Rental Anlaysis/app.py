import streamlit as st
import database
import pandas as pd
import st_components
import altair as alt
from database import *

connection = database.connect_to_database()
cities = database.get_all_cities(connection)
types = database.get_all_types(connection)

col1, col2, col3, col4 = st.columns([1,2,2,2], gap="large")

with col1:
	st.text("")
	st_components.metric_box("Total Props", get_houses_count_in_city(connection), "grey")
	st_components.metric_box("Avg Rent", f'{get_avg_min_max_rent_in_city(connection, None, "avg")} £', "ivory")
	st_components.metric_box("Min Rent", f'{get_avg_min_max_rent_in_city(connection, None, "min")} £', "teal")
	st_components.metric_box("Max Rent", f'{get_avg_min_max_rent_in_city(connection, None, "max")} £', "aqua")

with col2:
	df_top_city_rent_price = pd.read_sql_query(f"""
        select city, round(avg(rentppw),0) as avg_rent from houses
        group by city
        order by avg_rent DESC
        limit 7
        """, connection)
	
	st.subheader("Average PPW by City")
	st.write(alt.Chart(df_top_city_rent_price, width=400, height = 350).mark_bar(width=17,color="ivory").encode(x=alt.X('city', sort=None),y='avg_rent'))
	
	df_rooms = pd.read_sql_query(f"""
        select count(*) as count, availableRooms from houses
        group by availableRooms
        order by count ASC
        """, connection)
	st.subheader("Bedrooms in the properties")
	st.write(alt.Chart(df_rooms, width=400, height=250).mark_bar(width=17,color="orange").encode(x=alt.X('availableRooms', sort="ascending"),y='count'))

with col3:
	df_map_location = pd.read_sql_query(f"""
		select lon, lat from houses
		""", connection)
	st.map(df_map_location)

with col4:
	city = st.selectbox("City",options = cities, index=11)
	df_avg_rent_price_per_type = pd.read_sql_query(f"""
        select type, round(avg(rentppw),0) as avg_rent from houses
        where city = '{city}' 
        group by type
        order by avg_rent desc
        """, connection)
	df_num_houses_per_type = pd.read_sql_query(f"""
        select type, count(*) as count_prop from houses
        where city = '{city}' 
        group by type
        """, connection)

	st.subheader("Number of listings per type")
	st.write(alt.Chart(df_num_houses_per_type, width=400, height= 240).mark_arc(align="center").encode(theta="count_prop",color="type"))
	st.subheader("Average PPW by Type")
	st.write(alt.Chart(df_avg_rent_price_per_type, width=400, height=270).mark_bar(width=17,color="orange").encode(x=alt.X('type', sort=None),y='avg_rent'))
