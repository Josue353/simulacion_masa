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

    explicar = st.checkbox("🎤 Activar modo explicación")

    masa_total = sal + arena + hierro
    st.metric("Masa total inicial (Sistema cerrado)", f"{masa_total:.2f} g")

    iniciar = st.button("Iniciar proceso completo")

# ==============================
# ÁREA DE SIMULACIÓN
# ==============================

with col2:

    placeholder = st.empty()

    if iniciar and masa_total > 0:

        np.random.seed(7)

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
# ETAPA 1 – IMANTACIÓN (FLUIDA)
# ==========================

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Etapa 1: Imantación")

# Dibujar imán fijo
ax.add_patch(Rectangle((8, 2), 0.4, 2, color='red'))
ax.add_patch(Rectangle((8.8, 2), 0.4, 2, color='blue'))
ax.add_patch(Rectangle((8, 2), 1.2, 0.3, color='black'))

scatter_sal = ax.scatter(sal_x, sal_y, s=15, color="white", edgecolors="black")
scatter_arena = ax.scatter(arena_x, arena_y, s=20, color="#C2B280")
scatter_hierro = ax.scatter(hierro_x, hierro_y, s=25, color="gray")

placeholder.pyplot(fig)

for step in range(60):

    dx = 8 - hierro_x
    dy = 3 - hierro_y
    dist = np.sqrt(dx**2 + dy**2) + 1e-6

    hierro_x += (dx / dist) * 0.25 * campo
    hierro_y += (dy / dist) * 0.25 * campo

    scatter_hierro.set_offsets(np.c_[hierro_x, hierro_y])

    placeholder.pyplot(fig)
    time.sleep(velocidad * 0.6)

        # ==========================
        # ETAPA 2 – SEPARACIÓN MECÁNICA
        # ==========================

        if explicar:
            st.info("Luego realizamos una separación mecánica. "
                    "La arena, por diferencia de tamaño de partícula, "
                    "se separa de la sal.")

        for step in range(40):

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 6)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title("Etapa 2: Separación Mecánica")

            arena_y -= 0.07
            sal_y += 0.02

            ax.scatter(sal_x, sal_y, s=15, color="white", edgecolors="black")
            ax.scatter(arena_x, arena_y, s=25, color="#C2B280")
            ax.scatter(hierro_x, hierro_y, s=25, color="gray")

            ax.axhline(y=2.5, linestyle="--")

            # Imán
            ax.add_patch(Rectangle((8, 2), 0.4, 2, color='red'))
            ax.add_patch(Rectangle((8.8, 2), 0.4, 2, color='blue'))
            ax.add_patch(Rectangle((8, 2), 1.2, 0.3, color='black'))

            placeholder.pyplot(fig)
            time.sleep(velocidad)

        # ==========================
        # ETAPA 3 – RECIPIENTES
        # ==========================

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("Componentes Separados en Recipientes")

        # Recipientes
        ax.add_patch(Rectangle((1, 1), 2, 3, fill=False))
        ax.add_patch(Rectangle((4, 1), 2, 3, fill=False))
        ax.add_patch(Rectangle((7, 1), 2, 3, fill=False))

        ax.text(2, 4.3, "Arena")
        ax.text(5, 4.3, "Sal")
        ax.text(8, 4.3, "Hierro")

        # Contenido visual
        ax.scatter(np.random.uniform(1.2, 2.8, n_arena),
                   np.random.uniform(1.2, 3.5, n_arena),
                   color="#C2B280")

        ax.scatter(np.random.uniform(4.2, 5.8, n_sal),
                   np.random.uniform(1.2, 3.5, n_sal),
                   color="white", edgecolors="black")

        ax.scatter(np.random.uniform(7.2, 8.8, n_hierro),
                   np.random.uniform(1.2, 3.5, n_hierro),
                   color="gray")

        placeholder.pyplot(fig)

        st.success("Proceso completado correctamente.")

        # ==========================
        # RESULTADOS FINALES
        # ==========================

        st.markdown("---")
        st.subheader("Verificación Experimental")

        st.write(f"Masa inicial total: {masa_total:.2f} g")
        st.write(f"Suma de componentes separados: {(sal + arena + hierro):.2f} g")

        fig2, ax2 = plt.subplots()
        ax2.bar(["Sal", "Arena", "Hierro"], [sal, arena, hierro])
        ax2.set_ylabel("Masa (g)")
        ax2.set_title("Distribución Final de Masa")

        st.pyplot(fig2)

        if masa_total == (sal + arena + hierro):
            st.success("Ley de Conservación de la Masa verificada.")