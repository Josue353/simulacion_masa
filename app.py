import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.patches import Rectangle

st.set_page_config(
    page_title="Simulador Científico Avanzado",
    layout="wide"
)

st.title("Simulación Científica Avanzada de Separación de Mezcla")
st.markdown("Sistema: Agua + Sal (disuelta) + Arena + Hierro")

col1, col2 = st.columns([1, 2])

# ==============================
# PANEL DE CONTROL
# ==============================

with col1:
    st.subheader("Parámetros Iniciales")

    agua = st.number_input("Agua (g)", 0.0, step=10.0)
    sal = st.number_input("Sal disuelta (g)", 0.0, step=1.0)
    arena = st.number_input("Arena (g)", 0.0, step=1.0)
    hierro = st.number_input("Hierro (g)", 0.0, step=1.0)

    campo = st.slider("Intensidad del campo magnético", 0.1, 2.0, 1.0)
    temperatura = st.slider("Temperatura de evaporación (°C)", 20, 120, 80)
    velocidad = st.slider("Velocidad simulación", 0.01, 0.15, 0.05)

    masa_total = agua + sal + arena + hierro
    st.metric("Masa total inicial", f"{masa_total:.2f} g")

    iniciar = st.button("Iniciar proceso completo")

# ==============================
# ÁREA DE SIMULACIÓN
# ==============================

with col2:

    placeholder = st.empty()

    if iniciar and masa_total > 0:

        np.random.seed(3)

        n_arena = int(arena)
        n_hierro = int(hierro)

        arena_x = np.random.uniform(1, 5, n_arena)
        arena_y = np.random.uniform(1, 5, n_arena)

        hierro_x = np.random.uniform(1, 5, n_hierro)
        hierro_y = np.random.uniform(1, 5, n_hierro)

        progreso = st.progress(0)

        # ==========================
        # ETAPA 1 – IMANTACIÓN
        # ==========================

        for step in range(40):

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 6)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title("Etapa 1: Separación Magnética")

            dx = 8 - hierro_x
            dy = 3 - hierro_y
            dist = np.sqrt(dx**2 + dy**2) + 1e-6

            hierro_x += (dx / dist) * 0.2 * campo
            hierro_y += (dy / dist) * 0.2 * campo

            ax.scatter(arena_x, arena_y, s=20)
            ax.scatter(hierro_x, hierro_y, s=25)

            # Dibujar imán tipo herradura
            ax.add_patch(Rectangle((8, 2), 0.4, 2, color='red'))
            ax.add_patch(Rectangle((8.8, 2), 0.4, 2, color='blue'))
            ax.add_patch(Rectangle((8, 2), 1.2, 0.3, color='gray'))

            placeholder.pyplot(fig)
            progreso.progress(step / 100)
            time.sleep(velocidad)

        # ==========================
        # ETAPA 2 – FILTRACIÓN
        # ==========================

        for step in range(30):

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 6)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title("Etapa 2: Filtración")

            arena_y -= 0.1

            ax.scatter(arena_x, arena_y, s=25)
            ax.scatter(hierro_x, hierro_y, s=25)

            placeholder.pyplot(fig)
            progreso.progress((40 + step) / 100)
            time.sleep(velocidad)

        # ==========================
        # ETAPA 3 – CÁLCULOS FÍSICOS
        # ==========================

        agua_retenida = arena * 0.15
        agua_libre = max(0, agua - agua_retenida)
        agua_evaporada = agua_libre * (temperatura / 120)

        masa_final = hierro + arena + sal + agua_retenida

        progreso.progress(1.0)

        st.success("Proceso completado.")

        st.markdown("---")
        st.subheader("Informe Científico")

        st.write(f"Masa inicial total: {masa_total:.2f} g")
        st.write(f"Agua retenida en arena: {agua_retenida:.2f} g")
        st.write(f"Agua evaporada: {agua_evaporada:.2f} g")
        st.write(f"Masa final del sistema sólido: {masa_final:.2f} g")

        error = abs(masa_total - (masa_final + agua_evaporada))
        st.write(f"Error experimental estimado: {error:.4f} g")