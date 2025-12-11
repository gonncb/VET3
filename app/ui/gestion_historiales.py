import streamlit as st
from app.services.medical_service import MedicalService
from app.services.inventory_service import InventoryService # Necesitamos esto para listar productos

def mostrar_gestion_historiales(medical_service: MedicalService, inventory_service: InventoryService):
    st.header("📋 Historial Clínico Digital")
    
    dni_search = st.text_input("Buscar Dueño por DNI:", key="hist_dni_search")
    
    if dni_search:
        cliente = medical_service.buscar_cliente_por_dni(dni_search)
        
        if cliente:
            st.info(f"Propietario: {cliente.nombre} | Tel: {cliente.telefono}")
            opciones_mascotas = {m.nombre: m for m in cliente.mascotas}
            
            if not opciones_mascotas:
                st.warning("Sin mascotas registradas.")
                return

            nombre_mascota = st.selectbox("Seleccionar Paciente:", list(opciones_mascotas.keys()))
            mascota_obj = opciones_mascotas[nombre_mascota]
            
            st.divider()
            
            tab_ver, tab_nuevo = st.tabs(["📜 Historial", "➕ Nueva Consulta"])
            
            # --- PESTAÑA VER ---
            with tab_ver:
                historial = medical_service.obtener_historial_mascota(mascota_obj.id)
                if historial:
                    for entrada in historial:
                        try:
                            nombre_vet = entrada.veterinario.nombre
                        except:
                            nombre_vet = "Desconocido"
                        
                        with st.expander(f"📅 {entrada.fecha} | {entrada.diagnostico} (Dr. {nombre_vet})"):
                            st.markdown(f"**Descripción:** {entrada.descripcion}")
                            
                            # VISUALIZAR PRODUCTOS USADOS
                            if entrada.productos_utilizados:
                                st.markdown("---")
                                st.caption("💊 Tratamiento / Productos administrados:")
                                for prod in entrada.productos_utilizados:
                                    st.markdown(f"- {prod.nombre} ({prod.categoria})")
                            
                            st.divider()
                            # (Aquí irían los botones de Editar/Borrar igual que antes...)
                            if st.button("🗑️ Borrar", key=f"del_{entrada.id}"):
                                medical_service.eliminar_consulta(entrada.id)
                                st.rerun()
                else:
                    st.info("Sin historial.")
            
            # --- PESTAÑA NUEVA CONSULTA (CON STOCK) ---
            with tab_nuevo:
                st.subheader(f"Nueva entrada para {mascota_obj.nombre}")
                
                with st.form("form_historial", clear_on_submit=True):
                    diagnostico = st.text_input("Diagnóstico Breve")
                    descripcion = st.text_area("Descripción detallada")
                    
                    st.markdown("---")
                    st.write("📦 **Material Utilizado (Se descontará del stock):**")
                    
                    # 1. Obtenemos todos los productos disponibles
                    todos_productos = inventory_service.obtener_todos()
                    # Creamos un diccionario para el multiselect
                    mapa_prod = {f"{p.nombre} (Stock: {p.stock})": p.id for p in todos_productos}
                    
                    # 2. Selector Múltiple
                    seleccionados = st.multiselect("Seleccionar productos:", list(mapa_prod.keys()))
                    
                    # 3. Convertimos los nombres seleccionados a IDs
                    ids_seleccionados = [mapa_prod[nombre] for nombre in seleccionados]
                    
                    guardar = st.form_submit_button("Guardar y Descontar Stock")
                    
                    if guardar:
                        if diagnostico and descripcion:
                            usuario_actual = st.session_state['usuario']
                            medical_service.registrar_consulta(
                                id_mascota=mascota_obj.id,
                                id_veterinario=usuario_actual.id,
                                diagnostico=diagnostico,
                                descripcion=descripcion,
                                lista_ids_productos=ids_seleccionados # Pasamos la lista
                            )
                            st.success("✅ Historial guardado y stock actualizado.")
                        else:
                            st.error("Faltan datos.")
        else:
            st.warning("Cliente no encontrado.")