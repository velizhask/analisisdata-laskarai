import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')

# Load dataset
st.header('Bike Sharing Dashboard :bike:')
uploaded_file = st.file_uploader('Upload a CSV file', type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())  # menampilkan sample data
    
    # konversi dteday menjadi datetime
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Menentukan tanggal awal dan akhir dataset
    min_date = df['dteday'].min()
    max_date = df['dteday'].max()
    
    # Sidebar - Date filter
    with st.sidebar:
        selected_date = st.date_input(
            'Pilih Tanggal', min_value=min_date, max_value=max_date, value=min_date
        )
    
    # Filter data hanya untuk tanggal yang dipilih
    filtered_df = df[df['dteday'] == pd.to_datetime(selected_date)]
    
    if not filtered_df.empty:
        st.subheader(f'Visualisasi Data pada {selected_date}')

        # Menampilkan Total Rentals
        st.subheader('Daily Rentals')
        total_rentals = filtered_df['total_rentals'].sum()

        st.metric(label="Total Rentals", value=total_rentals)

        
        #Total Rentals per Hour
        st.subheader('Total Rentals per Hour')
        hourly_data = filtered_df.groupby('hr')['total_rentals'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=hourly_data['hr'], y=hourly_data['total_rentals'], ax=ax, palette='coolwarm')
        ax.set_title(f'Total Rentals per Hour on {selected_date}')
        ax.set_xlabel('Hour')
        ax.set_ylabel('Total Rentals')
        st.pyplot(fig)

        #Casual vs Registered Rentals
        st.subheader('Casual vs Registered Rentals')
        fig, ax = plt.subplots(figsize=(10, 5))
        hourly_data = filtered_df.groupby('hr')[['casual', 'registered']].sum().reset_index()
        ax.bar(hourly_data['hr'], hourly_data['casual'], label='Casual', color='blue', alpha=0.6)
        ax.bar(hourly_data['hr'], hourly_data['registered'], bottom=hourly_data['casual'], label='Registered', color='orange', alpha=0.6)
        ax.set_title(f'Casual vs Registered Rentals per Hour on {selected_date}')
        ax.set_xlabel('Hour')
        ax.set_ylabel('Total Rentals')
        ax.legend()
        st.pyplot(fig)

        st.subheader('Total Rentals Berdasarkan Kondisi Cuaca')
        weather_labels = {
            1: "Clear",
            2: "Mist",
            3: "Light Rain/Snow",
            4: "Heavy Rain/Snow"
        }
        weather_data = filtered_df.groupby('weathersit')['total_rentals'].sum().reset_index()
        weather_data['weathersit'] = weather_data['weathersit'].map(weather_labels)

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=weather_data['weathersit'], y=weather_data['total_rentals'], ax=ax, palette='viridis')
        ax.set_title('Total Rentals by Weather Condition')
        ax.set_xlabel('Weather Condition')
        ax.set_ylabel('Total Rentals')
        st.pyplot(fig)
        
    else:
        st.warning('Tidak ada data untuk tanggal yang dipilih.')
