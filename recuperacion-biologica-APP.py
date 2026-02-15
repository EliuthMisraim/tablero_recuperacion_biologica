import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =========================================
# CONFIGURACIÓN DE LA PÁGINA
# =========================================
st.set_page_config(
    page_title="Calculadora Costos Ocultos",
    page_icon="🏢",
    layout="wide"
)

# =========================================
# ESTILOS CSS PERSONALIZADOS (El Botón Mágico)
# =========================================
st.markdown("""
<style>
/* Animación de las olas de colores */
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
    /* Fondo base con gradiente multicolor */
    background: linear-gradient(270deg, #FF512F, #DD2476, #40E0D0, #FF512F);
    background-size: 300% 300%;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: all 0.4s ease;
    border: none;
}

/* Efecto al pasar el mouse (Hover) */
.wave-btn:hover {
    /* Activar la animación de olas */
    animation: gradient-animation 3s ease infinite;
    /* Efecto de iluminación/resplandor */
    box-shadow: 0 0 15px rgba(221, 36, 118, 0.6), 0 0 30px rgba(64, 224, 208, 0.4);
    transform: scale(1.02); /* Crece un poquito */
}
</style>
""", unsafe_allow_html=True)

# =========================================
# BARRA LATERAL (INPUTS, LOGO Y BOTÓN)
# =========================================
with st.sidebar:
    # --- LOGO CENTRADO ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=150)
        
    st.header("⚙️ Parámetros de la Empresa")
    
    moneda = st.selectbox("Moneda", ["$", "€", "S/", "MXN"], index=0)
    
    st.subheader("Datos de la Plantilla")
    empleados = st.number_input("Total de Empleados", min_value=1, value=500, step=10)
    salario_promedio = st.number_input(f"Salario Promedio Mensual ({moneda})", min_value=0, value=15000, step=500)
    pct_fumadores = st.slider("% Estimado de Fumadores", 5, 60, 25, help="Porcentaje de la plantilla que consume tabaco") / 100

    # --- LLAMADA A LA ACCIÓN ---
    st.markdown("---")
    st.markdown("### ¿Listo para eliminar estos costos de tu nómina?")
    
    # Botón HTML personalizado
    link_agenda = "https://meetings.hubspot.com/eliuth-misraim?uuid=169366e7-ae2e-4855-8083-cc554bb3db85"
    st.markdown(f"""
        <a href="{link_agenda}" target="_blank" class="wave-btn">
            📅 Agendar Consulta
        </a>
    """, unsafe_allow_html=True)

# =========================================
# LÓGICA DE NEGOCIO (Cálculos)
# =========================================
def calcular_costo_tabaquismo(num_empleados, salario_mensual_promedio, porcentaje_fumadores):
    # Constantes
    MINUTOS_PERDIDOS_DIA = 60
    DIAS_LABORALES_ANIO = 250
    DIAS_EXTRA_AUSENTISMO = 3

    # Tasas
    salario_diario = salario_mensual_promedio / 30
    salario_hora = salario_diario / 8
    salario_minuto = salario_hora / 60

    num_fumadores = int(num_empleados * porcentaje_fumadores)

    # Costos
    costo_pausas = (num_fumadores * MINUTOS_PERDIDOS_DIA * salario_minuto * DIAS_LABORALES_ANIO)
    costo_absentismo = (num_fumadores * DIAS_EXTRA_AUSENTISMO * salario_diario)
    costo_total = costo_pausas + costo_absentismo

    return num_fumadores, costo_pausas, costo_absentismo, costo_total

fumadores, costo_pausas, costo_absentismo, costo_total = calcular_costo_tabaquismo(empleados, salario_promedio, pct_fumadores)

# =========================================
# INTERFAZ PRINCIPAL
# =========================================
st.title("🏢 Calculadora de Costos Ocultos por Tabaquismo")
st.markdown("""
Las pausas para fumar y los días extra de enfermedad generan una fuga de capital silenciosa en tu organización. 
Utiliza este simulador para estimar **cuánto dinero está perdiendo tu empresa cada año**.
""")

# --- SECCIÓN 1: MÉTRICAS CLAVE ---
st.divider()
col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.metric("Pérdida Total Anual Estimada", f"{moneda}{costo_total:,.0f}", delta="Costo Oculto", delta_color="inverse")

with col_m2:
    st.metric("Empleados Fumadores Estimados", f"{fumadores}", help=f"El {pct_fumadores*100:.0f}% de tu plantilla actual.")

with col_m3:
    costo_por_fumador = costo_total / fumadores if fumadores > 0 else 0
    st.metric("Pérdida Anual por Fumador", f"{moneda}{costo_por_fumador:,.0f}")

# --- SECCIÓN 2: GRÁFICO INTERACTIVO ---
st.divider()
st.subheader("📊 Desglose de Pérdidas Financieras")

# Creamos el gráfico de barras con Plotly para que sea interactivo
fig = go.Figure(data=[
    go.Bar(
        name='Pausas Laborales', 
        x=['Pausas Laborales (Presentismo)'], 
        y=[costo_pausas],
        marker_color='#ff9999',
        text=[f"{moneda}{costo_pausas:,.0f}"],
        textposition='outside',
        textfont=dict(size=14, color='#333333', family="Arial Black")
    ),
    go.Bar(
        name='Absentismo Extra', 
        x=['Días de Enfermedad (Ausentismo)'], 
        y=[costo_absentismo],
        marker_color='#66b3ff',
        text=[f"{moneda}{costo_absentismo:,.0f}"],
        textposition='outside',
        textfont=dict(size=14, color='#333333', family="Arial Black")
    )
])

# Estilización del gráfico
salario_k = salario_promedio / 1000
fig.update_layout(
    title=dict(
        text=f"<b>Costo Oculto Anual: {moneda}{costo_total:,.0f}</b><br><span style='font-size:14px; color:gray'>Empresa {empleados} empleados, Salario Prom. {moneda}{salario_k:.0f}k</span>",
        font=dict(size=20, color='#333333')
    ),
    yaxis_title=f"Costo Anual ({moneda})",
    template='plotly_white',
    showlegend=False,
    height=500,
    margin=dict(t=80, b=40),
    yaxis=dict(range=[0, max(costo_pausas, costo_absentismo) * 1.2], showgrid=True, gridcolor='#eeeeee') # Espacio extra arriba para los números
)

st.plotly_chart(fig, use_container_width=True)

# --- SECCIÓN 3: INTERPRETACIÓN DE RESULTADOS ---
st.divider()
st.header("💡 Interpretación de tu Fuga de Capital")

st.info(f"""
**Análisis del impacto en tu organización:**

1.  **El peso del Presentismo (Pausas):** * De los {moneda}{costo_total:,.0f} que pierdes al año, la mayor parte ({moneda}{costo_pausas:,.0f}) se debe a los **minutos acumulados en pausas para fumar**. 
    * Si un empleado fuma y pierde 60 minutos al día, al final del año suma semanas enteras de tiempo no laborado pero sí pagado.

2.  **El impacto del Ausentismo:**
    * Fumar compromete el sistema inmunológico. Estadísticamente, los fumadores piden en promedio **3 días más por incapacidad o enfermedad** al año.
    * Esto representa un costo extra directo a tu nómina de **{moneda}{costo_absentismo:,.0f}**.

3.  **El Costo de no hacer nada:**
    * Cada empleado fumador le está costando a la empresa **{moneda}{costo_por_fumador:,.0f} adicionales cada año**.
    * Implementar un programa de cesación no es un "gasto de bienestar", es una **estrategia de reducción de costos operativos**. Recuperar a solo unos cuantos empleados ya paga cualquier inversión.
""")