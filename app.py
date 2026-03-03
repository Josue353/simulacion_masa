import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Conservación de la Masa", layout="centered")

st.title("Simulación: Ley de Conservación de la Masa")

st.write("Ingrese las masas de los componentes (en gramos):")

sal = st.number_input("Masa de sal (g)", min_value=0.0, step=1.0)
arena = st.number_input("Masa de arena (g)", min_value=0.0, step=1.0)
hierro = st.number_input("Masa de hierro (g)", min_value=0.0, step=1.0)

if st.button("Mezclar"):
    masa_inicial = sal + arena + hierro
    masa_final = masa_inicial  # Sistema cerrado

    st.subheader("Resultados")
    st.write(f"Masa total inicial: {masa_inicial} g")
    st.write(f"Masa total final: {masa_final} g")

    if masa_inicial == masa_final:
        st.success("✅ Se cumple la Ley de Conservación de la Masa")
    else:
        st.error("❌ No se conserva la masa")

    etiquetas = ["Masa Inicial", "Masa Final"]
    valores = [masa_inicial, masa_final]

    fig, ax = plt.subplots()
    ax.bar(etiquetas, valores)
    ax.set_ylabel("Masa (g)")
    ax.set_title("Comparación de Masa")

    st.pyplot(fig)