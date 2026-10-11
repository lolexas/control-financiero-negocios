from datetime import datetime
import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Gestión Financiera - Negocios", page_icon="📊", layout="wide"
)

# Archivo de base de datos local (CSV simple)
DATA_FILE = "registros_financieros.csv"


# Función para cargar datos
def cargar_datos():
  try:
    return pd.read_csv(DATA_FILE)
  except FileNotFoundError:
    # Si no existe, creamos un DataFrame vacío con la estructura correcta
    return pd.DataFrame(
        columns=[
            "Fecha",
            "Negocio",
            "Tipo",
            "Categoria",
            "Monto",
            "Descripcion",
            "Metodo_Pago",
        ]
    )


# Función para guardar datos
def guardar_registro(nuevo_registro):
  df = cargar_datos()
  df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
  df.to_csv(DATA_FILE, index=False)


df_registros = cargar_datos()

# Título Principal
st.title("💼 Control Financiero Multinegocio")
st.markdown(
    "Administra las finanzas de tu **Salón de Belleza** y tu **Venta de"
    " Helados/Hielos** de forma rápida."
)

# --- BARRA LATERAL (MENÚ Y REGISTROS) ---
st.sidebar.header("📝 Nuevo Movimiento")

negocio = st.sidebar.selectbox(
    "Selecciona el Negocio", ["💇‍♀️ Salón de Belleza", "🧊 Helados y Hielos"]
)

tipo = st.sidebar.radio("Tipo de Movimiento", ["Ingreso (Venta)", "Gasto"])

# Categorías dinámicas según el negocio y tipo
if "Salón" in negocio:
  cat_ingresos = [
      "Corte / Peinado",
      "Tintes y Químicos",
      "Manicure / Pedicure",
      "Barbería",
      "Otro Servicio Salón",
  ]
  cat_gastos = [
      "Insumos (Shampoos, Tintes)",
      "Alquiler Local",
      "Servicios (Luz/Agua)",
      "Pago Personal / Comisión",
      "Mantenimiento",
  ]
else:
  cat_ingresos = [
      "Venta de Helados (Popsicles)",
      "Venta de Hielo en Cubo",
      "Venta de Bebidas",
      "Otro Venta Fría",
  ]
  cat_gastos = [
      "Materia Prima / Insumos Helados",
      "Bolsas y Empaques",
      "Electricidad (Congeladoras)",
      "Hielo / Producción",
      "Transporte / Distribución",
  ]

categoria = st.sidebar.selectbox(
    "Categoría", cat_ingresos if tipo == "Ingreso (Venta)" else cat_gastos
)
monto = st.sidebar.number_input("Monto (S/.)", min_value=0.0, format="%.2f")
metodo_pago = st.sidebar.selectbox(
    "Método de Pago", ["Efectivo", "Yape / Plin", "Tarjeta / Transferencia"]
)
descripcion = st.sidebar.text_input("Descripción opcional (Ej: Cliente frecuente)")
fecha = st.sidebar.date_input("Fecha", datetime.now())

if st.sidebar.button("💾 Guardar Registro", type="primary"):
  if monto > 0:
    nuevo = {
        "Fecha": str(fecha),
        "Negocio": negocio,
        "Tipo": "Ingreso" if "Ingreso" in tipo else "Gasto",
        "Categoria": categoria,
        "Monto": monto,
        "Descripcion": descripcion,
        "Metodo_Pago": metodo_pago,
    }
    guardar_registro(nuevo)
    st.sidebar.success("¡Registro guardado con éxito!")
    st.rerun()
  else:
    st.sidebar.error("El monto debe ser mayor a 0.")

# --- CUERPO PRINCIPAL (PANEL DE RESUMEN) ---
if not df_registros.empty:
  # Filtros globales en pantalla
  st.sidebar.markdown("---")
  st.sidebar.header("🔍 Filtros de Visualización")
  negocio_filtro = st.sidebar.selectbox(
      "Filtrar Negocio", ["Todos", "💇‍♀️ Salón de Belleza", "🧊 Helados y Hielos"]
  )

  df_filtrado = df_registros.copy()
  if negocio_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Negocio"] == negocio_filtro]

  # Métricas principales
  total_ingresos = df_filtrado[df_filtrado["Tipo"] == "Ingreso"][
      "Monto"
  ].sum()
  total_gastos = df_filtrado[df_filtrado["Tipo"] == "Gasto"]["Monto"].sum()
  balance_neto = total_ingresos - total_gastos

  col1, col2, col3 = st.columns(3)
  col1.metric("💰 Ingresos Totales", f"S/. {total_ingresos:,.2f}")
  col2.metric("📉 Gastos Totales", f"S/. {total_gastos:,.2f}")
  col3.metric(
      "💎 Balance Neto",
      f"S/. {balance_neto:,.2f}",
      delta=f"S/. {balance_neto:,.2f}",
  )

  st.markdown("---")

  # Visualización de datos
  st.subheader("📋 Historial de Movimientos")
  st.dataframe(
      df_filtrado.sort_values(by="Fecha", ascending=False), use_container_width=True
  )

  # Exportar o limpiar
  col_l1, col_l2 = st.columns(2)
  with col_l1:
    if st.button("🗑️ Borrar Todo el Historial (Cuidado)"):
      pd.DataFrame(columns=df_registros.columns).to_csv(DATA_FILE, index=False)
      st.rerun()
else:
  st.info(
      "👋 ¡Hola! Aún no hay registros guardados. Usa el menú de la izquierda"
      " para registrar tu primera venta o gasto."
  )