import streamlit as st
import pandas as pd
from gspread import service_account

# --- Configuracion de la conexion a Google Sheets ---

CREDENTIALS_FILE = "D:/arcad/Escritorio/JAC/Proyectos/ListaRegalosGemelos/listaregalosgemelos-9aab84e6b567.json"
SPREADSHEET_ID = "1F5IhqmaFbkE-b9DrW62kxDJ1aPd1ntjXcOvUrtiMXRk" 
WORKSHEET_NAME = "lista"

@st.cache_resource
def get_gsheet_data():
    gc = service_account(filename=CREDENTIALS_FILE)
    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.worksheet(WORKSHEET_NAME)
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df, worksheet

def update_gift_status(worksheet, index, new_status):
    worksheet.update_cell(index + 2, 6, new_status)  # Actualiza la columna de estado
    # +2 porque los indices empiezan en 1 y hay encabezado

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

df, worksheet = get_gsheet_data()

for index, row in df.iterrows():
    col1, col2, col3, col4, col5, col6 = st.columns([0.4,2,1.4,1,1.8,1.2])

    with col1:
        st.write(f"**{row['Orden']}**")
    with col2:
        st.write(f"**{row['Categoria']} - {row['Tipo_de_regalo']}**")
    with col3:
        st.write(f"Precio: {row['Precio']}")
    with col4:
        st.markdown(f"[Enlace de Compra]({row['Link_de_compra']})")
    with col5:
        status = row['Nos_confirmas_tu_regalo?']
        options = ["no", "Regalado! =)"]
        default_index = 0 if "no" in status else 1
        new_status = st.selectbox(
            "Estado:",
            options,
            index=default_index,
            key=f"status_selectbox_{index}",
            label_visibility="collapsed"
        )
        st.session_state[f"new_status_{index}"] = new_status
        # Almacenar el nuevo estado en la sesión para que persista al hacer clic en el botón
    with col6:
        if st.button("Guardar", key=f"save_button_{index}"):
            old_status = row['Nos_confirmas_tu_regalo?']
            saved_status = st.session_state.get(f"new_status_{index}", old_status)
            if saved_status != old_status:
                update_gift_status(worksheet, index, saved_status)
                st.success("¡Estado guardado!")
                st.rerun() # Volver a ejecutar para actualizar la vista

st.write("---")
st.markdown("¡Gracias por tu gemelosidad!")