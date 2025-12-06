from datetime import date
from app.repositories.historial_repository import HistorialRepository
from app.repositories.cliente_repository import ClienteRepository
from app.models.historial import HistorialMedico

class MedicalService:
    def __init__(self, historial_repo: HistorialRepository, cliente_repo: ClienteRepository):
        self.historial_repo = historial_repo
        self.cliente_repo = cliente_repo

    def buscar_cliente_por_dni(self, dni):
        return self.cliente_repo.buscar_por_dni(dni)

    def obtener_historial_mascota(self, id_mascota):
        return self.historial_repo.buscar_por_mascota(id_mascota)

    def registrar_consulta(self, id_mascota, id_veterinario, diagnostico, descripcion):
        nueva_consulta = HistorialMedico(
            fecha=date.today(),
            id_mascota=id_mascota,
            id_veterinario=id_veterinario,
            diagnostico=diagnostico,
            descripcion=descripcion
        )
        return self.historial_repo.guardar(nueva_consulta)

    # --- NUEVOS MÉTODOS ---
    def eliminar_consulta(self, id_historial):
        consulta = self.historial_repo.buscar_por_id(id_historial)
        if consulta:
            self.historial_repo.eliminar(consulta)
            return True
        return False

    def actualizar_consulta(self, id_historial, nuevo_diagnostico, nueva_descripcion):
        consulta = self.historial_repo.buscar_por_id(id_historial)
        if consulta:
            consulta.diagnostico = nuevo_diagnostico
            consulta.descripcion = nueva_descripcion
            self.historial_repo.actualizar()
            return True
        return False