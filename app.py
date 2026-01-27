import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Tablero de Recuperación Biológica",
    page_icon="🫁",
    layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .big-font { font-size:20px !important; }
    .success-text { color: #2ecc71; font-weight: bold; }
    .metric-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #2ecc71; }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS MÉDICOS (Fuente: OMS / Cancer.org) ---
health_milestones = [
    {"hito": "Presión arterial normalizada", "tiempo_horas": 0.33, "desc": "En 20 min, tu presión baja a niveles normales."},
    {"hito": "Niveles de CO normalizados", "tiempo_horas": 12, "desc": "El monóxido de carbono en sangre baja a lo normal."},
    {"hito": "Menor riesgo de infarto", "tiempo_horas": 24, "desc": "Tu riesgo de ataque cardíaco empieza a descender."},
    {"hito": "Sentidos recuperados", "tiempo_horas": 48, "desc": "El olfato y el gusto comienzan a mejorar notablemente."},
    {"hito": "Nicotina eliminada", "tiempo_horas": 72, "desc": "Tu cuerpo está 100% libre de nicotina física."},
    {"hito": "Mejor circulación", "tiempo_horas": 2160, "desc": "3 Meses: Tu función pulmonar aumenta hasta un 30%."},
    {"hito": "Cilios pulmonares recuperados", "tiempo_horas": 6570, "desc": "9 Meses: Menos tos y fatiga; los pulmones se limpian solos."},
    {"hito": "Riesgo coronario a la mitad", "tiempo_horas": 8760, "desc": "1 Año: El riesgo de enfermedad coronaria es 50% menor."},
    {"hito": "Riesgo de ACV igual a no fumador", "tiempo_horas": 43800, "desc": "5 Años: Las arterias se han sanado lo suficiente."},
    {"hito": "Riesgo de cáncer pulmonar a la mitad", "tiempo_horas": 87600, "desc": "10 Años: Células precancerosas reemplazadas."},
    {"hito": "Salud cardiovascular total", "tiempo_horas": 131400, "desc": "15 Años: Tu corazón es igual al de alguien que nunca fumó."}
]

# --- SIDEBAR: INPUTS DEL USUARIO ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966486.png", width=100) 
    st.header("Configura tu Viaje")
    
    fecha_inicio = st.date_input("¿Cuándo es tu 'Día Cero'?", datetime.now())
    hora_inicio = st.time_input("Hora aproximada", datetime.now().time())
    
    st.markdown("---")
    st.subheader("Datos Financieros")
    
    cigarros_dia = st.slider("Cigarros al día", 1, 40, 10)
    
    precio_cajetilla = st.number_input("Precio Cajetilla ($)", value=75)
    
    st.markdown("---")
    st.markdown("### ¿Te cuesta empezar?")
    st.info("**Grupo JD** tiene el método probado para que este contador empiece a correr hoy mismo.")
    
    # ENLACE A HUBSPOT
    st.link_button("📅 Agendar Cita (Grupo JD)", "https://meetings.hubspot.com/eliuth-misraim?uuid=498ae106-fe1d-4541-8d48-c374da63d972")

# --- LÓGICA DE CÁLCULO ---
fecha_completa_inicio = datetime.combine(fecha_inicio, hora_inicio)
ahora = datetime.now()
diferencia = ahora - fecha_completa_inicio
horas_transcurridas = diferencia.total_seconds() / 3600
dias_transcurridos = diferencia.days

# --- HEADER PRINCIPAL ---
st.title("🫁 Tu Cronograma de Regeneración Biológica")
st.markdown(f"Has estado libre de humo por: **{dias_transcurridos} días y {int((horas_transcurridas % 24))} horas**.")

# --- METRICAS KPI ---
col1, col2, col3 = st.columns(3)
cigarros_evitados = dias_transcurridos * cigarros_dia
dinero_ahorrado = (cigarros_evitados / 20) * precio_cajetilla
vida_ganada = cigarros_evitados * 11 # 11 minutos por cigarro aprox.
vida_ganada_horas = vida_ganada / 60

col1.metric("Cigarros Evitados", f"{cigarros_evitados:,.0f}", delta_color="normal")
col2.metric("Dinero Ahorrado", f"${dinero_ahorrado:,.2f}", delta_color="normal")
col3.metric("Vida Ganada (aprox)", f"{vida_ganada_horas:.1f} Horas", "Tiempo valioso")

st.markdown("---")

# --- PROCESAMIENTO DE DATOS PARA GRÁFICO ---
df = pd.DataFrame(health_milestones)
df['Fecha Hito'] = df['tiempo_horas'].apply(lambda x: fecha_completa_inicio + timedelta(hours=x))
df['Estado'] = df['tiempo_horas'].apply(lambda x: '✅ Completado' if x <= horas_transcurridas else '🔒 Pendiente')
df['Días Restantes'] = df['tiempo_horas'].apply(lambda x: max(0, (x - horas_transcurridas)/24))

# CORRECCIÓN DE GRÁFICO: Creamos columna explícita para evitar error de 'y'
df['Nivel'] = 1 

# Convertir a texto legible para el gráfico
def formato_tiempo(horas):
    if horas < 24: return f"{horas:.1f} Horas"
    if horas < 8760: return f"{horas/24:.1f} Días"
    return f"{horas/8760:.1f} Años"

df['Tiempo Legible'] = df['tiempo_horas'].apply(formato_tiempo)

# --- VISUALIZACIÓN 1: TIMELINE DE LOGROS ---
st.subheader("📍 Tu Mapa de Ruta")

fig = px.scatter(
    df, 
    x="Fecha Hito", 
    y="Nivel", # Usamos la columna creada arriba
    color="Estado",
    hover_name="hito",
    hover_data={"desc": True, "Fecha Hito": True, "Nivel": False}, 
    color_discrete_map={'✅ Completado': '#2ecc71', '🔒 Pendiente': '#bdc3c7'},
    size=[20]*len(df),
    title="Línea de Tiempo de Recuperación"
)

# Personalizar gráfico para que parezca un Roadmap
fig.update_layout(
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    xaxis=dict(title="Fecha Estimada"),
    height=300,
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

# --- VISUALIZACIÓN 2: DETALLE DE HITOS (TABLA/TARJETAS) ---
col_izq, col_der = st.columns([1, 1])

with col_izq:
    st.subheader("✅ Logros Desbloqueados")
    desbloqueados = df[df['Estado'] == '✅ Completado']
    if desbloqueados.empty:
        st.warning("Aún no ha pasado suficiente tiempo. ¡Tu primer logro llega en 20 minutos!")
    else:
        for index, row in desbloqueados.iterrows():
            st.success(f"**{row['hito']}**: {row['desc']}")

with col_der:
    st.subheader("🚀 Próximas Metas")
    pendientes = df[df['Estado'] == '🔒 Pendiente']
    if pendientes.empty:
        st.balloons()
        st.info("¡Felicidades! Has completado todos los hitos médicos principales.")
    else:
        # Mostramos el próximo hito con una barra de progreso
        proximo = pendientes.iloc[0]
        st.info(f"**Siguiente: {proximo['hito']}**")
        st.write(f"_{proximo['desc']}_")
        
        # Calcular porcentaje para el próximo hito específico
        hito_anterior_horas = 0 if len(desbloqueados) == 0 else desbloqueados.iloc[-1]['tiempo_horas']
        meta_horas = proximo['tiempo_horas']
        progreso_actual = horas_transcurridas - hito_anterior_horas
        progreso_total_tramo = meta_horas - hito_anterior_horas
        
        # Evitar errores matemáticos si el progreso es negativo o cero
        if progreso_total_tramo > 0:
            porcentaje = min(1.0, max(0.0, progreso_actual / progreso_total_tramo))
        else:
            porcentaje = 0.0
            
        st.progress(porcentaje)
        st.caption(f"Faltan {proximo['Días Restantes']:.1f} días para este logro.")
        
        # Lista del resto
        with st.expander("Ver metas a largo plazo"):
            st.table(pendientes.iloc[1:][['hito', 'Tiempo Legible']])