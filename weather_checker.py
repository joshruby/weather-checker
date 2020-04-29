import streamlit as st
from streamlit import caching
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
# import plotly.express as px

# mapbox weather-checker token for plotly use:
mapbox_token = 'pk.eyJ1IjoianJydWJ5IiwiYSI6ImNrOWtrMDU3czF2dTkzZG53Nmw2NDdneTMifQ.zzXEhr0Z1biR2pydOFco8A'
openweather_token = '5c3d72cdc2b3e6fc1c06ddc0004a713b'

st.header('Weather Checker')

# st.subheader('Weather by Zip Code')

# zip_code = st.text_input('Zip Code', value='', key=None, type='default')
city = st.text_input('City', value='', key=None, type='default')
state = st.text_input('State (Only necessary for non-unique cities, e.g. Glendale, CA and Glendale, AZ)', value='', key=None, type='default')
country_code = st.text_input('Country',  value='', key=None, type='default')


# st.subheader('Weather by City')
# city = st.text_input('City', value='', key=None, type='default')
# state = st.text_input('State', value='', key=None, type='default')
# country_code = st.text_input('Country Code', value='', key=None, type='default')


if city:
    if country_code:
        # call = 'http://api.openweathermap.org/data/2.5/weather?'+'zip='+zip_code+','+country_code+'&appid='+openweather_token
        call = 'http://api.openweathermap.org/data/2.5/weather?q='+city+','+country_code+'&appid='+openweather_token

    elif not country_code:
        # call = 'http://api.openweathermap.org/data/2.5/weather?'+'zip='+zip_code+'&appid='+openweather_token
        default_country_code = 'us'
        if state:
            call = 'http://api.openweathermap.org/data/2.5/weather?q='+city+','+state+','+default_country_code+'&appid='+openweather_token
        elif not state:
            call = 'http://api.openweathermap.org/data/2.5/weather?q='+city+','+default_country_code+'&appid='+openweather_token
    
    r = requests.get(call)


    ## Debug only
    # st.subheader('Raw call')
    # st.write(call)
    # st.subheader('Raw response')
    # st.write(r.json())

    ## Debug only
    # st.write(int(r.json()['cod']))
    # st.write(type(r.json()['cod']))


    if (int(r.json()['cod']) != 200):
        st.error('Invalid entry')
        if not country_code:
            st.info('Country is required for international cities')

    elif (int(r.json()['cod']) == 200):
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
                l=4,
                r=4,
                b=4,
                t=4,
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

        st.plotly_chart(fig, use_container_width=True)

        st.subheader('Current weather in ' + city_name)

        # st.write('Conditions: ', conditions)
        st.write('Temperature: ', float('%.1f' % temp_f))
        st.write('Feels Like: ', float('%.1f' % feels_like_f))
        st.write('Humidity: ', humidity)
        # # st.write('Today\'s high: ', float('%.2f' % high_f))
        # # st.write('Today\'s low: ', float('%.2f' % low_f))

# elif city:
#     r_city = requests.get('http://api.openweathermap.org/data/2.5/weather?q='
#         + city + ',' 
#         + state + ',' 
#         + country_code 
#         + '&appid=' + openweather_token
# )
#     st.write(r_city.json())