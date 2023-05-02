import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static


st.sidebar.title("Welcome to HomePage")

# Read the data
df = pd.read_csv('cleaned_data.csv')

# Show the title and basic information
st.title('Welcome to our Pub Finder App!')

st.subheader("basic information about pubs in the UK.")
st.write(f"shape of data: {df.shape}")

st.write("Columns in the dataset:")
st.write(df.columns.T)


# Show some statistics
st.subheader(f"basic statistics about the pubs in uk:")
st.write(df.describe())


#### 2.Pub Locations
st.sidebar.title("Pub_Locations")

st.title('Find Pubs by Postal Code or Local Authority')

# Ask the user for the Postal Code or Local Authority
search_type = st.selectbox('Search by:', ('Postal Code', 'Local Authority'))

if search_type == 'Postal Code':
    search_text = st.text_input('Enter the Postal Code:')
    pubs = df[df['postcode'] == search_text]
elif search_type == 'Local Authority':
    search_text = st.text_input('Enter the Local Authority:')
    pubs = df[df['local_authority'] == search_text]

# Show the map
if pubs is not None and not pubs.empty:
    # Get the center of the pubs
    center_lat = pubs['latitude'].mean()
    center_lon = pubs['longitude'].mean()

    # Create the map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Add markers for each pub
    for _, pub in pubs.iterrows():
        folium.Marker(location=[pub['latitude'], pub['longitude']], popup=pub['name']).add_to(m)

    # Display the map
    folium_static(m)
else:
    st.write('No pubs found.')





st.sidebar.title("Find the nearest Pub")

st.title("Find the 5 nearest pub_Locations")


# Ask the user for their location
user_lat = st.text_input("Enter your latitude:")
user_lon = st.text_input("Enter your longitude:")

# Convert the user's location to floats, checking for empty input
if user_lat and user_lon:
    user_lat = float(user_lat)
    user_lon = float(user_lon)

    # Compute the Euclidean distance between the user's location and each pub's location
    df['distance'] = ((df['latitude'] - user_lat) ** 2 + (df['longitude'] - user_lon) ** 2) ** 0.5

    # Select the nearest 5 pubs
    nearest_pubs = df.sort_values(by='distance').head(5)
    for _, pub in nearest_pubs.iterrows():
        
        st.write(f"Distance: {pub['distance']:.2f} km")
        st.write("")




    # Create a map and add markers for each of the nearest pubs
    m = folium.Map(location=[user_lat, user_lon], zoom_start=12)

    for _, pub in nearest_pubs.iterrows():
        folium.Marker(location=[pub['latitude'], pub['longitude']], popup=pub['name']).add_to(m)

    folium_static(m)
else:
    st.write("Please enter your latitude and longitude.")
