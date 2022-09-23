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
cluster_column = cluster.create_cluster(dsP, 40)
print('LOG -- Cluster criado')

dsP['cluster_id'] = cluster_column

ds = open('pokemon.json')
dsjson = json.load(ds)

vulnerabilities = ['normal_attack_effectiveness',
                   'fire_attack_effectiveness',
                   'water_attack_effectiveness',
                   'electric_attack_effectiveness',
                   'grass_attack_effectiveness',
                   'ice_attack_effectiveness',
                   'fighting_attack_effectiveness',
                   'poison_attack_effectiveness',
                   'ground_attack_effectiveness',
                   'fly_attack_effectiveness',
                   'psychic_attack_effectiveness',
                   'bug_attack_effectiveness',
                   'rock_attack_effectiveness',
                   'ghost_attack_effectiveness',
                   'dragon_attack_effectiveness',
                   'dark_attack_effectiveness',
                   'steel_attack_effectiveness',
                   'fairy_attack_effectiveness']


def weaknesses(pokemon_index, local_ds):
    vuls = vulnerabilities.copy()
    max_controller = 20
    max_vuls = [0, 0]
    for vul in vuls:
        iter_vul = int(local_ds.loc[pokemon_index, vul])
        if iter_vul < max_controller:
            max_controller = iter_vul
            max_vuls[0] = vul

    vuls.remove(max_vuls[0])
    max_controller = 20

    for vul in vuls:
        iter_vul = int(local_ds.loc[pokemon_index, vul])
        if iter_vul < max_controller:
            max_controller = iter_vul
            max_vuls[1] = vul

    return {
        'type1': max_vuls[0].split('_')[0].capitalize(),
        'type2': max_vuls[1].split('_')[0].capitalize()
    }


def advantages(pokemon_index, local_ds):
    vuls = vulnerabilities.copy()
    max_controller = 0
    max_vuls = [0, 0]
    for vul in vuls:
        iter_vul = int(local_ds.loc[pokemon_index, vul])
        if iter_vul > max_controller:
            max_controller = iter_vul
            max_vuls[0] = vul

    vuls.remove(max_vuls[0])
    max_controller = 0

    for vul in vuls:
        iter_vul = int(local_ds.loc[pokemon_index, vul])
        if iter_vul > max_controller:
            max_controller = iter_vul
            max_vuls[1] = vul

    return {
        'type1': max_vuls[0].split('_')[0].capitalize(),
        'type2': max_vuls[1].split('_')[0].capitalize()
    }


def types_to_map(types_string):
    types_list = types_string.split('~')
    types_dict = {}
    for i in range(len(types_list)):
        types_dict["type"+str(i+1)] = types_list[i]
    return types_dict


def abilities_to_map(abilities_string):
    abilities_list = abilities_string.split('~')
    abilities_dict = {}
    for i in range(len(abilities_list)):
        abilities_dict["ability"+str(i+1)] = abilities_list[i]
    return abilities_dict


@app.route('/alldataofpokemon/<string:id>', methods=['GET'])
def alldataofpokemon(id):

    local_ds = dsP.copy()
    pokemon = local_ds.loc[dsP['id'] == str(id)].to_dict()
    pokemon_input_index = local_ds.index[local_ds['id'] == id].tolist()[0]

    pokemon_data = {
        "name": str(*pokemon['name'].values()),
        "genus": str(*pokemon['genus'].values()),
        "typing": str(types_to_map(*pokemon['typing'].values())),
        "primary_color": str(*pokemon['primary_color'].values()),
        "height": str(*pokemon['height'].values()),
        "weight": str(*pokemon['weight'].values()),
        "hp": str(*pokemon['hp'].values()),
        "attack": str(*pokemon['attack'].values()),
        "defense": str(*pokemon['defense'].values()),
        "speed": str(*pokemon['speed'].values()),
        "special_attack": str(*pokemon['special_attack'].values()),
        "special_defense": str(*pokemon['special_defense'].values()),
        "abilities": str(abilities_to_map(*pokemon['abilities'].values())),
        "id": str(*pokemon['id'].values()),
        "weaknesses": str(weaknesses(pokemon_input_index, local_ds)),
        "advantages": str(advantages(pokemon_input_index, local_ds)),
        "pokedex_number": str(*pokemon['pokedex_number'])}

    return make_response(
        jsonify(pokemon_data)
    )


@app.route('/alladvantageofpokemon/<string:id>', methods=['GET'])
def alladvantageofpokemon(id):

    local_ds = dsP.copy()
    vuls = vulnerabilities.copy()
    pokemon_input_index = local_ds.index[local_ds['id'] == id].tolist()[0]

    max_controller = 0
    max_vuls = [0, 0]
    for vul in vuls:
        iter_vul = int(local_ds.loc[pokemon_input_index, vul])
        if iter_vul > max_controller:
            max_controller = iter_vul
            max_vuls[0] = vul

    vuls.remove(max_vuls[0])
    max_controller = 0

    for vul in vuls:
        iter_vul = int(local_ds.loc[pokemon_input_index, vul])
        if iter_vul > max_controller:
            max_controller = iter_vul
            max_vuls[1] = vul

    json_body_list = [{
        'type1': max_vuls[0].split('_')[0].capitalize(),
        'type2': max_vuls[1].split('_')[0].capitalize()
    }]

    return make_response(
        jsonify(json_body_list)
    )


@app.route('/allweaknessofpokemon/<string:id>', methods=['GET'])
def allweaknessofpokemon(id):

    local_ds = dsP.copy()
    vuls = vulnerabilities.copy()
    pokemon_input_index = local_ds.index[local_ds['id'] == id].tolist()[0]

    max_controller = 20
    max_vuls = [0, 0]
    for vul in vuls:
        iter_vul = int(local_ds.loc[pokemon_input_index, vul])
        if iter_vul < max_controller:
            max_controller = iter_vul
            max_vuls[0] = vul

    vuls.remove(max_vuls[0])
    max_controller = 20

    for vul in vuls:
        iter_vul = int(local_ds.loc[pokemon_input_index, vul])
        if iter_vul < max_controller:
            max_controller = iter_vul
            max_vuls[1] = vul

    json_body_list = [{
        'type1': max_vuls[0].split('_')[0].capitalize(),
        'type2': max_vuls[1].split('_')[0].capitalize()
    }]

    return make_response(
        jsonify(json_body_list)
    )


@app.route('/allstatusofpokemon/<string:id>', methods=['GET'])
def allstatusofpokemon(id):
    pokemon = dsP.loc[dsP['id'] == str(id)].to_dict()

    pokemon_status = [
        {
            "hp": str(*pokemon['hp'].values()),
            "attack": str(*pokemon['attack'].values()),
            "defense": str(*pokemon['defense'].values()),
            "speed": str(*pokemon['speed'].values()),
            "special_attack": str(*pokemon['special_attack'].values()),
            "special_defense": str(*pokemon['special_defense'].values())
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
    pokemon_input_cluster_index = local_ds.loc[pokemon_input_id, 'cluster_id']

    pokemons_by_cluster_id = local_ds.loc[local_ds['cluster_id']
                                          == pokemon_input_cluster_index]

    all_pokemons = []

    for i in pokemons_by_cluster_id.index:
        all_pokemons.append({
            "name": str(pokemons_by_cluster_id.loc[i, 'name']),
            "id": str(pokemons_by_cluster_id.loc[i, 'id']),
            "typing": str(pokemons_by_cluster_id.loc[i, 'typing']),
            "pokedex_number": str(pokemons_by_cluster_id.loc[i, 'pokedex_number']),
            "img": str(pokemons_by_cluster_id.loc[i, 'id'])
        })

    return make_response(
        jsonify(all_pokemons)
    )


app.run()
