import streamlit as st
from app.services.medical_service import MedicalService

def mostrar_gestion_historiales(service: MedicalService):
    st.header("📋 Historial Clínico Digital")
    
    # Buscador (Fuera del form para no perder el estado)
    dni_search = st.text_input("Buscar Dueño por DNI:", key="hist_dni_search")
    
    if dni_search:
        cliente = service.buscar_cliente_por_dni(dni_search)
        
        if cliente:
            st.info(f"Propietario: {cliente.nombre} | Tel: {cliente.telefono}")
            
            opciones_mascotas = {m.nombre: m for m in cliente.mascotas}
            
            if not opciones_mascotas:
                st.warning("Este cliente no tiene mascotas registradas.")
                return

            nombre_mascota = st.selectbox("Seleccionar Paciente:", list(opciones_mascotas.keys()))
            mascota_obj = opciones_mascotas[nombre_mascota]
            
            st.divider()
            
            tab_ver, tab_nuevo = st.tabs(["📜 Ver y Gestionar Historial", "➕ Nueva Consulta"])
            
            # --- PESTAÑA 1: VER, EDITAR Y BORRAR ---
            with tab_ver:
                historial = service.obtener_historial_mascota(mascota_obj.id)
                if historial:
                    for entrada in historial:
                        try:
                            nombre_vet = entrada.veterinario.nombre
                        except:
                            nombre_vet = "Desconocido"
                            
                        # Usamos un expander para cada entrada médica
                        with st.expander(f"📅 {entrada.fecha} | {entrada.diagnostico} (Dr. {nombre_vet})"):
                            st.write(f"**Descripción:** {entrada.descripcion}")
                            
                            st.divider()
                            
                            # Columnas para los botones de acción
                            col_edit, col_delete = st.columns([1, 4])
                            
                            # BOTÓN EDITAR (Popover)
                            with col_edit:
                                with st.popover("✏️ Editar"):
                                    with st.form(f"form_edit_hist_{entrada.id}"):
                                        st.write("Modificar Entrada")
                                        nuevo_diag = st.text_input("Diagnóstico", value=entrada.diagnostico)
                                        nueva_desc = st.text_area("Descripción", value=entrada.descripcion)
                                        
                                        if st.form_submit_button("Guardar Cambios"):
                                            service.actualizar_consulta(entrada.id, nuevo_diag, nueva_desc)
                                            st.success("Actualizado")
                                            st.rerun()

                            # BOTÓN BORRAR
                            with col_delete:
                                if st.button("🗑️ Borrar", key=f"del_hist_{entrada.id}"):
                                    service.eliminar_consulta(entrada.id)
                                    st.toast("Entrada eliminada correctamente")
                                    st.rerun()
                else:
                    st.info("Este paciente no tiene historial registrado.")
            
            # --- PESTAÑA 2: NUEVA CONSULTA ---
            with tab_nuevo:
                st.subheader(f"Nueva entrada para {mascota_obj.nombre}")
                
                with st.form("form_historial", clear_on_submit=True):
                    diagnostico = st.text_input("Diagnóstico Breve (ej: Otitis)")
                    descripcion = st.text_area("Descripción detallada / Tratamiento")
                    
                    guardar = st.form_submit_button("Guardar Consulta")
                    
                    if guardar:
                        if diagnostico and descripcion:
                            usuario_actual = st.session_state['usuario']
                            service.registrar_consulta(
                                id_mascota=mascota_obj.id,
                                id_veterinario=usuario_actual.id,
                                diagnostico=diagnostico,
                                descripcion=descripcion
                            )
                            st.success("✅ Historial actualizado correctamente.")
                        else:
                            st.error("Debes rellenar diagnóstico y descripción.")
        else:
            st.warning("No se encuentra cliente con ese DNI.")