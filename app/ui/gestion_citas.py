import streamlit as st
from datetime import datetime, time
from app.services.cita_service import CitaService

def mostrar_gestion_citas(service: CitaService):
    st.header("📅 Gestión de Citas Médicas")
    
    tab_nueva, tab_ver = st.tabs(["➕ Nueva Cita", "👁️ Ver Agenda y Cancelar"])
    
    # --- PESTAÑA 1: PEDIR CITA (Igual que antes) ---
    with tab_nueva:
        st.subheader("Reservar Cita")
        dni_busqueda = st.text_input("Buscar Cliente por DNI:", key="cita_dni_search")
        
        if dni_busqueda:
            cliente = service.buscar_cliente_por_dni(dni_busqueda)
            if cliente:
                st.success(f"Cliente: {cliente.nombre}")
                with st.form("form_crear_cita", clear_on_submit=True):
                    col1, col2 = st.columns(2)
                    
                    opciones_mascotas = {m.nombre: m.id for m in cliente.mascotas}
                    if not opciones_mascotas:
                        st.warning("Este cliente no tiene mascotas.")
                        st.form_submit_button("Cancelar")
                        return

                    nombre_mascota = col1.selectbox("Paciente (Mascota)", list(opciones_mascotas.keys()))
                    id_mascota_selec = opciones_mascotas[nombre_mascota]
                    
                    vets = service.obtener_veterinarios_formateados()
                    opciones_vets = {f"{v.nombre} ({v.especialidad})": v.id for v in vets}
                    nombre_vet = col2.selectbox("Veterinario", list(opciones_vets.keys()))
                    id_vet_selec = opciones_vets[nombre_vet]
                    
                    fecha = col1.date_input("Fecha", min_value=datetime.today())
                    hora_selec = col2.time_input("Hora", value=time(9, 0))
                    motivo = st.text_area("Motivo de la consulta")
                    
                    if st.form_submit_button("Confirmar Cita"):
                        service.crear_cita(fecha, hora_selec, motivo, id_mascota_selec, id_vet_selec)
                        st.success("✅ Cita agendada correctamente.")
            else:
                st.info("Introduce un DNI válido.")

    # --- PESTAÑA 2: VER AGENDA (¡ACTUALIZADO!) ---
    with tab_ver:
        citas = service.obtener_historial_citas()
        if citas:
            st.subheader("Próximas Citas")
            for cita in citas:
                # Usamos columnas para simular una tabla con botón
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 1])
                
                col1.write(f"📅 **{cita.fecha}**")
                col2.write(f"⏰ {cita.hora}")
                col3.write(f"🐾 {cita.mascota.nombre}")
                col4.write(f"🩺 {cita.veterinario.nombre}")
                
                # Botón de borrar (pequeño y rojo si es posible, pero Streamlit es limitado en estilos)
                if col5.button("❌", key=f"del_cita_{cita.id}", help="Cancelar Cita"):
                    service.cancelar_cita(cita.id)
                    st.toast("Cita cancelada correctamente") # Mensaje flotante elegante
                    st.rerun()
                
                st.divider() # Línea separadora
        else:
            st.info("No hay citas programadas.")