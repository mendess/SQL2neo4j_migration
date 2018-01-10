import sql_module
from sql_module import runQuery
import neo4j_module
import json

db = sql_module.connect()

cursorCategoria             = runQuery(db,"SELECT * FROM Categoria;")
cursorCidade                = runQuery(db,"SELECT * FROM Cidade;")
cursorCinema                = runQuery(db,"SELECT * FROM Cinema;")
cursorFilme                 = runQuery(db,"SELECT * FROM Filme;")
cursorFilme_a_Categoria     = runQuery(db,"SELECT * FROM Filme_associado_Categoria;")
cursorFilme_e_Cinema        = runQuery(db,"SELECT * FROM Filme_exibido_Cinema;")
cursorFilme_tA_Participante = runQuery(db,"SELECT * FROM Filme_temAtor_Participante;")
cursorFilme_tR_Participante = runQuery(db,"SELECT * FROM Filme_temRealizador_Participante;")
cursorParticipante          = runQuery(db,"SELECT * FROM Participante;")

categorias = []
cidades = []
cinemas = []
filmes = []
filmeAcat = []
filmeEcinema = []
filmeTAparticipante = []
filmeTRparticipante = []
participantes = []

print("IMPORTING CATEGORIAS")
for row in cursorCategoria.fetchall():
    categoria = {}
    categoria['ID']   = row[0]
    categoria['Nome'] = row[1]
    categorias.append(categoria)

print("IMPORTING CIDADES")
for row in cursorCidade.fetchall():
    cidade = {}
    cidade['ID']   = row[0]
    cidade['Nome'] = row[1]
    cidades.append(cidade)

print("IMPORTING CINEMAS")
for row in cursorCinema.fetchall():
    cinema = {}
    cinema['ID']            = row[0]
    cinema['Nome']          = row[1]
    cinema['Rua']           = row[2]
    cinema['CodigoPostal']  = row[3]
    cinema['Classificacao'] = row[4]
    cinema['Cidade_ID']     = row[5]
    cinemas.append(cinema)

print("IMPORTING PARTICIPANTES")
for row in cursorParticipante.fetchall():
    participante = {}
    participante['ID']             = row[0]
    participante['Nome']           = row[1]
    participante['DataNascimento'] = row[2]
    participante['Fotografia']     = row[3]
    participantes.append(participante)

print("IMPORTING FILMES")
for row in cursorFilme.fetchall():
    filme = {}
    filme['ID']                  = row[0]
    filme['Titulo']              = row[1]
    filme['Subtitulo']           = row[2]
    filme['Cartaz']              = row[3]
    filme['AnoLancamento']       = row[4]
    filme['ClassificacaoEtaria'] = row[5]
    filme['Duracao']             = row[6]
    filme['Sinopse']             = row[7]
    filme['Classificacao']       = row[8]
    filmes.append(filme)

print("IMPORTING ASSOCIACOES FILME -> CATEGORIA")
for row in cursorFilme_a_Categoria.fetchall():
    fAc = {}
    fAc['Filme_ID']     = row[0]
    fAc['Categoria_ID'] = row[1]
    filmeAcat.append(fAc)

print("IMPORTING ASSOCIACOES FILME -> CINEMA")
for row in cursorFilme_e_Cinema.fetchall():
    fEc = {}
    fEc['Filme_ID']     = row[0]
    fEc['Cinema_ID']    = row[1]
    filmeEcinema.append(fEc)

print("IMPORTING ASSOCIACOES FILME -> ATOR")
for row in cursorFilme_tA_Participante.fetchall():
    fTAp = {}
    fTAp['Filme_ID']        = row[0]
    fTAp['Participante_ID'] = row[1]
    filmeTAparticipante.append(fTAp)

print("IMPORTING ASSOCIACOES FILME -> REALIZADOR")
for row in cursorFilme_tR_Participante.fetchall():
    fTRp = {}
    fTRp['Filme_ID']        = row[0]
    fTRp['Participante_ID'] = row[1]
    filmeTRparticipante.append(fTRp)

# tables = [categorias,           #
#           cidades,              #
#           cinemas,              #
#           filmes,               #
#           filmeAcat,
#           filmeEcinema,
#           filmeTAparticipante,
#           filmeTRparticipante,
#           participantes]        #

# for table in tables:
#     for thing in table:
#         print(thing)
#     print("\n")

db.close()

neoDriver = neo4j_module.connect()

print("***\nCLEARING DATABASE\n***")
neo4j_module.clearDB(neoDriver)

with neoDriver.session() as session:
    print("MIGRATING CATEGORIAS")
    with session.begin_transaction() as tx:
        for cat in categorias:
            neo4j_module.create_categoria(tx,cat['ID'],cat['Nome'])

    print("MIGRATING CIDADES")
    with session.begin_transaction() as tx:
        for cidade in cidades:
            neo4j_module.create_cidade(tx,cidade['ID'],cidade['Nome'])

    print("MIGRATING CINEMAS")
    with session.begin_transaction() as tx:
        for cinema in cinemas:
            neo4j_module.create_cinema(tx,
                                       cinema['ID'],
                                       cinema['Nome'],
                                       cinema['Rua'],
                                       cinema['CodigoPostal'],
                                       cinema['Classificacao'],
                                       cinema['Cidade_ID'])

    print("MIGRATING PARTICIPANTES")
    with session.begin_transaction() as tx:
        for participante in participantes:
            neo4j_module.create_participante(tx,
                                             participante['ID'],
                                             participante['Nome'],
                                             participante['DataNascimento'],
                                             participante['Fotografia'])

    print("MIGRATING FILMES")
    with session.begin_transaction() as tx:
        for filme in filmes:
            neo4j_module.create_filme(tx,
                                      filme['ID'],
                                      filme['Titulo'],
                                      filme['Subtitulo'],
                                      filme['Cartaz'],
                                      filme['AnoLancamento'],
                                      filme['ClassificacaoEtaria'],
                                      filme['Duracao'],
                                      filme['Sinopse'],
                                      filme['Classificacao'])

    print("MIGRATING ASSOCIACOES FILME -> CATEGORIA")
    with session.begin_transaction() as tx:
        for relationship in filmeAcat:
            neo4j_module.create_filme_associado_categoria(tx,
                                                          relationship['Filme_ID'],
                                                          relationship['Categoria_ID'])

    print("MIGRATING ASSOCIACOES FILME -> CINEMA")
    with session.begin_transaction() as tx:
        for relationship in filmeEcinema:
            neo4j_module.create_filme_exibido_cinema(tx,
                                                     relationship['Filme_ID'],
                                                     relationship['Cinema_ID'])

    print("MIGRATING ASSOCIACOES FILME -> ATOR")
    with session.begin_transaction() as tx:
        for relationship in filmeTAparticipante:
            neo4j_module.create_filme_temAtor_participante(tx,
                                                           relationship['Filme_ID'],
                                                           relationship['Participante_ID'])

    print("MIGRATING ASSOCIACOES FILME -> REALIZADOR")
    with session.begin_transaction() as tx:
        for relationship in filmeTRparticipante:
            neo4j_module.create_filme_temRealizador_participante(tx,
                                                                 relationship['Filme_ID'],
                                                                 relationship['Participante_ID'])

neoDriver.close()
print("ALL DONE :)")