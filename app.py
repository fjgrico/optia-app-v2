
import streamlit as st
from utils.procesar import superponer_gafas
import tempfile
from PIL import Image

st.set_page_config(page_title="Prueba Inteligente de Gafas - OPTIA V2", layout="centered")

st.title("🤖 OPTIA V2 - Gafas con IA")
st.write("Sube una foto clara de tu rostro. Usamos IA para colocar las gafas automáticamente sobre tus ojos.")

foto = st.file_uploader("📷 Sube tu foto (formato JPG o PNG)", type=["jpg", "jpeg", "png"])
modelo = st.selectbox("🕶️ Elige un modelo de gafas", ["modelo1", "modelo2"])

if foto:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(foto.read())
        tmp_path = tmp.name

    resultado = superponer_gafas(tmp_path, f"gafas/{modelo}.png")
    st.image(resultado, caption="Resultado con gafas colocadas automáticamente", use_column_width=True)

    st.download_button("📥 Descargar imagen", data=resultado.tobytes(), file_name="gafas_ia.png", mime="image/png")
