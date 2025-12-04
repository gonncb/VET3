import streamlit as st
from app.services.medical_service import MedicalService

def mostrar_gestion_historiales(service: MedicalService):
    st.header("📋 Historial Clínico Digital")
    
    # Buscador fuera del form
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
            
            tab_ver, tab_nuevo = st.tabs(["📜 Ver Historial Previo", "➕ Nueva Consulta"])
            
            with tab_ver:
                historial = service.obtener_historial_mascota(mascota_obj.id)
                if historial:
                    for entrada in historial:
                        # Usamos try/except por si acaso hay datos antiguos sin vet asignado
                        try:
                            nombre_vet = entrada.veterinario.nombre
                        except:
                            nombre_vet = "Desconocido"
                            
                        with st.expander(f"{entrada.fecha} - {entrada.diagnostico} (Dr. {nombre_vet})"):
                            st.write(f"**Descripción:** {entrada.descripcion}")
                else:
                    st.info("Este paciente no tiene historial registrado.")
            
            with tab_nuevo:
                st.subheader(f"Nueva entrada para {mascota_obj.nombre}")
                
                # AQUI ESTÁ EL CAMBIO: clear_on_submit=True
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
                            # NOTA: Hemos quitado st.rerun() para que se vea el mensaje y se limpie el form.
                        else:
                            st.error("Debes rellenar diagnóstico y descripción.")
        else:
            st.warning("No se encuentra cliente con ese DNI.")