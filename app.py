import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# ==============================
# CONFIGURACIÓN GENERAL
# ==============================

st.set_page_config(
    page_title="Simulación de Separación de Mezclas",
    layout="wide"
)

st.title("Simulación Científica: Separación de Mezcla")

st.markdown("---")

# ==============================
# PANEL IZQUIERDO – CONTROL
# ==============================

col_control, col_sim = st.columns([1, 2])

with col_control:
    st.subheader("Parámetros del Experimento")

    sal = st.number_input("Masa de Sal (g)", min_value=0.0, value=0.0, step=1.0)
    arena = st.number_input("Masa de Arena (g)", min_value=0.0, value=0.0, step=1.0)
    hierro = st.number_input("Masa de Hierro (g)", min_value=0.0, value=0.0, step=1.0)

    masa_total = sal + arena + hierro

    st.markdown("---")
    st.metric("Masa Total Inicial (Sistema Cerrado)", f"{masa_total:.2f} g")

    iniciar = st.button("Iniciar proceso de separación")

# ==============================
# PANEL DERECHO – SIMULACIÓN
# ==============================

with col_sim:

    st.subheader("Área de Simulación")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Sistema Inicial")

    # Generación inicial de partículas
    np.random.seed(1)

    n_sal = int(sal)
    n_arena = int(arena)
    n_hierro = int(hierro)

    sal_x = np.random.uniform(1, 5, n_sal)
    sal_y = np.random.uniform(1, 5, n_sal)

    arena_x = np.random.uniform(1, 5, n_arena)
    arena_y = np.random.uniform(1, 5, n_arena)

    hierro_x = np.random.uniform(1, 5, n_hierro)
    hierro_y = np.random.uniform(1, 5, n_hierro)

    # Dibujar sistema inicial
    ax.scatter(sal_x, sal_y, label="Sal", s=20)
    ax.scatter(arena_x, arena_y, label="Arena", s=20)
    ax.scatter(hierro_x, hierro_y, label="Hierro", s=20)

    # Dibujar imán
    ax.text(8.5, 3, "🧲", fontsize=40)

    ax.legend(loc="upper right")

    placeholder = st.empty()
    placeholder.pyplot(fig)

    # ==============================
    # ANIMACIÓN DE SEPARACIÓN
    # ==============================

    if iniciar and masa_total > 0:

        st.info("Aplicando campo magnético...")

        for step in range(30):

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 6)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title("Separación Magnética en Proceso")

            # Movimiento progresivo del hierro hacia el imán
            hierro_x = hierro_x + (8 - hierro_x) * 0.08
            hierro_y = hierro_y + (3 - hierro_y) * 0.08

            ax.scatter(sal_x, sal_y, s=20)
            ax.scatter(arena_x, arena_y, s=20)
            ax.scatter(hierro_x, hierro_y, s=20)

            ax.text(8.5, 3, "🧲", fontsize=40)

            placeholder.pyplot(fig)
            time.sleep(0.05)

        st.success("Hierro separado mediante imantación.")

        # Mostrar sistema final
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("Sistema Tras Separación Magnética")

        ax.scatter(sal_x, sal_y, s=20)
        ax.scatter(arena_x, arena_y, s=20)
        ax.scatter(hierro_x, hierro_y, s=20)

        ax.text(8.5, 3, "🧲", fontsize=40)

        placeholder.pyplot(fig)

        st.markdown("---")
        st.metric("Masa Final del Sistema", f"{masa_total:.2f} g")
        st.caption("Ley de Conservación de la Masa verificada: Sistema cerrado.")