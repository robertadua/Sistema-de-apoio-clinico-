import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

neo4j_driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)


def testar_conexao_neo4j():
    with neo4j_driver.session() as session:
        resultado = session.run("RETURN 'Neo4j conectado com sucesso!' AS mensagem")
        return resultado.single()["mensagem"]