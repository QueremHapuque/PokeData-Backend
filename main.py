from operator import index
from flask import Flask, make_response, jsonify
import json
import pandas as pd
import cluster
import warnings
from pokeColuna import pokeId
from vulnerabilities import list_Vulnerabilities

warnings.filterwarnings("ignore")
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

print('LOG -- Importando Dataset')
dsP = pd.read_parquet('pokemon.parquet')
print('LOG -- Dataset importado')

print('LOG -- Habitando coluna de IDS')
dsP = pokeId(dsP)
print('LOG -- Coluna de IDS Habitada')

print('LOG -- Criando cluster')
cluster_column = cluster.create_cluster(dsP, 45)
print('LOG -- Cluster criado')

dsP['cluster_id'] = cluster_column

ds = open('pokemon.json')
dsjson = json.load(ds)


@app.route('/pokeinfo/<string:index>', methods=['GET'])
def aldataofpokemon(index):
    
    pokemon = dsP.loc[dsP['pokedex_number'] == int(index)].to_dict()
    
    pokemon_data = [
        {
            "name": str(pokemon['name'].values()),
            "typing":str(pokemon['typing'].values()),
            "primary_color": str(pokemon['primary_color'].values()),
            "height": str(pokemon['height'].values()),
            "weight": str(pokemon['weight'].values()),
            "gen_introduced": str(pokemon['gen_introduced'].values()),
            "hp": str(pokemon['hp'].values()),
            "attack":str(pokemon['attack'].values()),
            "defense": str(pokemon['defense'].values()),
            "speed": str(pokemon['speed'].values()),
            "special_attack": str(pokemon['special_attack'].values()),
            "special_defense": str(pokemon['special_defense'].values()),
            "abilities": str(pokemon['abilities'].values()),
            "id": str(pokemon['id'].values())
        }
    ]

    return make_response(
        jsonify(pokemon_data)
    )

@app.route('/allweaknessofpokemon/<string:id>', methods=['GET'])
def allweaknessofpokemon(id):
    pokemon = dsP.loc[dsP['id'] == str(id)].to_dict()
    vulnerabilities = list_Vulnerabilities(pokemon)
    bigger = 0
    type1 = ''
    type2 = ''

    for key, value in vulnerabilities.items():
        if value > bigger:
            type2 = type1
            type1 = key

    weakness = [
        {
            "type_1": type1,
            "type_2": type2,
        }
    ]

    return make_response(
        jsonify(vulnerabilities)
    )

@app.route('/alladvantageofpokemon/<string:tipo>', methods=['GET'])
def alladvantageofpokemon(tipo):

    listaMultplicador = []
    listaIndex = []
    contador = 0
    ataq = 'fire_attack_effectiveness'
    maior = 0
    tipo1 = ''
    tipo2 = ''
    rep = ataq.replace('fire', tipo)
    for mult in dsjson[rep]:
        if int(dsjson[rep][mult]) >= maior:
            maior = int(dsjson[rep][mult])
            listaMultplicador.append(maior)
            listaIndex.append(mult)

    for i in range(len(listaIndex)):
        contador -= 1
        if tipo1 == '':
            tipo1 = dsjson['typing'][listaIndex[contador]]
        if tipo1 != dsjson['typing'][listaIndex[contador]]:
            tipo2 = dsjson['typing'][listaIndex[contador]]
            break
    vantagens = [
        {
            "type_1": tipo1,
            "type_2": tipo2
        }
    ]
    return make_response(
        jsonify(vantagens)
    )

@app.route('/status/<string:id>', methods=['GET'])
def allstatusofpokemon(id):
    pokemon = dsP.loc[dsP['id'] == str(id)].to_dict()

    pokemon_status = [
        {
            "hp": str(pokemon['hp'].values()),
            "attack": str(pokemon['attack'].values()),
            "defense": str(pokemon['defense'].values()),
            "speed": str(pokemon['speed'].values()),
            "special_attack": str(pokemon['special_attack'].values()),
            "special_defense": str(pokemon['special_defense'].values())
        }
    ]

    return make_response(
        jsonify(pokemon_status)
    )

@app.route('/allpokemons', methods=['GET'])
def allpokemons():
    pokemon = dsP

    allpikomons = []

    for i in range(len(pokemon)):
        allpikomons.append({
            "name": str(pokemon.loc[i, 'name']),
            "id": str(pokemon.loc[i, 'id']),
            "typing": str(pokemon.loc[i, 'typing']),
            "pokedex_number": str(pokemon.loc[i, 'pokedex_number']),
            "img": str(pokemon.loc[i, 'id'])
        })

    return make_response(
        jsonify(allpikomons)
    )


@app.route('/pokemonscluster/<string:id>', methods=['GET'])
def cluster_by_pokemon(id):
    local_ds = dsP.copy()
    
    pokemon_input_id = local_ds.index[local_ds['id'] == id].tolist()[0]
    pokemon_input_cluster_index = local_ds.loc[pokemon_input_id,'cluster_id']
    print(pokemon_input_cluster_index)

    pokemons_by_cluster_id = local_ds.loc[local_ds['cluster_id']
                                     == pokemon_input_cluster_index]

    print(pokemons_by_cluster_id)
    
    all_pikomons = []

    for i in pokemons_by_cluster_id.index:
        all_pikomons.append({
            "name": str(pokemons_by_cluster_id.loc[i, 'name']),
            "id": str(pokemons_by_cluster_id.loc[i, 'id']),
            "typing": str(pokemons_by_cluster_id.loc[i, 'typing']),
            "pokedex_number": str(pokemons_by_cluster_id.loc[i, 'pokedex_number']),
            "img": str(pokemons_by_cluster_id.loc[i, 'id'])
        })

    return make_response(
        jsonify(all_pikomons)
    )


app.run()
