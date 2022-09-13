from operator import index
from flask import Flask, make_response, jsonify
import json
import pandas as pd
from pokeColuna import pokeId
from vulnerabilities import list_Vulnerabilities

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

dsP = pd.read_parquet('pokemon.parquet')
dsP = pokeId(dsP)

ds = open('pokemon.json')
dsjson = json.load(ds)


@app.route('/alldataofpokemon/<string:id>', methods=['GET'])
def alldataofpokemon(id):
    
    pokemon = dsP.loc[dsP['id'] == str(id)].to_dict()
    
    pokemon_data = [
        {
            "name": str(*pokemon['name'].values()),
            "typing":str(*pokemon['typing'].values()),
            "primary_color": str(*pokemon['primary_color'].values()),
            "height": str(*pokemon['height'].values()),
            "weight": str(*pokemon['weight'].values()),
            "gen_introduced": str(*pokemon['gen_introduced'].values()),
            "hp": str(*pokemon['hp'].values()),
            "attack":str(*pokemon['attack'].values()),
            "defense": str(*pokemon['defense'].values()),
            "speed": str(*pokemon['speed'].values()),
            "special_attack": str(*pokemon['special_attack'].values()),
            "special_defense": str(*pokemon['special_defense'].values()),
            "abilities": str(*pokemon['abilities'].values()),
            "id": str(*pokemon['id'].values())
        }
    ]

    return make_response(
        jsonify(pokemon_data)    
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
            "name": str(pokemon.loc[i,'name']),
            "id": str(pokemon.loc[i,'id']),
            "typing": str(pokemon.loc[i,'typing']),
            "pokedex_number": str(pokemon.loc[i,'pokedex_number']),
            "img": str(pokemon.loc[i,'id'])
        })

    return make_response(
        jsonify(allpikomons)
    )

app.run()
