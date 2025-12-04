from datetime import date
from app.repositories.historial_repository import HistorialRepository
from app.repositories.cliente_repository import ClienteRepository
from app.models.historial import HistorialMedico

class MedicalService:
    def __init__(self, historial_repo: HistorialRepository, cliente_repo: ClienteRepository):
        self.historial_repo = historial_repo
        self.cliente_repo = cliente_repo

    def buscar_cliente_por_dni(self, dni):
        # Reutilizamos la lógica de buscar cliente para encontrar a la mascota
        return self.cliente_repo.buscar_por_dni(dni)

    def obtener_historial_mascota(self, id_mascota):
        return self.historial_repo.buscar_por_mascota(id_mascota)

    def registrar_consulta(self, id_mascota, id_veterinario, diagnostico, descripcion):
        nueva_consulta = HistorialMedico(
            fecha=date.today(), # La fecha es automática al momento del registro
            id_mascota=id_mascota,
            id_veterinario=id_veterinario,
            diagnostico=diagnostico,
            descripcion=descripcion
        )
        return self.historial_repo.guardar(nueva_consulta)