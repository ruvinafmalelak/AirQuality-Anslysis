import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv('dashboard\main_data.csv')

# Set page configuration
st.set_page_config(page_title="Guanyuan's Air Quality Analysis ", layout="wide")

# Header
st.title("Guanyuan's Air Quality Analysis")
st.markdown("""
Dashboard ini menyajikan analisis kualitas udara di Guanyuan, termasuk tren polusi berdasarkan musim, bulan, hari, dan hubungannya dengan variabel cuaca.
""")

# Sidebar for filters
st.sidebar.header("Filter Data")
year = st.sidebar.multiselect("Pilih Tahun", options=df["year"].unique(), default=df["year"].unique())
month = st.sidebar.multiselect("Pilih Bulan", options=df["month"].unique(), default=df["month"].unique())
pollutant = st.sidebar.selectbox("Pilih Jenis Polutan", options=["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"])

# Filter data based on selection
filtered_df = df[(df["year"].isin(year)) & (df["month"].isin(month))]

# Section 1: Monthly and Seasonal Analysis
st.subheader("Analisis Polusi Berdasarkan Bulan dan Musim")

# Monthly Analysis
monthly_avg = filtered_df.groupby('month').mean(numeric_only=True)

# Define colors
monthly_color = 'b'

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_avg.index, monthly_avg[pollutant], marker='o', color=monthly_color)
ax.set_title(f'Rata-Rata Konsentrasi {pollutant} Berdasarkan Bulan di Guanyuan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Konsentrasi (µg/m³)')
st.pyplot(fig)

# Penjelasan untuk grafik bulanan
st.markdown(f"""
Penjelasan:
Grafik di atas menunjukkan rata-rata konsentrasi {pollutant} per bulan di Guanyuan. 
Dari grafik ini, kita dapat mengamati tren bulanan, apakah terdapat bulan tertentu dengan tingkat polusi yang lebih tinggi. 
Misalnya, jika terdapat puncak pada bulan tertentu, hal ini dapat menunjukkan faktor musiman atau aktivitas manusia yang lebih intensif pada bulan tersebut.
""")

# Seasonal Analysis
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

filtered_df.loc[:, 'season'] = filtered_df['month'].map(get_season)
seasonal_avg = filtered_df.groupby('season').mean(numeric_only=True)

seasonal_color = 'skyblue'

fig, ax = plt.subplots(figsize=(10, 6))
seasonal_avg[[pollutant]].plot(kind='bar', ax=ax, color=seasonal_color)
ax.set_title(f'Rata-Rata Konsentrasi {pollutant} Berdasarkan Musim di Guanyuan')
ax.set_xlabel('Musim')
ax.set_ylabel('Konsentrasi (µg/m³)')
st.pyplot(fig)

# Penjelasan untuk grafik musiman
st.markdown(f"""
Penjelasan:
Grafik ini menggambarkan rata-rata konsentrasi {pollutant} berdasarkan musim di Guanyuan. 
Analisis ini membantu kita memahami bagaimana kualitas udara berubah sepanjang tahun. 
Misalnya, jika konsentrasi {pollutant} lebih tinggi pada musim tertentu, bisa jadi disebabkan oleh perubahan cuaca, polusi dari sumber tertentu, atau aktivitas industri.
""")

# Section 2: Daily Analysis
st.subheader("Tren Harian Polusi Udara di Guanyuan")
daily_avg = filtered_df.groupby('day').mean(numeric_only=True)

daily_color = 'green'

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_avg.index, daily_avg[pollutant], marker='o', color=daily_color)
ax.set_title(f'Rata-Rata Konsentrasi {pollutant} Berdasarkan Hari dalam Sebulan di Guanyuan')
ax.set_xlabel('Hari dalam Sebulan')
ax.set_ylabel('Konsentrasi (µg/m³)')
st.pyplot(fig)

# Penjelasan untuk grafik harian
st.markdown(f"""
Penjelasan:
Grafik ini menunjukkan rata-rata konsentrasi {pollutant} berdasarkan hari dalam sebulan di Guanyuan. 
Dengan melihat grafik ini, kita dapat mengidentifikasi hari-hari dengan konsentrasi polusi yang tinggi atau rendah. 
Faktor-faktor seperti cuaca, aktivitas industri, dan lalu lintas dapat mempengaruhi variasi harian ini.
""")

# Section 3: Correlation Analysis
st.subheader("Analisis Korelasi antara Polutan dan Variabel Cuaca")
correlation_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
correlation_matrix = filtered_df[correlation_columns].corr()

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='RdBu', vmin=-1, vmax=1, ax=ax)
ax.set_title('Korelasi antara Polutan dan Variabel Cuaca di Guanyuan')
st.pyplot(fig)

# Penjelasan untuk grafik korelasi
st.markdown(f"""
Penjelasan :
Grafik heatmap di atas menunjukkan analisis korelasi antara berbagai polutan dan variabel cuaca di Guanyuan. 
Nilai korelasi berkisar antara -1 hingga 1, di mana 1 menunjukkan hubungan positif yang kuat, -1 menunjukkan hubungan negatif yang kuat, dan 0 menunjukkan tidak ada hubungan. 
Analisis ini membantu kita memahami faktor-faktor yang berkontribusi terhadap kualitas udara, misalnya, bagaimana suhu atau kelembapan dapat mempengaruhi konsentrasi polutan.
""")

# Section 4: Data Table
st.subheader("Data Lengkap: Guanyuan Air Quality")
st.dataframe(filtered_df)
