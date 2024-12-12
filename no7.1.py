import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import folium
import json
from streamlit_folium import st_folium

# Data koordinat kota
city_coordinates = {
    "Bandung": [-6.9175, 107.6191],
    "Bekasi": [-6.2383, 106.9756],
    "Bogor": [-6.5950, 106.8166],
    "Cimahi": [-6.8721, 107.5422],
    "Tasikmalaya": [-7.3274, 108.2207],
    "Jakarta": [-6.2088, 106.8456],
    "Depok": [-6.4025, 106.7942],
    "Purwakarta": [-6.5560, 107.4464],
    "Ciamis": [-7.3346, 108.3535]
}

# Memuat data koneksi dari file JSON
with open("connect.json", "r") as file:
    city_connections = json.load(file)

# Fungsi untuk membuat graf dari data koneksi kota
def create_graph(city_data):
    graph = nx.Graph()
    for city, neighbors in city_data.items():
        for neighbor in neighbors:
            graph.add_edge(city, neighbor)
    return graph

# Judul aplikasi Streamlit
st.title("City Connections in West Java")

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Profile", "Empty", "City Map"])

if menu == "Profile":
    st.header("Profiles of Team Members")

    # Profile 1
    st.subheader("Person 1")
    st.image("https://via.placeholder.com/150", caption="Person 1")
    st.write("This is a brief description of Person 1.")

    # Profile 2
    st.subheader("Person 2")
    st.image("https://via.placeholder.com/150", caption="Person 2")
    st.write("This is a brief description of Person 2.")

    # Profile 3
    st.subheader("Person 3")
    st.image("https://via.placeholder.com/150", caption="Person 3")
    st.write("This is a brief description of Person 3.")

elif menu == "Empty":
    st.header("Empty Menu")
    st.write("This section is intentionally left empty.")

elif menu == "City Map":
    # Input nama provinsi
    province = st.text_input("Enter the name of the province (in Bahasa Indonesia or English):")

    if province.lower() in ["jawa barat", "west java"]:
        # Input untuk memilih kota
        st.subheader("Select Cities to Visualize Connections")

        # Daftar kota untuk seleksi
        selected_cities = st.multiselect(
            "Select cities to show connections:", 
            options=list(city_coordinates.keys()),
            default=["Bandung", "Jakarta"]
        )

        if selected_cities:
            # Membuat peta dengan Folium
            m = folium.Map(location=[-6.9175, 107.6191], zoom_start=8)

            # Menambahkan marker untuk setiap kota
            for city, coords in city_coordinates.items():
                if city in selected_cities:
                    folium.Marker(location=coords, popup=city, tooltip=city).add_to(m)

            # Menambahkan koneksi antar kota
            for city in selected_cities:
                for neighbor in city_connections.get(city, []):
                    if neighbor in selected_cities:
                        city_coords = city_coordinates[city]
                        neighbor_coords = city_coordinates[neighbor]
                        folium.PolyLine([city_coords, neighbor_coords], color="blue", weight=2.5).add_to(m)

            # Menampilkan peta di Streamlit
            st_folium(m, width=700, height=500)

            # Membuat graf dari data koneksi kota
            graph = create_graph({
                city: [neighbor for neighbor in neighbors if neighbor in selected_cities]
                for city, neighbors in city_connections.items()
                if city in selected_cities
            })

            # Visualisasi graf
            st.subheader("City Connections Graph")
            fig, ax = plt.subplots(figsize=(10, 8))
            nx.draw(
                graph, 
                with_labels=True, 
                node_color="lightblue", 
                node_size=2500, 
                font_size=10, 
                edge_color="gray", 
                ax=ax
            )
            st.pyplot(fig)

        else:
            st.warning("Please select at least one city to display connections.")
    else:
        st.warning("Data for the specified province is not available.")
