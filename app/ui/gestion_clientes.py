import streamlit as st
from app.services.clinic_service import ClinicService

def mostrar_gestion_clientes(service: ClinicService):
    st.header("👥 Gestión de Clientes")
    
    tab_registro, tab_listado = st.tabs(["📝 Nuevo Cliente", "📋 Listado y Edición"])
    
    # --- PESTAÑA 1: REGISTRO ---
    with tab_registro:
        st.subheader("Alta de Cliente y Mascota")
        with st.form("form_alta_cliente", clear_on_submit=True):
            c1, c2 = st.columns(2)
            dni = c1.text_input("DNI")
            nombre = c2.text_input("Nombre Completo")
            telefono = c1.text_input("Teléfono")
            st.divider()
            st.caption("Datos de la primera mascota")
            nombre_mascota = c1.text_input("Nombre Mascota")
            especie = c2.selectbox("Especie", ["Perro", "Gato", "Ave", "Exótico", "Roedor"])
            
            if st.form_submit_button("Registrar"):
                if dni and nombre and nombre_mascota:
                    if service.registrar_cliente_completo(dni, nombre, telefono, nombre_mascota, especie):
                        st.success(f"✅ Cliente {nombre} registrado.")
                    else:
                        st.error("⚠️ Error: Ese DNI ya existe.")
                else:
                    st.warning("Faltan datos.")

    # --- PESTAÑA 2: LISTADO Y EDICIÓN ---
    with tab_listado:
        st.subheader("Directorio de Clientes")
        clientes = service.obtener_todos_clientes()
        
        if clientes:
            for cliente in clientes:
                # Usamos un expander para cada cliente. Es elegante y limpio.
                with st.expander(f"👤 {cliente.nombre} (DNI: {cliente.dni})"):
                    col_info, col_edit = st.columns([2, 1])
                    
                    with col_info:
                        st.write(f"📞 **Teléfono:** {cliente.telefono}")
                        mascotas_str = ", ".join([m.nombre for m in cliente.mascotas])
                        st.write(f"🐾 **Mascotas:** {mascotas_str}")

                    with col_edit:
                        st.write("**Acciones:**")
                        # Botón para borrar
                        if st.button("🗑️ Eliminar Cliente", key=f"del_{cliente.id}"):
                            service.eliminar_cliente(cliente.id)
                            st.rerun() # Recargamos para que desaparezca de la lista
                        
                        # Formulario para editar (dentro del expander)
                        with st.popover("✏️ Editar Datos"):
                            with st.form(f"edit_form_{cliente.id}"):
                                new_name = st.text_input("Nombre", value=cliente.nombre)
                                new_tel = st.text_input("Teléfono", value=cliente.telefono)
                                if st.form_submit_button("Guardar Cambios"):
                                    service.actualizar_cliente(cliente.id, new_name, new_tel)
                                    st.success("Actualizado")
                                    st.rerun()
        else:
            st.info("No hay clientes registrados.")