import streamlit as st
import pandas as pd
from datetime import date
from bson.objectid import ObjectId
from database import pacientes_collection, consultas_collection, diagnosticos_collection

st.set_page_config(
    page_title="CLINIO",
    page_icon="🩺",
    layout="wide"
)

st.title("CLINIO - Sistema de Apoio Clínico")

st.sidebar.title("Menu")
pagina = st.sidebar.radio(
    "Escolha uma opção:",
    ["Dashboard", "Pacientes", "Consultas", "Diagnósticos"]
)


def montar_opcoes_pacientes():
    pacientes = list(pacientes_collection.find())
    return {
        f"{paciente['nome']} - CPF: {paciente['cpf']}": str(paciente["_id"])
        for paciente in pacientes
    }


def montar_opcoes_consultas():
    consultas = list(consultas_collection.find())
    opcoes = {}

    for consulta in consultas:
        paciente = pacientes_collection.find_one({"_id": consulta["paciente_id"]})
        nome_paciente = paciente["nome"] if paciente else "Paciente não encontrado"

        texto_opcao = (
            f"{nome_paciente} - {consulta['especialidade']} - "
            f"{consulta['data']} às {consulta['horario']}"
        )

        opcoes[texto_opcao] = str(consulta["_id"])

    return opcoes


if pagina == "Dashboard":
    st.header("Dashboard - Briefing Clínico e Aggregation Pipelines")

    aba_briefing, aba_pipeline_1, aba_pipeline_2, aba_sample = st.tabs(
        ["Briefing Clínico", "Pipeline 1", "Pipeline 2", "Sample"]
    )

    with aba_briefing:
        pacientes = list(pacientes_collection.find())

        if len(pacientes) == 0:
            st.info("Cadastre pacientes para visualizar o briefing clínico.")
        else:
            opcoes_pacientes = montar_opcoes_pacientes()

            paciente_escolhido = st.selectbox(
                "Escolha um paciente",
                list(opcoes_pacientes.keys())
            )

            paciente_id = opcoes_pacientes[paciente_escolhido]
            paciente = pacientes_collection.find_one({"_id": ObjectId(paciente_id)})

            st.subheader("Dados do paciente")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"**Nome:** {paciente['nome']}")
                st.write(f"**CPF:** {paciente['cpf']}")

            with col2:
                st.write(f"**Nascimento:** {paciente['data_nascimento']}")
                st.write(f"**Sexo:** {paciente['sexo']}")

            with col3:
                st.write(f"**Telefone:** {paciente['telefone']}")
                st.write(f"**E-mail:** {paciente['email']}")

            st.write(f"**Endereço:** {paciente['endereco']}")

            st.subheader("Histórico clínico")

            consultas = list(
                consultas_collection.find(
                    {"paciente_id": ObjectId(paciente_id)}
                ).sort("data", -1)
            )

            if len(consultas) == 0:
                st.info("Este paciente ainda não possui consultas cadastradas.")
            else:
                for consulta in consultas:
                    with st.expander(
                        f"{consulta['data']} - {consulta['especialidade']} - {consulta['medico']}"
                    ):
                        st.write(f"**Horário:** {consulta['horario']}")
                        st.write(f"**Status:** {consulta['status']}")
                        st.write(f"**Valor:** R$ {consulta['valor']:.2f}")

                        diagnostico = diagnosticos_collection.find_one(
                            {"consulta_id": consulta["_id"]}
                        )

                        if diagnostico:
                            st.write("**Sintomas:**")
                            st.write(diagnostico["sintomas"])

                            st.write("**Diagnóstico:**")
                            st.write(diagnostico["diagnostico"])

                            st.write("**Tratamento:**")
                            st.write(diagnostico["tratamento"])

                            st.write("**Observações:**")
                            st.write(diagnostico["observacoes"])
                        else:
                            st.warning("Esta consulta ainda não possui diagnóstico.")

    with aba_pipeline_1:
        st.subheader("Pipeline 1 - Consultas com paciente e diagnóstico")

        pipeline_1 = [
            {
                "$lookup": {
                    "from": "pacientes",
                    "localField": "paciente_id",
                    "foreignField": "_id",
                    "as": "paciente"
                }
            },
            {"$unwind": "$paciente"},
            {
                "$lookup": {
                    "from": "diagnosticos",
                    "localField": "_id",
                    "foreignField": "consulta_id",
                    "as": "diagnostico"
                }
            },
            {
                "$unwind": {
                    "path": "$diagnostico",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$set": {
                    "nome_paciente": "$paciente.nome",
                    "texto_diagnostico": "$diagnostico.diagnostico"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "Paciente": "$nome_paciente",
                    "Especialidade": "$especialidade",
                    "Data": "$data",
                    "Horário": "$horario",
                    "Médico": "$medico",
                    "Status": "$status",
                    "Diagnóstico": "$texto_diagnostico"
                }
            },
            {"$sort": {"Data": -1}}
        ]

        resultado_1 = list(consultas_collection.aggregate(pipeline_1))

        st.write("Código da Aggregation Pipeline:")
        st.code(str(pipeline_1), language="python")

        if len(resultado_1) == 0:
            st.info("Nenhum resultado encontrado.")
        else:
            st.dataframe(pd.DataFrame(resultado_1), use_container_width=True)

    with aba_pipeline_2:
        st.subheader("Pipeline 2 - Estatísticas por especialidade com $merge")

        pipeline_2 = [
            {
                "$match": {
                    "status": {
                        "$in": ["Agendada", "Realizada", "Cancelada"]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$especialidade",
                    "quantidade_consultas": {"$sum": 1},
                    "valor_total": {"$sum": "$valor"},
                    "valor_medio": {"$avg": "$valor"}
                }
            },
            {"$sort": {"quantidade_consultas": -1}},
            {
                "$project": {
                    "_id": 0,
                    "especialidade": "$_id",
                    "quantidade_consultas": 1,
                    "valor_total": 1,
                    "valor_medio": 1
                }
            },
            {
                "$merge": {
                    "into": "estatisticas_especialidades",
                    "whenMatched": "replace",
                    "whenNotMatched": "insert"
                }
            }
        ]

        st.write("Código da Aggregation Pipeline:")
        st.code(str(pipeline_2), language="python")

        list(consultas_collection.aggregate(pipeline_2))

        estatisticas_collection = consultas_collection.database["estatisticas_especialidades"]
        resultado_2 = list(estatisticas_collection.find({}, {"_id": 0}))

        st.success("Pipeline executada e resultado salvo na coleção estatisticas_especialidades.")

        if len(resultado_2) == 0:
            st.info("Nenhum resultado encontrado.")
        else:
            st.dataframe(pd.DataFrame(resultado_2), use_container_width=True)

    with aba_sample:
        st.subheader("Pipeline Extra - Amostra aleatória com $sample")

        pipeline_sample = [
            {"$sample": {"size": 2}},
            {
                "$lookup": {
                    "from": "pacientes",
                    "localField": "paciente_id",
                    "foreignField": "_id",
                    "as": "paciente"
                }
            },
            {"$unwind": "$paciente"},
            {
                "$project": {
                    "_id": 0,
                    "Paciente": "$paciente.nome",
                    "Especialidade": "$especialidade",
                    "Data": "$data",
                    "Médico": "$medico",
                    "Status": "$status"
                }
            }
        ]

        resultado_sample = list(consultas_collection.aggregate(pipeline_sample))

        st.write("Código da Aggregation Pipeline:")
        st.code(str(pipeline_sample), language="python")

        if len(resultado_sample) == 0:
            st.info("Nenhum resultado encontrado.")
        else:
            st.dataframe(pd.DataFrame(resultado_sample), use_container_width=True)


elif pagina == "Pacientes":
    st.header("Pacientes")

    aba_cadastrar, aba_listar, aba_editar, aba_excluir = st.tabs(
        ["Cadastrar", "Listar", "Editar", "Excluir"]
    )

    with aba_cadastrar:
        st.subheader("Cadastrar paciente")

        with st.form("form_cadastro_paciente"):
            nome = st.text_input("Nome completo")
            cpf = st.text_input("CPF")
            data_nascimento = st.date_input(
                "Data de nascimento",
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                value=date(1990, 1, 1)
            )
            sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
            telefone = st.text_input("Telefone")
            email = st.text_input("E-mail")
            endereco = st.text_area("Endereço")

            botao_salvar = st.form_submit_button("Salvar paciente")

            if botao_salvar:
                if nome == "" or cpf == "":
                    st.error("Nome e CPF são obrigatórios.")
                else:
                    paciente = {
                        "nome": nome,
                        "cpf": cpf,
                        "data_nascimento": str(data_nascimento),
                        "sexo": sexo,
                        "telefone": telefone,
                        "email": email,
                        "endereco": endereco
                    }

                    pacientes_collection.insert_one(paciente)
                    st.success("Paciente cadastrado com sucesso!")

    with aba_listar:
        st.subheader("Pacientes cadastrados")

        pacientes = list(pacientes_collection.find())

        if len(pacientes) == 0:
            st.info("Nenhum paciente cadastrado ainda.")
        else:
            for paciente in pacientes:
                paciente["_id"] = str(paciente["_id"])

            st.dataframe(pd.DataFrame(pacientes), use_container_width=True)

    with aba_editar:
        st.subheader("Editar paciente")

        pacientes = list(pacientes_collection.find())

        if len(pacientes) == 0:
            st.info("Nenhum paciente cadastrado para editar.")
        else:
            opcoes_pacientes = montar_opcoes_pacientes()

            paciente_escolhido = st.selectbox(
                "Escolha o paciente que deseja editar",
                list(opcoes_pacientes.keys())
            )

            paciente_id = opcoes_pacientes[paciente_escolhido]
            paciente = pacientes_collection.find_one({"_id": ObjectId(paciente_id)})

            with st.form("form_editar_paciente"):
                novo_nome = st.text_input("Nome completo", value=paciente["nome"])
                novo_cpf = st.text_input("CPF", value=paciente["cpf"])
                nova_data_nascimento = st.text_input(
                    "Data de nascimento",
                    value=paciente["data_nascimento"]
                )
                novo_sexo = st.selectbox(
                    "Sexo",
                    ["Masculino", "Feminino", "Outro"],
                    index=["Masculino", "Feminino", "Outro"].index(paciente["sexo"])
                )
                novo_telefone = st.text_input("Telefone", value=paciente["telefone"])
                novo_email = st.text_input("E-mail", value=paciente["email"])
                novo_endereco = st.text_area("Endereço", value=paciente["endereco"])

                botao_atualizar = st.form_submit_button("Atualizar paciente")

                if botao_atualizar:
                    pacientes_collection.update_one(
                        {"_id": ObjectId(paciente_id)},
                        {
                            "$set": {
                                "nome": novo_nome,
                                "cpf": novo_cpf,
                                "data_nascimento": nova_data_nascimento,
                                "sexo": novo_sexo,
                                "telefone": novo_telefone,
                                "email": novo_email,
                                "endereco": novo_endereco
                            }
                        }
                    )

                    st.success("Paciente atualizado com sucesso!")

    with aba_excluir:
        st.subheader("Excluir paciente")

        pacientes = list(pacientes_collection.find())

        if len(pacientes) == 0:
            st.info("Nenhum paciente cadastrado para excluir.")
        else:
            opcoes_pacientes = montar_opcoes_pacientes()

            paciente_escolhido = st.selectbox(
                "Escolha o paciente que deseja excluir",
                list(opcoes_pacientes.keys())
            )

            paciente_id = opcoes_pacientes[paciente_escolhido]

            st.warning("Atenção: essa ação não pode ser desfeita.")

            if st.button("Excluir paciente"):
                pacientes_collection.delete_one({"_id": ObjectId(paciente_id)})
                st.success("Paciente excluído com sucesso!")


elif pagina == "Consultas":
    st.header("Consultas")

    aba_cadastrar_consulta, aba_listar_consulta, aba_editar_consulta, aba_excluir_consulta = st.tabs(
        ["Cadastrar", "Listar", "Editar", "Excluir"]
    )

    pacientes = list(pacientes_collection.find())
    consultas = list(consultas_collection.find())

    with aba_cadastrar_consulta:
        st.subheader("Cadastrar consulta")

        if len(pacientes) == 0:
            st.warning("Cadastre um paciente antes de cadastrar uma consulta.")
        else:
            opcoes_pacientes = montar_opcoes_pacientes()

            with st.form("form_cadastro_consulta"):
                paciente_escolhido = st.selectbox(
                    "Paciente",
                    list(opcoes_pacientes.keys())
                )

                data = st.date_input("Data da consulta")
                horario = st.time_input("Horário")
                especialidade = st.text_input("Especialidade")
                medico = st.text_input("Médico")
                status = st.selectbox(
                    "Status",
                    ["Agendada", "Realizada", "Cancelada"]
                )
                valor = st.number_input(
                    "Valor da consulta",
                    min_value=0.0,
                    step=10.0
                )

                botao_salvar_consulta = st.form_submit_button("Salvar consulta")

                if botao_salvar_consulta:
                    paciente_id = opcoes_pacientes[paciente_escolhido]

                    consulta = {
                        "paciente_id": ObjectId(paciente_id),
                        "data": str(data),
                        "horario": str(horario),
                        "especialidade": especialidade,
                        "medico": medico,
                        "status": status,
                        "valor": valor
                    }

                    consultas_collection.insert_one(consulta)
                    st.success("Consulta cadastrada com sucesso!")

    with aba_listar_consulta:
        st.subheader("Consultas cadastradas")

        consultas = list(consultas_collection.find())

        if len(consultas) == 0:
            st.info("Nenhuma consulta cadastrada ainda.")
        else:
            lista_consultas = []

            for consulta in consultas:
                paciente = pacientes_collection.find_one(
                    {"_id": consulta["paciente_id"]}
                )

                lista_consultas.append({
                    "_id": str(consulta["_id"]),
                    "paciente": paciente["nome"] if paciente else "Paciente não encontrado",
                    "data": consulta["data"],
                    "horario": consulta["horario"],
                    "especialidade": consulta["especialidade"],
                    "medico": consulta["medico"],
                    "status": consulta["status"],
                    "valor": consulta["valor"]
                })

            st.dataframe(pd.DataFrame(lista_consultas), use_container_width=True)

    with aba_editar_consulta:
        st.subheader("Editar consulta")

        if len(consultas) == 0:
            st.info("Nenhuma consulta cadastrada para editar.")
        elif len(pacientes) == 0:
            st.warning("Cadastre um paciente antes de editar consultas.")
        else:
            opcoes_consultas = montar_opcoes_consultas()

            consulta_escolhida = st.selectbox(
                "Escolha a consulta que deseja editar",
                list(opcoes_consultas.keys())
            )

            consulta_id = opcoes_consultas[consulta_escolhida]
            consulta = consultas_collection.find_one({"_id": ObjectId(consulta_id)})

            opcoes_pacientes = montar_opcoes_pacientes()
            lista_ids_pacientes = list(opcoes_pacientes.values())
            paciente_atual_id = str(consulta["paciente_id"])
            indice_paciente_atual = lista_ids_pacientes.index(paciente_atual_id)

            with st.form("form_editar_consulta"):
                novo_paciente_escolhido = st.selectbox(
                    "Paciente",
                    list(opcoes_pacientes.keys()),
                    index=indice_paciente_atual
                )

                nova_data = st.text_input("Data da consulta", value=consulta["data"])
                novo_horario = st.text_input("Horário", value=consulta["horario"])
                nova_especialidade = st.text_input(
                    "Especialidade",
                    value=consulta["especialidade"]
                )
                novo_medico = st.text_input("Médico", value=consulta["medico"])
                novo_status = st.selectbox(
                    "Status",
                    ["Agendada", "Realizada", "Cancelada"],
                    index=["Agendada", "Realizada", "Cancelada"].index(consulta["status"])
                )
                novo_valor = st.number_input(
                    "Valor da consulta",
                    min_value=0.0,
                    step=10.0,
                    value=float(consulta["valor"])
                )

                botao_atualizar_consulta = st.form_submit_button("Atualizar consulta")

                if botao_atualizar_consulta:
                    novo_paciente_id = opcoes_pacientes[novo_paciente_escolhido]

                    consultas_collection.update_one(
                        {"_id": ObjectId(consulta_id)},
                        {
                            "$set": {
                                "paciente_id": ObjectId(novo_paciente_id),
                                "data": nova_data,
                                "horario": novo_horario,
                                "especialidade": nova_especialidade,
                                "medico": novo_medico,
                                "status": novo_status,
                                "valor": novo_valor
                            }
                        }
                    )

                    st.success("Consulta atualizada com sucesso!")

    with aba_excluir_consulta:
        st.subheader("Excluir consulta")

        if len(consultas) == 0:
            st.info("Nenhuma consulta cadastrada para excluir.")
        else:
            opcoes_consultas = montar_opcoes_consultas()

            consulta_escolhida = st.selectbox(
                "Escolha a consulta que deseja excluir",
                list(opcoes_consultas.keys())
            )

            consulta_id = opcoes_consultas[consulta_escolhida]

            st.warning("Atenção: essa ação não pode ser desfeita.")

            if st.button("Excluir consulta"):
                consultas_collection.delete_one({"_id": ObjectId(consulta_id)})
                st.success("Consulta excluída com sucesso!")


elif pagina == "Diagnósticos":
    st.header("Diagnósticos")

    aba_cadastrar_diag, aba_listar_diag, aba_editar_diag, aba_excluir_diag = st.tabs(
        ["Cadastrar", "Listar", "Editar", "Excluir"]
    )

    consultas = list(consultas_collection.find())
    diagnosticos = list(diagnosticos_collection.find())

    with aba_cadastrar_diag:
        st.subheader("Cadastrar diagnóstico")

        if len(consultas) == 0:
            st.warning("Cadastre uma consulta antes de cadastrar um diagnóstico.")
        else:
            opcoes_consultas = montar_opcoes_consultas()

            with st.form("form_cadastro_diagnostico"):
                consulta_escolhida = st.selectbox(
                    "Consulta",
                    list(opcoes_consultas.keys())
                )

                sintomas = st.text_area("Sintomas")
                diagnostico = st.text_area("Diagnóstico")
                tratamento = st.text_area("Tratamento")
                observacoes = st.text_area("Observações")

                botao_salvar_diag = st.form_submit_button("Salvar diagnóstico")

                if botao_salvar_diag:
                    consulta_id = opcoes_consultas[consulta_escolhida]

                    novo_diagnostico = {
                        "consulta_id": ObjectId(consulta_id),
                        "sintomas": sintomas,
                        "diagnostico": diagnostico,
                        "tratamento": tratamento,
                        "observacoes": observacoes
                    }

                    diagnosticos_collection.insert_one(novo_diagnostico)
                    st.success("Diagnóstico cadastrado com sucesso!")

    with aba_listar_diag:
        st.subheader("Diagnósticos cadastrados")

        diagnosticos = list(diagnosticos_collection.find())

        if len(diagnosticos) == 0:
            st.info("Nenhum diagnóstico cadastrado ainda.")
        else:
            lista_diagnosticos = []

            for diag in diagnosticos:
                consulta = consultas_collection.find_one(
                    {"_id": diag["consulta_id"]}
                )

                if consulta:
                    paciente = pacientes_collection.find_one(
                        {"_id": consulta["paciente_id"]}
                    )
                    nome_paciente = paciente["nome"] if paciente else "Paciente não encontrado"
                    especialidade = consulta["especialidade"]
                    data_consulta = consulta["data"]
                else:
                    nome_paciente = "Consulta não encontrada"
                    especialidade = "-"
                    data_consulta = "-"

                lista_diagnosticos.append({
                    "_id": str(diag["_id"]),
                    "paciente": nome_paciente,
                    "especialidade": especialidade,
                    "data_consulta": data_consulta,
                    "sintomas": diag["sintomas"],
                    "diagnostico": diag["diagnostico"],
                    "tratamento": diag["tratamento"],
                    "observacoes": diag["observacoes"]
                })

            st.dataframe(pd.DataFrame(lista_diagnosticos), use_container_width=True)

    with aba_editar_diag:
        st.subheader("Editar diagnóstico")

        if len(diagnosticos) == 0:
            st.info("Nenhum diagnóstico cadastrado para editar.")
        else:
            opcoes_diagnosticos = {}

            for diag in diagnosticos:
                consulta = consultas_collection.find_one(
                    {"_id": diag["consulta_id"]}
                )

                if consulta:
                    paciente = pacientes_collection.find_one(
                        {"_id": consulta["paciente_id"]}
                    )
                    nome_paciente = paciente["nome"] if paciente else "Paciente não encontrado"
                    texto_opcao = f"{nome_paciente} - {consulta['data']} - {diag['diagnostico']}"
                else:
                    texto_opcao = f"Consulta não encontrada - {diag['diagnostico']}"

                opcoes_diagnosticos[texto_opcao] = str(diag["_id"])

            diagnostico_escolhido = st.selectbox(
                "Escolha o diagnóstico que deseja editar",
                list(opcoes_diagnosticos.keys())
            )

            diagnostico_id = opcoes_diagnosticos[diagnostico_escolhido]
            diag = diagnosticos_collection.find_one(
                {"_id": ObjectId(diagnostico_id)}
            )

            with st.form("form_editar_diagnostico"):
                novos_sintomas = st.text_area("Sintomas", value=diag["sintomas"])
                novo_diagnostico = st.text_area("Diagnóstico", value=diag["diagnostico"])
                novo_tratamento = st.text_area("Tratamento", value=diag["tratamento"])
                novas_observacoes = st.text_area("Observações", value=diag["observacoes"])

                botao_atualizar_diag = st.form_submit_button("Atualizar diagnóstico")

                if botao_atualizar_diag:
                    diagnosticos_collection.update_one(
                        {"_id": ObjectId(diagnostico_id)},
                        {
                            "$set": {
                                "sintomas": novos_sintomas,
                                "diagnostico": novo_diagnostico,
                                "tratamento": novo_tratamento,
                                "observacoes": novas_observacoes
                            }
                        }
                    )

                    st.success("Diagnóstico atualizado com sucesso!")

    with aba_excluir_diag:
        st.subheader("Excluir diagnóstico")

        if len(diagnosticos) == 0:
            st.info("Nenhum diagnóstico cadastrado para excluir.")
        else:
            opcoes_diagnosticos = {}

            for diag in diagnosticos:
                consulta = consultas_collection.find_one(
                    {"_id": diag["consulta_id"]}
                )

                if consulta:
                    paciente = pacientes_collection.find_one(
                        {"_id": consulta["paciente_id"]}
                    )
                    nome_paciente = paciente["nome"] if paciente else "Paciente não encontrado"
                    texto_opcao = f"{nome_paciente} - {consulta['data']} - {diag['diagnostico']}"
                else:
                    texto_opcao = f"Consulta não encontrada - {diag['diagnostico']}"

                opcoes_diagnosticos[texto_opcao] = str(diag["_id"])

            diagnostico_escolhido = st.selectbox(
                "Escolha o diagnóstico que deseja excluir",
                list(opcoes_diagnosticos.keys())
            )

            diagnostico_id = opcoes_diagnosticos[diagnostico_escolhido]

            st.warning("Atenção: essa ação não pode ser desfeita.")

            if st.button("Excluir diagnóstico"):
                diagnosticos_collection.delete_one(
                    {"_id": ObjectId(diagnostico_id)}
                )
                st.success("Diagnóstico excluído com sucesso!")