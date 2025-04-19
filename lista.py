import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client, Client
#import gspread
#from google.oauth2.service_account import Credentials

load_dotenv()
supabase_url = st.secrets["SUPABASE_URL"]
supabase_anon_key = st.secrets["SUPABASE_ANON_KEY"]
supabase: Client = create_client(supabase_url, supabase_anon_key)
##supabase_url = os.environ.get("SUPABASE_URL")
##supabase_anon_key = os.environ.get("SUPABASE_ANON_KEY")

@st.cache_resource
def get_supabase_data():
    data = supabase.table("lista_regalos").select("*").execute()
    df = pd.DataFrame(data.data)  # Extrae los datos correctamente
    return df

def update_gift_status(index, new_status):
    confirmed_value = True if new_status == "Regalado! =)" else False
    data, count = supabase.table("lista_regalos").update({"confirmado": confirmed_value}).eq("orden", index + 1).execute()
    return data, count

# --- Configuracion de la conexion a Google Sheets 1 --- #
#CREDENTIALS_INFO = {
#    "type": os.environ.get("GOOGLE_SHEETS_TYPE"),
#    "project_id": os.environ.get("GOOGLE_SHEETS_PROJECT_ID"),
#    "private_key_id": os.environ.get("GOOGLE_SHEETS_PRIVATE_KEY_ID"),
#    "private_key": os.environ.get("GOOGLE_SHEETS_PRIVATE_KEY").replace('\\n', '\n'),
#    "client_email": os.environ.get("GOOGLE_SHEETS_CLIENT_EMAIL"),
#    "client_id": os.environ.get("GOOGLE_SHEETS_CLIENT_ID"),
#    "auth_uri": os.environ.get("GOOGLE_SHEETS_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
#    "token_uri": os.environ.get("GOOGLE_SHEETS_TOKEN_URI", "https://oauth2.googleapis.com/token"),
#    "auth_provider_x509_cert_url": os.environ.get("GOOGLE_SHEETS_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
#    "client_x509_cert_url": os.environ.get("GOOGLE_SHEETS_CLIENT_X509_CERT_URL"),
#    "universe_domain": os.environ.get("GOOGLE_SHEETS_UNIVERSE_DOMAIN", "googleapis.com")
#}
#SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
#WORKSHEET_NAME = os.environ.get("WORKSHEET_NAME")
#SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# --- Configuracion de la conexion a Google Sheets 2 --- #
#@st.cache_resource
#def get_gsheet_data():
#    creds = Credentials.from_service_account_info(CREDENTIALS_INFO, scopes=SCOPES)  
#    gc = gspread.authorize(creds)  # Autentica con las credenciales
#    sh = gc.open_by_key(SPREADSHEET_ID)
#    worksheet = sh.worksheet(WORKSHEET_NAME)
#    data = worksheet.get_all_values()
#    df = pd.DataFrame(data[1:], columns=data[0])
#    return df, worksheet
#def update_gift_status(worksheet, index, new_status):
#    worksheet.update_cell(index + 2, 6, new_status)  # Actualiza la columna estado

# --- Diseño de la aplicación ---

st.title("Lista de Regalos para AXEL & MAXI")
st.markdown("¡Prepárense para una doble dosis de amor! Los gemelos ya casi están aquí, ¡y nuestra emoción no cabe en el pecho!")
st.markdown("Su cariño es el regalo más grande, y para ayudarnos a darles la bienvenida a esta familia, hemos preparado una lista de cositas especiales para estos dos pequeños aventureros.")
st.markdown("Si gustan participar en esta emocionante etapa, los invitamos con mucha alegría a explorar nuestra lista, elegir un regalo, ir al enlace de compra y confirmanos con un Regalado! =)")
st.markdown("Estaremos felices de recibir sus obsequios el 02 de mayo en esta dirección: Jr. Paucartambo 285 Independencia, Referencia a la Altura de la Comisaria de Tahuantinsuyo.")
st.markdown("¡Si no pueden ese día, no se preocupen! Cualquier otro día será genial. Solo recuerden que el 03 de mayo estaremos celebrando el Baby Shower fuera de casa.")
st.markdown("Ojo los enlaces de compra de Falabella son referenciales, si ves el mismo producto en otra tienda no dudes en comprarlo, avísanos si debemos ir por ellos.")
st.markdown("Cualquier duda o mensaje no dudes en escribirnos al Whatsapp de Claudine 940959197 o Jose Luis 986109315.")
st.markdown("¡Gracias por ser parte de esta maravillosa aventura gemelar!")
st.write("---")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://i.postimg.cc/7Ys2s4P2/Fondo-Pantalla-BShower.png") !important;
        background-size: cover !important;
        background-repeat: no-repeat !important;
        background-position: center !important;        
    }}   
    h1 {{
        color: white !important;
    }}
    .stMarkdown, .stText {{
        color: white !important;
    }}  
    div.stButton button{{
        margin-top: 0em !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        height: auto !important;
        line-height: 1 !important;
        background-color: green;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

#df, worksheet = get_gsheet_data()
df = get_supabase_data()

for index, row in df.iterrows():
    col1, col2, col3, col4, col5, col6 = st.columns([0.4,2,1.4,1,1.8,1.2])

    with col1:
        st.write(f"**{row['orden']}**")
    with col2:
        st.write(f"**{row['categoria']} - {row['tipo_regalo']}**")
    with col3:
        st.write(f"Precio: S/.{float(row['precio']):.2f}")
    with col4:
        st.markdown(f"[Enlace de Compra]({row['link_compra']})")
    with col5:
        status = row['confirmado']
        options = ["no", "Regalado! =)"]
        #default_index = 0 if "no" in status else 1
        default_index = 0 if status is False else 1  # Evalúa el booleano correctamente
        new_status = st.selectbox(
            "Estado:",
            options,
            index=default_index,
            key=f"status_selectbox_{index}",
            label_visibility="collapsed"
        )
        st.session_state[f"new_status_{index}"] = new_status # Almacenar nuevo estado con Guardar
    with col6:
        if st.button("Guardar", key=f"save_button_{index}"):
            saved_status = st.session_state.get(f"new_status_{index}", "no")
            #update_gift_status(worksheet, index, saved_status)
            update_gift_status(index, saved_status)
            st.success("¡Estado guardado!")
            st.rerun()

st.write("---")
st.markdown("¡Gracias por tu gemelosidad!")