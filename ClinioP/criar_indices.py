from database import pacientes_collection, consultas_collection, diagnosticos_collection

consultas_collection.create_index("paciente_id")
diagnosticos_collection.create_index("consulta_id")

print("Índices criados com sucesso!")
print("Índice 1: consultas.paciente_id")
print("Índice 2: diagnosticos.consulta_id")