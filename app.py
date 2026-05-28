import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import json

# Config
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

def connect_gsheet():
    creds_dict = json.loads(st.secrets["gcp_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    # Reemplaza con el ID de tu hoja: 1lnrcy5-dyr-zZB4RFeQ3GhsZ03xdwVgtVGhmsEXWAfA
    return client.open_by_key("1lnrcy5-dyr-zZB4RFeQ3GhsZ03xdwVgtVGhmsEXWAfA").sheet1

st.title("Sistema de Incidencias de Inventario")

with st.form("registro"):
    producto = st.text_input("Producto y Peso")
    problema = st.text_area("Descripción del Problema")
    responsable = st.selectbox("Responsable", ["Tienda", "Deposito (Laura)"])
    enviar = st.form_submit_button("Registrar Incidencia")

if enviar:
    if producto and problema:
        sheet = connect_gsheet()
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        sheet.append_row([fecha, producto, problema, responsable])
        st.success("¡Incidencia registrada con éxito!")
    else:
        st.error("Por favor, llena todos los campos.")

st.subheader("Historial de incidencias")
try:
    sheet = connect_gsheet()
    data = sheet.get_all_records()
    if data:
        df = pd.DataFrame(data)
        st.table(df)
    else:
        st.write("No hay datos aún.")
except Exception as e:
    st.write(f"Error: {e}")
    st.write("No hay datos aún o la conexión falló.")
