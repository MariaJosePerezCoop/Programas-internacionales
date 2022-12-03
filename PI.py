import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from PIL import Image
import squarify
import seaborn as sns
from matplotlib.backends.backend_agg import RendererAgg


st.set_page_config(page_title='PI',
    page_icon=':bar_chart:',
    layout='wide'
    
    )



df=pd.read_csv('internacional.csv')
df.head()


#fig=px.histogram(df, x='Promedio')
#fig.show()

df=df.dropna()

st.sidebar.header('Selección de campus')
estatus=st.sidebar.multiselect(
    'Elige los campus que quieras analizar:',
    options=df['CampusAdministrador'].unique(),
    default=df['CampusAdministrador'].unique()

)

df['EstatusNuevo']=df['Estatus'].str[:1]
df['EstatusNuevo'].value_counts()

df=df.replace(['A','P'],'Asignado')
df=df.replace(['E','I','C','T','R','N'],'Rechazado')
df['EstatusNuevo'].value_counts()

def tipos_intercambio(df):
    if('INT' in df['OportunidadAsignada']):
        return 'Intercambio Tradicional'
    else:
        return 'Study Abroad'
        
df['Tipo de intercanbio']=df.apply(tipos_intercambio, axis=1)
df['Tipo de intercanbio'].value_counts('primero')

def getFirstChoice(text):
    text = text[text.find("1 - ")+4:]
    if text.find(",") == -1:
        return text
    else:
        return text[:text.find(",")]


estatus=st.sidebar.multiselect(
    'Selecciona tipo de intercambio:',
    options=df['Tipo de intercanbio'].unique(),
    default=df['Tipo de intercanbio'].unique()
)

df["Orden asignado"] = df["OportunidadesSeleccionadas"].apply(getFirstChoice)

def primera_oportunidad(df):
    if(df['OportunidadAsignada'] in df['Orden asignado']):
        return ('Primera oportunidad')
    else:
        return ('Otra oportunidad')
        
df['Número de oportunidad asignada']=df.apply(primera_oportunidad, axis=1)
df['Número de oportunidad asignada'].value_counts()

Primeraopcion=df["Número de oportunidad asignada"].value_counts('Primera oportunidad')

def cambio(df):
    if('Asignado' in df['EstatusNuevo']):
        return int(1)
    else:
        return int(0)
        
df['Estatusconteo']=df.apply(cambio, axis=1)

df['Carrera'] = df['Programa'].replace({r'[0-9]+':''}, regex=True)


prog_estat=df.groupby('Carrera')[['Estatusconteo']].sum()

st.title(':earth_africa: Dashboard de Programas Internacionales')
st.markdown('##')


#st.sidebar.header('Selección de campus')
#estatus=st.sidebar.multiselect(
 #   'Elige los campus que quieras analizar:',
  #  options=df['CampusAdministrador'].unique(),
   # default=df['CampusAdministrador'].unique()

#)

#estatus=st.sidebar.multiselect(
#    'Selecciona tipo de intercambio:',
#    options=df['Tipo de intercanbio'].unique(),
#    default=df['Tipo de intercanbio'].unique()
#)

promedio=round(df['Promedio'].mean(),2)
matapro=int(df['Núm. MatAprobadas'].mean())
mattotal=int(df['Núm. MatTotales'].mean())

left_column, middle_column, right_column=st.columns(3)
with left_column:
    st.subheader(':memo: Calificación promedio de aplicantes')
    st.subheader(promedio)

with middle_column:
    st.subheader(':closed_book: Promedio de materias aprobadas')
    st.subheader(matapro)

with right_column:
    st.subheader(':orange_book: Promedio de materias totales')
    st.subheader(mattotal)

st.markdown('___')

fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### Promedio de niveles")
    fig = px.density_heatmap(
        data_frame=df, y="Promedio", x="Nivel"
    )
    st.write(fig)
   
with fig_col2:
    st.markdown("### Aplicantes por nivel")
    fig2 = px.histogram(data_frame=df, x="Nivel")
    st.write(fig2)

st.markdown('___')


h1, h2 = st.columns(2)

with h1:
    st.markdown("### Personas que quedaron en su primera opción")
    labels = 'Primera oportunidad', 'Otra oportunidad'
    sizes = [42360,5488]
    colores=['#FF4B4B','#F0F2F5']

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct="%0.1f %%", colors=colores)
    ax1.axis('equal')
    p = plt.gcf()
    p.gca().add_artist(plt.Circle( (0,0), 0.7, color='white'))

    st.pyplot(fig1)

    
   
with h2:
    st.markdown("### Tipo de internacionalización elegida")
    labels = ['Study Abroad','Intercambio Tradicional']
    sizes = df['Tipo de intercanbio'].value_counts()
    colores=['#0D0886','#F0F2F5']

    imag2, ax2 = plt.subplots()
    ax2.pie(sizes, labels=labels, autopct="%0.1f %%", colors=colores)
    ax2.axis('equal')
    p = plt.gcf()
    p.gca().add_artist(plt.Circle( (0,0), 0.7, color='white'))

    

st.markdown('___')

st.markdown("### Aplicantes asignados por carrera")
figura = px.treemap(df, path=['Carrera'], values='Estatusconteo',
    color='Carrera',
    color_continuous_scale='Blues',
    )
st.write(figura)



#promedio y niveles
#cantidad de niveles



