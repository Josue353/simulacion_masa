import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Laboratorio Virtual - Conservación de la Masa", layout="wide")

# =============================
# ESTILO VISUAL
# =============================
st.markdown("""
<style>
.main-title {
    font-size:40px;
    font-weight:700;
    text-align:center;
}
.section-title {
    font-size:24px;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧪 Laboratorio Virtual de Separación de Mezclas</div>', unsafe_allow_html=True)
st.markdown("### ⚖️ Verificación Experimental de la Ley de Conservación de la Masa")
st.divider()

# =============================
# SIDEBAR - CONTROL DE EXPERIMENTO
# =============================
st.sidebar.header("⚙️ Configuración del Experimento")

sal = st.sidebar.number_input("🧂 Sal (g)", min_value=0.0, step=1.0)
arena = st.sidebar.number_input("🏖️ Arena (g)", min_value=0.0, step=1.0)
hierro = st.sidebar.number_input("🧲 Hierro (g)", min_value=0.0, step=1.0)

masa_inicial = sal + arena + hierro

st.sidebar.divider()
st.sidebar.metric("⚖️ Masa Total Inicial", f"{masa_inicial} g")

# =============================
# PASO 1
# =============================
st.markdown('<div class="section-title">🔹 Paso 1: Preparación de la Mezcla</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.info("Sistema cerrado: no entra ni sale materia.")
    st.write(f"🧂 Sal: {sal} g")
    st.write(f"🏖️ Arena: {arena} g")
    st.write(f"🧲 Hierro: {hierro} g")

with col2:
    fig1, ax1 = plt.subplots()
    ax1.pie(
        [sal, arena, hierro],
        labels=["Sal", "Arena", "Hierro"],
        autopct="%1.1f%%"
    )
    ax1.set_title("Composición de la Mezcla")
    st.pyplot(fig1)

st.divider()

# =============================
# PASO 2
# =============================
st.markdown('<div class="section-title">🧲 Paso 2: Separación Magnética</div>', unsafe_allow_html=True)

if st.button("Aplicar Imán"):
    st.success("El hierro ha sido atraído por el imán.")

    masa_final = sal + arena + hierro

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📦 Componentes Recuperados")
        st.write(f"🧂 Sal: {sal} g")
        st.write(f"🏖️ Arena: {arena} g")
        st.write(f"🧲 Hierro: {hierro} g")

    with col4:
        fig2, ax2 = plt.subplots()
        ax2.bar(
            ["Sal", "Arena", "Hierro"],
            [sal, arena, hierro]
        )
        ax2.set_ylabel("Masa (g)")
        ax2.set_title("Distribución después de la separación")
        st.pyplot(fig2)

    st.divider()

    # =============================
    # VERIFICACIÓN FINAL
    # =============================
    st.markdown('<div class="section-title">⚖️ Verificación de Conservación de la Masa</div>', unsafe_allow_html=True)

    col5, col6 = st.columns(2)

    with col5:
        st.metric("Masa Inicial", f"{masa_inicial} g")
        st.metric("Masa Final", f"{masa_final} g")

        if masa_inicial == masa_final:
            st.success("✅ Se cumple la Ley de Conservación de la Masa.")
        else:
            st.error("❌ No se conserva la masa.")

    with col6:
        fig3, ax3 = plt.subplots()
        ax3.bar(
            ["Inicial", "Final"],
            [masa_inicial, masa_final]
        )
        ax3.set_ylabel("Masa (g)")
        ax3.set_title("Comparación Final")
        st.pyplot(fig3)