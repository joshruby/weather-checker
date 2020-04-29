# mapbox weather-checker token:
mapbox_token = 'pk.eyJ1IjoianJydWJ5IiwiYSI6ImNrOWtrMDU3czF2dTkzZG53Nmw2NDdneTMifQ.zzXEhr0Z1biR2pydOFco8A'
# This token is configured for this script in ./streamlit/config.toml
# It's being initialized as a var here as well to use with plotly

import streamlit as st
from streamlit import caching
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.header('Weather Checker')

zip_code = st.text_input('Zip Code', value='', key=None, type='default')

if zip_code:
    # caching.clear_cache()

    r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=' + zip_code + ',us&appid=5c3d72cdc2b3e6fc1c06ddc0004a713b')

    # Debug only
    # st.subheader('Raw request')
    # st.write(r.json())

    city_name = r.json()['name']
    location = r.json()['coord']
    weather_k = temp_k = r.json()['main']
    # temp_k = r.json()['main']['temp']
    temp_f = (weather_k['temp'] - 273.15) * 1.8 + 32
    feels_like_f = (weather_k['feels_like'] - 273.15) * 1.8 + 32
    high_f = (weather_k['temp_max'] - 273.15) * 1.8 + 32
    low_f = (weather_k['temp_min'] - 273.15) * 1.8 + 32
    humidity = weather_k['humidity']
    conditions = r.json()['weather'][0]['main']

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

    # st.map(loc_df, zoom=11)

    # Plotly map (that actually updates!)
    fig = go.Figure(go.Scattermapbox(
        lat=loc_df['lat'],
        lon=loc_df['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=[city_name],
    ))

    fig.update_layout(
        autosize=False,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_token,
            bearing=0,
            center=dict(
                lat=lat,
                lon=lon
            ),
            pitch=0,
            zoom=9
        ),
    )

    st.plotly_chart(fig, use_container_width=False)

    st.subheader('Current weather in ' + city_name)

    # st.write('Conditions: ', conditions)
    st.write('Temperature: ', float('%.2f' % temp_f))
    st.write('Feels Like: ', float('%.2f' % feels_like_f))
    st.write('Humidity: ', humidity)
    # st.write('Today\'s high: ', float('%.2f' % high_f))
    # st.write('Today\'s low: ', float('%.2f' % low_f))