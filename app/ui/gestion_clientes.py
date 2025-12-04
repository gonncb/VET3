import streamlit as st
from app.services.clinic_service import ClinicService

def mostrar_gestion_clientes(service: ClinicService):
    st.header("👥 Gestión de Clientes")
    
    tab_registro, tab_listado = st.tabs(["📝 Nuevo Cliente", "📋 Listado Clientes"])
    
    # --- PESTAÑA 1: REGISTRO ---
    with tab_registro:
        st.subheader("Alta de Cliente y Mascota")
        
        # AQUI ESTÁ EL CAMBIO: clear_on_submit=True
        with st.form("form_alta_cliente", clear_on_submit=True):
            c1, c2 = st.columns(2)
            dni = c1.text_input("DNI")
            nombre = c2.text_input("Nombre Completo")
            telefono = c1.text_input("Teléfono")
            
            st.divider()
            st.caption("Datos de la primera mascota")
            nombre_mascota = c1.text_input("Nombre Mascota")
            especie = c2.selectbox("Especie", ["Perro", "Gato", "Ave", "Exótico", "Roedor"])
            
            btn_guardar = st.form_submit_button("Registrar")
            
            if btn_guardar:
                if dni and nombre and nombre_mascota:
                    exito = service.registrar_cliente_completo(dni, nombre, telefono, nombre_mascota, especie)
                    if exito:
                        st.success(f"✅ Cliente {nombre} registrado con éxito.")
                    else:
                        st.error("⚠️ Error: Ese DNI ya está registrado en el sistema.")
                else:
                    st.warning("Faltan datos obligatorios (DNI, Nombre, Mascota).")

    # --- PESTAÑA 2: LISTADO ---
    with tab_listado:
        st.subheader("Base de Datos de Clientes")
        clientes = service.obtener_todos_clientes()
        
        if clientes:
            datos = []
            for c in clientes:
                nombres_mascotas = ", ".join([m.nombre for m in c.mascotas])
                datos.append({
                    "DNI": c.dni,
                    "Nombre": c.nombre,
                    "Teléfono": c.telefono,
                    "Mascotas": nombres_mascotas
                })
            st.dataframe(datos, use_container_width=True)
        else:
            st.info("No hay clientes registrados todavía.")