import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import requests
from streamlit import caching

st.subheader('Testing the "requests" library')

zip_code = st.text_input('Zip Code', value='', key=None, type='default')

if zip_code:
    # caching.clear_cache()

    r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=' + zip_code + ',us&appid=5c3d72cdc2b3e6fc1c06ddc0004a713b')

    # st.write(r.json())

    location = r.json()['coord']
    weather_k = temp_k = r.json()['main']
    temp_k = r.json()['main']['temp']

    # st.write(location)

    lat = location['lat']
    lon = location['lon']

    # # st.write('lat: ', lat)
    # # st.write('lat: ', lon)

    loc_arr = np.zeros((1,2))
    loc_arr[0,0] = lat
    loc_arr[0,1] = lon

    loc_df = pd.DataFrame(loc_arr, columns=['lat', 'lon'])
    # st.write(loc_df)
    st.map(loc_df, zoom=11)

    # st.pydeck_chart(pdk.Deck(
    #     map_style='mapbox://styles/mapbox/light-v9',
    #     view_state=pdk.ViewState(
    #         latitude=lat,
    #         longitude=lon,
    #         zoom=11,
    #         pitch=50,
    #     ),
    #     layers= pdk.Layer(
    #             'ScatterplotLayer',
    #             data=loc_df,
    #             get_position='[lon, lat]',
    #             get_color='[200, 30, 0, 160]',
    #             get_radius=200,
    #     ),
    # ))

    # test_map_df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    #                         columns=['lat', 'lon'])
    # st.write(test_map_df)
    # st.write(test_map_df.iloc[1,1])
    # st.map(test_map_df[:1], zoom=11)

    st.write('Current weather in ' + zip_code + ' [K]: ', weather_k)

    temp_f = (temp_k - 273.15) * 1.8 + 32

    st.write('Current temperature in ' + zip_code + ' [F]: ', float('%.2f' % temp_f))

# st.button('Refresh')