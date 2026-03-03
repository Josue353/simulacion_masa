import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

st.set_page_config(
    page_title="Simulador Científico de Separación",
    layout="wide"
)

st.title("Simulador Científico de Separación de Mezcla")
st.markdown("Sistema cerrado • Conservación de la masa")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Parámetros")

    sal = st.number_input("Sal (g)", 0.0, step=1.0)
    arena = st.number_input("Arena (g)", 0.0, step=1.0)
    hierro = st.number_input("Hierro (g)", 0.0, step=1.0)

    velocidad = st.slider("Velocidad de simulación", 0.01, 0.2, 0.05)

    masa_total = sal + arena + hierro
    st.metric("Masa total inicial", f"{masa_total:.2f} g")

    iniciar = st.button("Iniciar experimento")

with col2:

    placeholder = st.empty()

    if iniciar and masa_total > 0:

        np.random.seed(2)

        n_sal = int(sal)
        n_arena = int(arena)
        n_hierro = int(hierro)

        sal_x = np.random.uniform(1, 5, n_sal)
        sal_y = np.random.uniform(1, 5, n_sal)

        arena_x = np.random.uniform(1, 5, n_arena)
        arena_y = np.random.uniform(1, 5, n_arena)

        hierro_x = np.random.uniform(1, 5, n_hierro)
        hierro_y = np.random.uniform(1, 5, n_hierro)

        progreso = st.progress(0)

        # ==========================
        # ETAPA 1 – MAGNETISMO
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

            hierro_x += dx / dist * 0.2
            hierro_y += dy / dist * 0.2

            ax.scatter(sal_x, sal_y, s=15)
            ax.scatter(arena_x, arena_y, s=15)
            ax.scatter(hierro_x, hierro_y, s=20)

            ax.text(8.5, 3, "🧲", fontsize=40)

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

            ax.scatter(sal_x, sal_y, s=15)
            ax.scatter(arena_x, arena_y, s=20)
            ax.scatter(hierro_x, hierro_y, s=20)

            placeholder.pyplot(fig)
            progreso.progress((40 + step) / 100)

            time.sleep(velocidad)

        # ==========================
        # ETAPA 3 – EVAPORACIÓN
        # ==========================

        for step in range(30):

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 6)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title("Etapa 3: Evaporación")

            sal_x += 0.05

            ax.scatter(sal_x, sal_y, s=20)
            ax.scatter(arena_x, arena_y, s=20)
            ax.scatter(hierro_x, hierro_y, s=20)

            placeholder.pyplot(fig)
            progreso.progress((70 + step) / 100)

            time.sleep(velocidad)

        progreso.progress(1.0)

        st.success("Proceso completado.")

        st.markdown("---")
        st.subheader("Informe Experimental")

        st.write(f"Masa inicial: {masa_total:.2f} g")
        st.write(f"Masa final: {masa_total:.2f} g")
        st.write("Error experimental: 0.00 %")