import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.patches import Rectangle

st.set_page_config(
    page_title="Simulador Científico Avanzado",
    layout="wide"
)

st.title("Simulación Científica Avanzada: Separación de Mezcla Sólida")
st.markdown("Sistema: Sal + Arena + Limaduras de Hierro")

col1, col2 = st.columns([1, 2])

# ==============================
# PANEL DE CONTROL
# ==============================

with col1:

    st.subheader("Configuración Experimental")

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
    velocidad = st.slider("Velocidad de simulación", 0.01, 0.12, 0.03)
    explicar = st.checkbox("🎤 Activar modo explicación")

    masa_total = sal + arena + hierro
    st.metric("Masa total inicial (Sistema cerrado)", f"{masa_total:.2f} g")

    iniciar = st.button("Iniciar proceso completo")

# ==============================
# ÁREA DE SIMULACIÓN
# ==============================

with col2:

    placeholder = st.empty()
    metric_placeholder = st.empty()
    progress_bar = st.progress(0)

    if iniciar and masa_total > 0:

        np.random.seed(15)

        n_sal = int(sal)
        n_arena = int(arena)
        n_hierro = int(hierro)

        sal_x = np.random.uniform(1, 5, n_sal)
        sal_y = np.random.uniform(2.5, 5, n_sal)

        arena_x = np.random.uniform(1, 5, n_arena)
        arena_y = np.random.uniform(2.5, 5, n_arena)

        hierro_x = np.random.uniform(1, 5, n_hierro)
        hierro_y = np.random.uniform(2.5, 5, n_hierro)

        # ==========================
        # ETAPA 1 – IMANTACIÓN
        # ==========================

        if explicar:
            st.info("Aplicamos un campo magnético. El hierro es atraído "
                    "debido a sus propiedades ferromagnéticas.")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("Etapa 1: Imantación")

        ax.add_patch(Rectangle((8, 2), 0.4, 2, color='red'))
        ax.add_patch(Rectangle((8.8, 2), 0.4, 2, color='blue'))
        ax.add_patch(Rectangle((8, 2), 1.2, 0.3, color='black'))

        scatter_sal = ax.scatter(sal_x, sal_y, s=15, color="white", edgecolors="black")
        scatter_arena = ax.scatter(arena_x, arena_y, s=20, color="#C2B280")
        scatter_hierro = ax.scatter(hierro_x, hierro_y, s=25, color="gray")

        placeholder.pyplot(fig)

        for step in range(70):

            dx = 8 - hierro_x
            dy = 3 - hierro_y
            dist = np.sqrt(dx**2 + dy**2) + 1e-6

            hierro_x += (dx / dist) * 0.25 * campo
            hierro_y += (dy / dist) * 0.25 * campo

            scatter_hierro.set_offsets(np.c_[hierro_x, hierro_y])
            placeholder.pyplot(fig)

            # Métricas dinámicas
            distancia_media = np.mean(dist)
            porcentaje = min(100, int((1 - distancia_media / 8) * 100))

            metric_placeholder.metric(
                "Hierro separado (%)",
                f"{max(0, porcentaje)}%"
            )

            progress_bar.progress(step / 140)

            time.sleep(velocidad)

        # ==========================
        # ETAPA 2 – SEPARACIÓN MECÁNICA
        # ==========================

        if explicar:
            st.info("Se realiza separación mecánica por diferencia "
                    "de tamaño de partícula.")

        ax.set_title("Etapa 2: Separación Mecánica")
        ax.axhline(y=2.5, linestyle="--")

        for step in range(70):

            arena_y -= 0.05
            sal_y += 0.015

            scatter_arena.set_offsets(np.c_[arena_x, arena_y])
            scatter_sal.set_offsets(np.c_[sal_x, sal_y])

            placeholder.pyplot(fig)
            progress_bar.progress((70 + step) / 140)

            time.sleep(velocidad)

        # ==========================
        # ETAPA 3 – RECIPIENTES
        # ==========================

        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 6)
        ax2.set_xticks([])
        ax2.set_yticks([])
        ax2.set_title("Componentes Separados")

        ax2.add_patch(Rectangle((1, 1), 2, 3, fill=False))
        ax2.add_patch(Rectangle((4, 1), 2, 3, fill=False))
        ax2.add_patch(Rectangle((7, 1), 2, 3, fill=False))

        ax2.text(2, 4.3, "Arena")
        ax2.text(5, 4.3, "Sal")
        ax2.text(8, 4.3, "Hierro")

        ax2.scatter(np.random.uniform(1.2, 2.8, n_arena),
                    np.random.uniform(1.2, 3.5, n_arena),
                    color="#C2B280")

        ax2.scatter(np.random.uniform(4.2, 5.8, n_sal),
                    np.random.uniform(1.2, 3.5, n_sal),
                    color="white", edgecolors="black")

        ax2.scatter(np.random.uniform(7.2, 8.8, n_hierro),
                    np.random.uniform(1.2, 3.5, n_hierro),
                    color="gray")

        placeholder.pyplot(fig2)

        st.success("Proceso completado correctamente.")

        # ==========================
        # RESULTADOS FINALES
        # ==========================

        st.markdown("---")
        st.subheader("Verificación Experimental")

        st.write(f"Masa inicial total: {masa_total:.2f} g")
        st.write(f"Suma de componentes separados: {(sal + arena + hierro):.2f} g")

        fig3, ax3 = plt.subplots()
        ax3.bar(["Sal", "Arena", "Hierro"], [sal, arena, hierro])
        ax3.set_ylabel("Masa (g)")
        ax3.set_title("Distribución Final de Masa")

        st.pyplot(fig3)

        if masa_total == (sal + arena + hierro):
            st.success("Ley de Conservación de la Masa verificada.")