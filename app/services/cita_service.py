from datetime import date
from collections import Counter
from app.repositories.cita_repository import CitaRepository
from app.repositories.veterinario_repository import VeterinarioRepository
from app.repositories.cliente_repository import ClienteRepository
from app.models.cita import Cita

class CitaService:
    def __init__(self, cita_repo: CitaRepository, vet_repo: VeterinarioRepository, cliente_repo: ClienteRepository):
        self.cita_repo = cita_repo
        self.vet_repo = vet_repo
        self.cliente_repo = cliente_repo

    def obtener_veterinarios_formateados(self):
        """Devuelve lista de veterinarios para usar en un selectbox"""
        return self.vet_repo.buscar_todos()

    def buscar_cliente_por_dni(self, dni):
        return self.cliente_repo.buscar_por_dni(dni)

    def crear_cita(self, fecha, hora, motivo, id_mascota, id_veterinario):
        nueva_cita = Cita(
            fecha=fecha,
            hora=hora,
            motivo=motivo,
            id_mascota=id_mascota,
            id_veterinario=id_veterinario
        )
        return self.cita_repo.guardar(nueva_cita)
        
    def obtener_historial_citas(self):
        return self.cita_repo.buscar_todas()
    
    def cancelar_cita(self, id_cita):
        return self.cita_repo.eliminar_por_id(id_cita)

    # --- MÉTODO PARA EL DASHBOARD ---
    def obtener_estadisticas_dashboard(self):
        """
        Calcula métricas clave para el panel de control.
        Devuelve un diccionario con totales y agrupaciones.
        """
        todas_citas = self.cita_repo.buscar_todas()
        
        # 1. Citas de Hoy (Comparando fechas)
        hoy = date.today()
        citas_hoy = sum(1 for c in todas_citas if c.fecha == hoy)
        
        # 2. Citas por Veterinario (Para el gráfico)
        # Extraemos solo los nombres de los doctores asignados
        vets = [c.veterinario.nombre for c in todas_citas if c.veterinario]
        conteo_vets = Counter(vets) 
        
        return {
            "total_citas": len(todas_citas),
            "citas_hoy": citas_hoy,
            "citas_por_vet": conteo_vets
        }