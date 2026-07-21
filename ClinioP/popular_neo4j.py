from database import pacientes_collection, consultas_collection, diagnosticos_collection
from neo4j_config import neo4j_driver


from database import pacientes_collection, consultas_collection, diagnosticos_collection
from neo4j_config import neo4j_driver


def limpar_banco_neo4j():
    with neo4j_driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        print("Banco Neo4j limpo com sucesso.")


def criar_grafo_clinio():
    pacientes = list(pacientes_collection.find())

    with neo4j_driver.session() as session:
        for paciente in pacientes:
            paciente_id = str(paciente["_id"])

            session.run(
                """
                MERGE (p:Paciente {id: $id})
                SET p.nome = $nome,
                    p.cpf = $cpf,
                    p.sexo = $sexo,
                    p.data_nascimento = $data_nascimento
                """,
                id=paciente_id,
                nome=paciente.get("nome", ""),
                cpf=paciente.get("cpf", ""),
                sexo=paciente.get("sexo", ""),
                data_nascimento=paciente.get("data_nascimento", "")
            )

            consultas = list(
                consultas_collection.find(
                    {"paciente_id": paciente["_id"]}
                )
            )

            for consulta in consultas:
                consulta_id = str(consulta["_id"])

                session.run(
                    """
                    MATCH (p:Paciente {id: $paciente_id})
                    MERGE (c:Consulta {id: $consulta_id})
                    SET c.data = $data,
                        c.horario = $horario,
                        c.status = $status,
                        c.valor = $valor
                    MERGE (p)-[:REALIZOU]->(c)
                    """,
                    paciente_id=paciente_id,
                    consulta_id=consulta_id,
                    data=consulta.get("data", ""),
                    horario=consulta.get("horario", ""),
                    status=consulta.get("status", ""),
                    valor=consulta.get("valor", 0)
                )

                medico = consulta.get("medico", "")
                especialidade = consulta.get("especialidade", "")

                if medico:
                    session.run(
                        """
                        MATCH (c:Consulta {id: $consulta_id})
                        MERGE (m:Medico {nome: $medico})
                        MERGE (m)-[:ATENDEU]->(c)
                        """,
                        consulta_id=consulta_id,
                        medico=medico
                    )

                if especialidade:
                    session.run(
                        """
                        MATCH (c:Consulta {id: $consulta_id})
                        MERGE (e:Especialidade {nome: $especialidade})
                        MERGE (c)-[:DA_ESPECIALIDADE]->(e)
                        """,
                        consulta_id=consulta_id,
                        especialidade=especialidade
                    )

                diagnostico = diagnosticos_collection.find_one(
                    {"consulta_id": consulta["_id"]}
                )

                if diagnostico:
                    texto_diagnostico = diagnostico.get("diagnostico", "")
                    sintomas_texto = diagnostico.get("sintomas", "")
                    tratamento = diagnostico.get("tratamento", "")

                    if texto_diagnostico:
                        session.run(
                            """
                            MATCH (p:Paciente {id: $paciente_id})
                            MATCH (c:Consulta {id: $consulta_id})
                            MERGE (d:Diagnostico {descricao: $diagnostico})
                            MERGE (c)-[:GEROU]->(d)
                            MERGE (p)-[:TEVE_DIAGNOSTICO]->(d)
                            """,
                            paciente_id=paciente_id,
                            consulta_id=consulta_id,
                            diagnostico=texto_diagnostico
                        )

                    if sintomas_texto:
                        sintomas = [
                            s.strip().lower()
                            for s in sintomas_texto.replace(";", ",").split(",")
                            if s.strip()
                        ]

                        for sintoma in sintomas:
                            session.run(
                                """
                                MATCH (p:Paciente {id: $paciente_id})
                                MATCH (c:Consulta {id: $consulta_id})
                                MERGE (s:Sintoma {descricao: $sintoma})
                                MERGE (c)-[:APRESENTOU]->(s)
                                MERGE (p)-[:RELATOU]->(s)
                                """,
                                paciente_id=paciente_id,
                                consulta_id=consulta_id,
                                sintoma=sintoma
                            )

                    if tratamento:
                        session.run(
                            """
                            MATCH (c:Consulta {id: $consulta_id})
                            MERGE (t:Tratamento {descricao: $tratamento})
                            MERGE (c)-[:INDICOU]->(t)
                            """,
                            consulta_id=consulta_id,
                            tratamento=tratamento
                        )

    print("Grafo CLINIO criado com sucesso no Neo4j.")


if __name__ == "__main__":
    limpar_banco_neo4j()
    criar_grafo_clinio()