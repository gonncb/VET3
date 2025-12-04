import streamlit as st
from datetime import datetime, time
from app.services.cita_service import CitaService

def mostrar_gestion_citas(service: CitaService):
    st.header("📅 Gestión de Citas Médicas")
    
    tab_nueva, tab_ver = st.tabs(["➕ Nueva Cita", "👁️ Ver Agenda"])
    
    # --- PESTAÑA 1: PEDIR CITA ---
    with tab_nueva:
        st.subheader("Reservar Cita")
        
        # El buscador va FUERA del formulario para que no se borre al buscar
        dni_busqueda = st.text_input("Buscar Cliente por DNI:", key="cita_dni_search")
        
        if dni_busqueda:
            cliente = service.buscar_cliente_por_dni(dni_busqueda)
            
            if cliente:
                st.success(f"Cliente: {cliente.nombre}")
                
                # AQUI ESTÁ EL CAMBIO: clear_on_submit=True
                with st.form("form_crear_cita", clear_on_submit=True):
                    col1, col2 = st.columns(2)
                    
                    # A. Selector de Mascota
                    opciones_mascotas = {m.nombre: m.id for m in cliente.mascotas}
                    if not opciones_mascotas:
                        st.warning("Este cliente no tiene mascotas.")
                        st.form_submit_button("Cancelar")
                        return

                    nombre_mascota = col1.selectbox("Paciente (Mascota)", list(opciones_mascotas.keys()))
                    id_mascota_selec = opciones_mascotas[nombre_mascota]
                    
                    # B. Selector de Veterinario
                    vets = service.obtener_veterinarios_formateados()
                    opciones_vets = {f"{v.nombre} ({v.especialidad})": v.id for v in vets}
                    
                    nombre_vet = col2.selectbox("Veterinario", list(opciones_vets.keys()))
                    id_vet_selec = opciones_vets[nombre_vet]
                    
                    # C. Fecha y Hora
                    fecha = col1.date_input("Fecha", min_value=datetime.today())
                    hora_selec = col2.time_input("Hora", value=time(9, 0))
                    
                    motivo = st.text_area("Motivo de la consulta")
                    
                    if st.form_submit_button("Confirmar Cita"):
                        service.crear_cita(fecha, hora_selec, motivo, id_mascota_selec, id_vet_selec)
                        st.success("✅ Cita agendada correctamente.")
            else:
                st.info("Introduce un DNI válido para ver las mascotas.")

    # --- PESTAÑA 2: VER AGENDA ---
    with tab_ver:
        citas = service.obtener_historial_citas()
        if citas:
            datos = []
            for c in citas:
                datos.append({
                    "Fecha": c.fecha,
                    "Hora": c.hora,
                    "Paciente": c.mascota.nombre,
                    "Veterinario": c.veterinario.nombre,
                    "Motivo": c.motivo
                })
            st.dataframe(datos, use_container_width=True)
        else:
            st.info("No hay citas programadas.")