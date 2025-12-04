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
        vets = self.vet_repo.buscar_todos()
        # Devuelve una lista de tuplas o diccionarios útiles
        return vets

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