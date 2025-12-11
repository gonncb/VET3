import streamlit as st
import pandas as pd
from app.services.inventory_service import InventoryService

def mostrar_gestion_inventario(service: InventoryService):
    st.header("📦 Gestión de Inventario y Farmacia")
    
    tab_listado, tab_nuevo = st.tabs(["📊 Stock Actual", "➕ Alta Producto"])
    
    # --- PESTAÑA 1: STOCK Y REPOSICIÓN ---
    with tab_listado:
        productos = service.obtener_todos()
        if productos:
            # Mostramos métricas rápidas
            total_items = len(productos)
            bajo_stock = sum(1 for p in productos if p.stock < 10)
            
            c1, c2 = st.columns(2)
            c1.metric("Referencias Totales", total_items)
            c2.metric("⚠️ Bajo Stock (<10)", bajo_stock, delta_color="inverse")
            
            st.divider()

            for p in productos:
                # Usamos colores para alertar del stock
                color_stock = "red" if p.stock == 0 else "orange" if p.stock < 10 else "green"
                
                with st.expander(f"💊 {p.nombre} | Stock: :{color_stock}[{p.stock} u.]"):
                    c_info, c_action = st.columns([2, 1])
                    
                    with c_info:
                        st.write(f"**Categoría:** {p.categoria}")
                        st.write(f"**Precio:** {p.precio}€")
                    
                    with c_action:
                        st.write("**Reponer Stock:**")
                        with st.form(f"form_stock_{p.id}"):
                            cantidad = st.number_input("Cantidad", min_value=1, value=10, key=f"qty_{p.id}")
                            if st.form_submit_button("➕ Añadir"):
                                service.actualizar_stock(p.id, cantidad, "sumar")
                                st.success("Stock actualizado")
                                st.rerun()
                        
                        if st.button("🗑️ Eliminar Ref.", key=f"del_prod_{p.id}"):
                            service.eliminar_producto(p.id)
                            st.rerun()
        else:
            st.info("El inventario está vacío.")

    # --- PESTAÑA 2: NUEVO PRODUCTO ---
    with tab_nuevo:
        st.subheader("Registrar Nuevo Producto")
        with st.form("form_nuevo_prod", clear_on_submit=True):
            col1, col2 = st.columns(2)
            nombre = col1.text_input("Nombre Comercial")
            categoria = col2.selectbox("Categoría", ["Vacuna", "Medicamento Oral", "Inyectable", "Cirugía", "Alimentación", "Accesorio"])
            precio = col1.number_input("Precio (€)", min_value=0.0, step=0.5)
            stock = col2.number_input("Stock Inicial", min_value=0, value=0)
            
            if st.form_submit_button("Guardar Producto"):
                if nombre and precio >= 0:
                    service.crear_producto(nombre, categoria, precio, stock)
                    st.success(f"✅ {nombre} añadido al inventario.")
                else:
                    st.error("Revisa los datos del formulario.")