from database import pacientes_collection, consultas_collection, diagnosticos_collection


def limpar_mongodb():
    pacientes_collection.delete_many({})
    consultas_collection.delete_many({})
    diagnosticos_collection.delete_many({})

    print("Coleções do MongoDB limpas com sucesso.")


def popular_mongodb():
    pacientes = [
        {
            "nome": "João Pereira",
            "cpf": "11111111111",
            "data_nascimento": "1980-05-10",
            "sexo": "Masculino",
            "telefone": "(34) 99999-1111",
            "email": "joao@email.com",
            "endereco": "Rua A, Uberlândia - MG"
        },
        {
            "nome": "Maria Souza",
            "cpf": "22222222222",
            "data_nascimento": "1975-08-22",
            "sexo": "Feminino",
            "telefone": "(34) 99999-2222",
            "email": "maria@email.com",
            "endereco": "Rua B, Uberlândia - MG"
        },
        {
            "nome": "Carlos Almeida",
            "cpf": "33333333333",
            "data_nascimento": "1968-03-15",
            "sexo": "Masculino",
            "telefone": "(34) 99999-3333",
            "email": "carlos@email.com",
            "endereco": "Rua C, Uberlândia - MG"
        },
        {
            "nome": "Ana Ribeiro",
            "cpf": "44444444444",
            "data_nascimento": "1990-11-30",
            "sexo": "Feminino",
            "telefone": "(34) 99999-4444",
            "email": "ana@email.com",
            "endereco": "Rua D, Uberlândia - MG"
        },
        {
            "nome": "Roberta Damião",
            "cpf": "55555555555",
            "data_nascimento": "2001-07-12",
            "sexo": "Feminino",
            "telefone": "(34) 99999-5555",
            "email": "roberta@email.com",
            "endereco": "Rua E, Uberlândia - MG"
        },
        {
            "nome": "Pedro Martins",
            "cpf": "66666666666",
            "data_nascimento": "1958-01-20",
            "sexo": "Masculino",
            "telefone": "(34) 99999-6666",
            "email": "pedro@email.com",
            "endereco": "Rua F, Uberlândia - MG"
        },
        {
            "nome": "Fernanda Costa",
            "cpf": "77777777777",
            "data_nascimento": "1988-09-05",
            "sexo": "Feminino",
            "telefone": "(34) 99999-7777",
            "email": "fernanda@email.com",
            "endereco": "Rua G, Uberlândia - MG"
        },
        {
            "nome": "Lucas Oliveira",
            "cpf": "88888888888",
            "data_nascimento": "1995-12-18",
            "sexo": "Masculino",
            "telefone": "(34) 99999-8888",
            "email": "lucas@email.com",
            "endereco": "Rua H, Uberlândia - MG"
        }
    ]

    resultado_pacientes = pacientes_collection.insert_many(pacientes)
    ids = resultado_pacientes.inserted_ids

    consultas = [
        {
            "paciente_id": ids[0],
            "data": "2026-07-01",
            "horario": "08:30:00",
            "especialidade": "Clínico Geral",
            "medico": "Dr. André",
            "status": "Realizada",
            "valor": 180.0
        },
        {
            "paciente_id": ids[1],
            "data": "2026-07-02",
            "horario": "09:00:00",
            "especialidade": "Clínico Geral",
            "medico": "Dr. André",
            "status": "Realizada",
            "valor": 180.0
        },
        {
            "paciente_id": ids[2],
            "data": "2026-07-03",
            "horario": "10:00:00",
            "especialidade": "Cardiologia",
            "medico": "Dra. Beatriz",
            "status": "Realizada",
            "valor": 250.0
        },
        {
            "paciente_id": ids[3],
            "data": "2026-07-04",
            "horario": "11:30:00",
            "especialidade": "Cardiologia",
            "medico": "Dra. Beatriz",
            "status": "Realizada",
            "valor": 250.0
        },
        {
            "paciente_id": ids[4],
            "data": "2026-07-05",
            "horario": "13:30:00",
            "especialidade": "Dermatologia",
            "medico": "Dra. Camila",
            "status": "Realizada",
            "valor": 220.0
        },
        {
            "paciente_id": ids[5],
            "data": "2026-07-06",
            "horario": "14:00:00",
            "especialidade": "Clínico Geral",
            "medico": "Dr. André",
            "status": "Realizada",
            "valor": 180.0
        },
        {
            "paciente_id": ids[6],
            "data": "2026-07-07",
            "horario": "15:00:00",
            "especialidade": "Ortopedia",
            "medico": "Dr. Marcelo",
            "status": "Realizada",
            "valor": 230.0
        },
        {
            "paciente_id": ids[7],
            "data": "2026-07-08",
            "horario": "16:00:00",
            "especialidade": "Ortopedia",
            "medico": "Dr. Marcelo",
            "status": "Realizada",
            "valor": 230.0
        },
        {
            "paciente_id": ids[0],
            "data": "2026-07-10",
            "horario": "08:00:00",
            "especialidade": "Cardiologia",
            "medico": "Dra. Beatriz",
            "status": "Agendada",
            "valor": 250.0
        },
        {
            "paciente_id": ids[1],
            "data": "2026-07-11",
            "horario": "09:30:00",
            "especialidade": "Clínico Geral",
            "medico": "Dr. André",
            "status": "Agendada",
            "valor": 180.0
        },
        {
            "paciente_id": ids[2],
            "data": "2026-07-12",
            "horario": "10:30:00",
            "especialidade": "Cardiologia",
            "medico": "Dra. Beatriz",
            "status": "Agendada",
            "valor": 250.0
        },
        {
            "paciente_id": ids[4],
            "data": "2026-07-13",
            "horario": "14:30:00",
            "especialidade": "Dermatologia",
            "medico": "Dra. Camila",
            "status": "Cancelada",
            "valor": 220.0
        }
    ]

    resultado_consultas = consultas_collection.insert_many(consultas)
    consulta_ids = resultado_consultas.inserted_ids

    diagnosticos = [
        {
            "consulta_id": consulta_ids[0],
            "sintomas": "febre, dor de cabeça, tosse",
            "diagnostico": "síndrome gripal",
            "tratamento": "hidratação, repouso e antitérmico",
            "observacoes": "Retornar se houver piora."
        },
        {
            "consulta_id": consulta_ids[1],
            "sintomas": "febre, dor no corpo, tosse",
            "diagnostico": "síndrome gripal",
            "tratamento": "repouso e medicação sintomática",
            "observacoes": "Paciente orientada sobre sinais de alerta."
        },
        {
            "consulta_id": consulta_ids[2],
            "sintomas": "dor no peito, falta de ar, cansaço",
            "diagnostico": "hipertensão arterial",
            "tratamento": "controle de pressão e avaliação cardiológica",
            "observacoes": "Solicitado acompanhamento."
        },
        {
            "consulta_id": consulta_ids[3],
            "sintomas": "falta de ar, palpitação, cansaço",
            "diagnostico": "arritmia leve",
            "tratamento": "exames complementares e acompanhamento",
            "observacoes": "Solicitado eletrocardiograma."
        },
        {
            "consulta_id": consulta_ids[4],
            "sintomas": "manchas na pele, coceira, vermelhidão",
            "diagnostico": "dermatite alérgica",
            "tratamento": "pomada antialérgica e evitar agente irritante",
            "observacoes": "Reavaliar em 15 dias."
        },
        {
            "consulta_id": consulta_ids[5],
            "sintomas": "febre, dor de cabeça, dor no corpo",
            "diagnostico": "virose",
            "tratamento": "hidratação e repouso",
            "observacoes": "Quadro leve."
        },
        {
            "consulta_id": consulta_ids[6],
            "sintomas": "dor lombar, dificuldade para caminhar, rigidez",
            "diagnostico": "lombalgia",
            "tratamento": "anti-inflamatório e fisioterapia",
            "observacoes": "Evitar esforço físico."
        },
        {
            "consulta_id": consulta_ids[7],
            "sintomas": "dor lombar, rigidez, dor na perna",
            "diagnostico": "lombalgia",
            "tratamento": "fisioterapia e alongamentos",
            "observacoes": "Acompanhar evolução."
        },
        {
            "consulta_id": consulta_ids[8],
            "sintomas": "cansaço, falta de ar, pressão alta",
            "diagnostico": "hipertensão arterial",
            "tratamento": "ajuste medicamentoso e dieta com pouco sal",
            "observacoes": "Monitorar pressão diariamente."
        },
        {
            "consulta_id": consulta_ids[9],
            "sintomas": "tosse, febre, dor de garganta",
            "diagnostico": "infecção respiratória",
            "tratamento": "medicação sintomática e hidratação",
            "observacoes": "Retorno em caso de piora."
        },
        {
            "consulta_id": consulta_ids[10],
            "sintomas": "dor no peito, cansaço, pressão alta",
            "diagnostico": "hipertensão arterial",
            "tratamento": "controle pressórico e exames laboratoriais",
            "observacoes": "Paciente com risco cardiovascular."
        },
        {
            "consulta_id": consulta_ids[11],
            "sintomas": "coceira, vermelhidão, descamação",
            "diagnostico": "dermatite alérgica",
            "tratamento": "creme hidratante e antialérgico",
            "observacoes": "Evitar produtos irritantes."
        }
    ]

    diagnosticos_collection.insert_many(diagnosticos)

    print("MongoDB populado com sucesso.")
    print(f"Pacientes inseridos: {len(pacientes)}")
    print(f"Consultas inseridas: {len(consultas)}")
    print(f"Diagnósticos inseridos: {len(diagnosticos)}")


if __name__ == "__main__":
    limpar_mongodb()
    popular_mongodb()