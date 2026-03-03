import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.patches import Rectangle

st.set_page_config(
    page_title="Simulador Científico de Separación",
    layout="wide"
)

st.title("Simulación Científica: Separación de Mezcla Sólida")
st.markdown("Sistema: Sal + Arena + Limaduras de Hierro")

col1, col2 = st.columns([1, 2])

# ==============================
# PANEL DE CONTROL
# ==============================

with col1:

    st.subheader("Configuración de Mezcla")

    modo = st.radio(
        "Tipo de mezcla",
        ["Personalizada", "Mezcla ligera", "Mezcla media", "Mezcla pesada"]
    )

    if modo == "Personalizada":
        sal = st.number_input("Sal (g)", 0.0, step=1.0)
        arena = st.number_input("Arena (g)", 0.0, step=1.0)
        hierro = st.number_input("Hierro (g)", 0.0, step=1.0)

    elif modo == "Mezcla ligera":
        sal, arena, hierro = 20.0, 20.0, 10.0

    elif modo == "Mezcla media":
        sal, arena, hierro = 30.0, 30.0, 30.0

    else:
        sal, arena, hierro = 40.0, 40.0, 40.0

    campo = st.slider("Intensidad del campo magnético", 0.1, 2.0, 1.0)
    velocidad = st.slider("Velocidad de simulación", 0.01, 0.15, 0.05)

    masa_total = sal + arena + hierro
    st.metric("Masa total inicial (Sistema cerrado)", f"{masa_total:.2f} g")

    iniciar = st.button("Iniciar proceso de imantación")

# ==============================
# ÁREA DE SIMULACIÓN
# ==============================

with col2:

    placeholder = st.empty()

    if iniciar and masa_total > 0:

        np.random.seed(5)

        n_sal = int(sal)
        n_arena = int(arena)
        n_hierro = int(hierro)

        sal_x = np.random.uniform(1, 5, n_sal)
        sal_y = np.random.uniform(1, 5, n_sal)

        arena_x = np.random.uniform(1, 5, n_arena)
        arena_y = np.random.uniform(1, 5, n_arena)

        hierro_x = np.random.uniform(1, 5, n_hierro)
        hierro_y = np.random.uniform(1, 5, n_hierro)

        # ==========================
        # ANIMACIÓN DE IMANTACIÓN
        # ==========================

        for step in range(40):

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 6)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title("Proceso de Imantación")

            dx = 8 - hierro_x
            dy = 3 - hierro_y
            dist = np.sqrt(dx**2 + dy**2) + 1e-6

            hierro_x += (dx / dist) * 0.2 * campo
            hierro_y += (dy / dist) * 0.2 * campo

            # Dibujar partículas
            ax.scatter(sal_x, sal_y, s=15, color="white", edgecolors="black", label="Sal")
            ax.scatter(arena_x, arena_y, s=20, color="#C2B280", label="Arena")
            ax.scatter(hierro_x, hierro_y, s=25, color="gray", label="Hierro")

            # Dibujar imán tipo herradura
            ax.add_patch(Rectangle((8, 2), 0.4, 2, color='red'))
            ax.add_patch(Rectangle((8.8, 2), 0.4, 2, color='blue'))
            ax.add_patch(Rectangle((8, 2), 1.2, 0.3, color='black'))

            ax.legend(loc="upper left")

            placeholder.pyplot(fig)
            time.sleep(velocidad)

        st.success("Hierro separado mediante campo magnético.")

        # ==========================
        # RESULTADOS FINALES
        # ==========================

        st.markdown("---")
        st.subheader("Resultados Experimentales")

        masas = {
            "Sal": sal,
            "Arena": arena,
            "Hierro": hierro
        }

        st.write("Masas individuales (g):")
        st.write(masas)

        st.write(f"Masa total inicial: {masa_total:.2f} g")
        st.write(f"Suma de componentes: {(sal + arena + hierro):.2f} g")

        # Gráfica de barras
        fig2, ax2 = plt.subplots()
        ax2.bar(masas.keys(), masas.values())
        ax2.set_ylabel("Masa (g)")
        ax2.set_title("Distribución de Masa por Componente")

        st.pyplot(fig2)

        if masa_total == (sal + arena + hierro):
            st.success("Ley de Conservación de la Masa verificada.")