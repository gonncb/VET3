import streamlit as st
import pandas as pd
import plotly.express as px # <--- NUEVA LIBRERÍA PRO PARA GRÁFICOS
from app.database import SessionLocal

# Repositorios
from app.repositories.veterinario_repository import VeterinarioRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.cita_repository import CitaRepository
from app.repositories.historial_repository import HistorialRepository
from app.repositories.producto_repository import ProductoRepository # <--- NUEVO

# Servicios
from app.services.auth_service import AuthService
from app.services.clinic_service import ClinicService
from app.services.cita_service import CitaService
from app.services.medical_service import MedicalService
from app.services.inventory_service import InventoryService # <--- NUEVO

# Vistas
from app.ui.login import mostrar_login
from app.ui.gestion_clientes import mostrar_gestion_clientes
from app.ui.gestion_citas import mostrar_gestion_citas
from app.ui.gestion_historiales import mostrar_gestion_historiales
from app.ui.gestion_inventario import mostrar_gestion_inventario # <--- NUEVO

st.set_page_config(page_title="VetManager ERP", page_icon="🏥", layout="wide")

class ServiceContainer:
    def __init__(self):
        self.db = SessionLocal()
        
        # Repos
        self.vet_repo = VeterinarioRepository(self.db)
        self.client_repo = ClienteRepository(self.db)
        self.cita_repo = CitaRepository(self.db)
        self.hist_repo = HistorialRepository(self.db)
        self.prod_repo = ProductoRepository(self.db) # <--- NUEVO
        
        # Services
        self.auth_service = AuthService(self.vet_repo)
        self.clinic_service = ClinicService(self.client_repo)
        self.cita_service = CitaService(self.cita_repo, self.vet_repo, self.client_repo)
        
        # Inyectamos el inventario en el servicio médico (para descontar stock)
        self.inventory_service = InventoryService(self.prod_repo) # <--- NUEVO
        self.medical_service = MedicalService(self.hist_repo, self.client_repo, self.prod_repo) # <--- ACTUALIZADO

def main():
    services = ServiceContainer()

    if 'usuario' not in st.session_state:
        mostrar_login(services.auth_service)
    else:
        usuario = st.session_state['usuario']
        
        with st.sidebar:
            st.title("🏥 VetManager ERP")
            st.write(f"Hola, **{usuario.nombre}**")
            st.divider()
            
            menu = st.radio("Navegación", [
                "📊 Dashboard", 
                "👥 Clientes", 
                "📅 Agenda", 
                "📋 Historial", 
                "📦 Inventario" # <--- NUEVO MENU
            ])
            
            st.divider()
            if st.button("Cerrar Sesión"):
                del st.session_state['usuario']
                st.rerun()

        if menu == "📊 Dashboard":
            st.title("Cuadro de Mando Integral")
            
            # Datos
            stats_citas = services.cita_service.obtener_estadisticas_dashboard()
            stats_especies = services.clinic_service.obtener_estadisticas_especies() # Para el gráfico circular
            
            # KPIs
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Citas Hoy", stats_citas["citas_hoy"])
            k2.metric("Total Citas", stats_citas["total_citas"])
            k3.metric("Pacientes", sum(stats_especies.values()))
            
            # Stock bajo (Alerta)
            productos = services.inventory_service.obtener_todos()
            bajo_stock = sum(1 for p in productos if p.stock < 10)
            k4.metric("⚠️ Alertas Stock", bajo_stock, delta_color="inverse")
            
            st.divider()
            
            # GRÁFICOS
            g1, g2 = st.columns(2)
            
            with g1:
                st.subheader("Carga de Trabajo (Citas/Vet)")
                if stats_citas["citas_por_vet"]:
                    df_vets = pd.DataFrame.from_dict(stats_citas["citas_por_vet"], orient='index', columns=['Citas'])
                    st.bar_chart(df_vets)
            
            with g2:
                st.subheader("Distribución de Pacientes")
                if stats_especies:
                    # Crear DataFrame para Plotly
                    df_pets = pd.DataFrame(list(stats_especies.items()), columns=['Especie', 'Cantidad'])
                    # Gráfico de Donut chulo
                    fig = px.pie(df_pets, values='Cantidad', names='Especie', hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)

        elif menu == "👥 Clientes":
            mostrar_gestion_clientes(services.clinic_service)
        elif menu == "📅 Agenda":
            mostrar_gestion_citas(services.cita_service)
        elif menu == "📋 Historial":
            # Pasamos ambos servicios: Médico (para guardar) e Inventario (para leer productos)
            mostrar_gestion_historiales(services.medical_service, services.inventory_service)
        elif menu == "📦 Inventario":
            mostrar_gestion_inventario(services.inventory_service)

if __name__ == "__main__":
    main()