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
    
    /* Animación de las olas de colores para el botón */
    @keyframes gradient-animation {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Estilo del botón */
    .wave-btn {
        display: block;
        width: 100%;
        padding: 12px 20px;
        margin: 10px 0;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        color: white !important;
        text-decoration: none !important;
        border-radius: 8px;
        background: linear-gradient(270deg, #FF512F, #DD2476, #40E0D0, #FF512F);
        background-size: 300% 300%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.4s ease;
        border: none;
    }

    /* Efecto al pasar el mouse (Hover) */
    .wave-btn:hover {
        animation: gradient-animation 3s ease infinite;
        box-shadow: 0 0 15px rgba(221, 36, 118, 0.6), 0 0 30px rgba(64, 224, 208, 0.4);
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS MÉDICOS (Fuente: OMS / Cancer.org) ---
# Definimos los hitos de recuperación en horas/días/años
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
    # --- LOGO CENTRADO ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=150)
        
    st.header("⚙️ Configura tu Viaje")
    
    fecha_inicio = st.date_input("¿Cuándo es tu 'Día Cero'?", datetime.now())
    hora_inicio = st.time_input("Hora aproximada", datetime.now().time())
    
    st.markdown("---")
    st.subheader("Datos Financieros")
    
    # --- NUEVO SELECTOR DE MONEDA ---
    moneda = st.selectbox("Moneda", ["$", "€", "S/", "MXN"], index=0)
    
    cigarros_dia = st.slider("Cigarros al día", 1, 40, 10)
    
    # --- INPUT ACTUALIZADO CON LA MONEDA ---
    precio_cajetilla = st.number_input(f"Precio Cajetilla de 20 pz ({moneda})", value=75)
    
    # --- LLAMADA A LA ACCIÓN ---
    st.markdown("---")
    st.markdown("### ¿Te cuesta empezar?")
    st.info("**Grupo JD** tiene el método probado para que este contador empiece a correr hoy mismo.")
    
    # Botón HTML personalizado
    link_agenda = "https://meetings.hubspot.com/eliuth-misraim?uuid=169366e7-ae2e-4855-8083-cc554bb3db85"
    st.markdown(f"""
        <a href="{link_agenda}" target="_blank" class="wave-btn">
            📅 Agendar Consulta
        </a>
    """, unsafe_allow_html=True)

# --- LÓGICA DE CÁLCULO ---
fecha_completa_inicio = datetime.combine(fecha_inicio, hora_inicio)
ahora = datetime.now()
diferencia = ahora - fecha_completa_inicio
horas_transcurridas = diferencia.total_seconds() / 3600
dias_transcurridos = diferencia.days

# --- HEADER PRINCIPAL ---
st.title("🫁 Tu Cronograma de Regeneración Biológica")
st.markdown(f"Has estado libre de humo por: **{max(0, dias_transcurridos)} días y {max(0, int((horas_transcurridas % 24)))} horas**.")

# --- METRICAS KPI ---
col1, col2, col3 = st.columns(3)
cigarros_evitados = max(0, dias_transcurridos * cigarros_dia)
dinero_ahorrado = (cigarros_evitados / 20) * precio_cajetilla
vida_ganada = cigarros_evitados * 11 # 11 minutos por cigarro aprox.
vida_ganada_horas = vida_ganada / 60

col1.metric("Cigarros Evitados", f"{cigarros_evitados:,.0f}", delta_color="normal")

# --- MÉTRICA ACTUALIZADA CON LA MONEDA ---
col2.metric("Dinero Ahorrado", f"{moneda}{dinero_ahorrado:,.2f}", delta_color="normal")

col3.metric("Vida Ganada (aprox)", f"{vida_ganada_horas:.1f} Horas", "Tiempo valioso")

st.markdown("---")

# --- PROCESAMIENTO DE DATOS PARA GRÁFICO ---
df = pd.DataFrame(health_milestones)
df['Fecha Hito'] = df['tiempo_horas'].apply(lambda x: fecha_completa_inicio + timedelta(hours=x))
df['Estado'] = df['tiempo_horas'].apply(lambda x: '✅ Completado' if x <= horas_transcurridas else '🔒 Pendiente')
df['Días Restantes'] = df['tiempo_horas'].apply(lambda x: max(0, (x - horas_transcurridas)/24))

# Convertir a texto legible para el gráfico
def formato_tiempo(horas):
    if horas < 24: return f"{horas:.1f} Horas"
    if horas < 8760: return f"{horas/24:.1f} Días"
    return f"{horas/8760:.1f} Años"

df['Tiempo Legible'] = df['tiempo_horas'].apply(formato_tiempo)

# --- VISUALIZACIÓN 1: TIMELINE DE LOGROS ---
st.subheader("📍 Tu Mapa de Ruta")

# 1. Agregamos los valores fijos como columnas al DataFrame
df['Nivel'] = 1
df['Tamaño_Punto'] = 20

# 2. Generamos el gráfico referenciando los nombres de las columnas
fig = px.scatter(
    df, 
    x="Fecha Hito", 
    y="Nivel",           # Usamos la columna en lugar de la lista
    color="Estado",
    hover_name="hito",
    hover_data={"desc": True, "Fecha Hito": True, "Nivel": False, "Tamaño_Punto": False},
    color_discrete_map={'✅ Completado': '#2ecc71', '🔒 Pendiente': '#bdc3c7'},
    size="Tamaño_Punto", # Usamos la columna en lugar de la lista
    title="Línea de Tiempo de Recuperación"
)

# Personalizar gráfico para que parezca un Roadmap
fig.update_layout(
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    xaxis=dict(title="Fecha Estimada"),
    height=200,
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=True
)

# Agregar anotaciones para los hitos
for i, row in df.iterrows():
    color = "#27ae60" if row['Estado'] == '✅ Completado' else "#7f8c8d"
    fig.add_annotation(
        x=row['Fecha Hito'],
        y=1,
        text=row['Tiempo Legible'],
        yshift=25,
        showarrow=False,
        font=dict(color=color, size=10)
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
        
        # Evitar cálculos negativos si la fecha elegida es en el futuro
        progreso_actual = max(0, horas_transcurridas - hito_anterior_horas)
        progreso_total_tramo = meta_horas - hito_anterior_horas
        
        porcentaje = min(1.0, max(0.0, progreso_actual / progreso_total_tramo))
        st.progress(porcentaje)
        st.caption(f"Faltan {proximo['Días Restantes']:.1f} días para este logro.")
        
        # Lista del resto
        with st.expander("Ver metas a largo plazo"):

            st.table(pendientes.iloc[1:][['hito', 'Tiempo Legible']])

