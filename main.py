from flask import Flask, make_response, jsonify
import json
import pandas as pd
from pokeColuna import pokeId

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

dsP = pd.read_parquet('pokemon.parquet')
dsP = pokeId(dsP)
print(dsP)

ds = open('pokemon.json')
dsjson = json.load(ds)


@app.route('/alldataofpokemon/<string:index>', methods=['GET'])
def alldataofpokemon(index):
    
    pokemon = dsP.loc[dsP['pokedex_number'] == int(index)].to_dict()
    
    pokemon_data = [
        {
            "name": pokemon['name'],
            "typing":pokemon['typing'],
            "primary_color": pokemon['primary_color'],
            "height": pokemon['height'],
            "weight": pokemon['weight'],
            "gen_introduced": pokemon['gen_introduced'],
            "hp": pokemon['hp'],
            "attack":pokemon['attack'],
            "defense": pokemon['defense'],
            "speed": pokemon['speed'],
            "special_attack": pokemon['special_attack'],
            "special_defense": pokemon['special_defense'],
            "abilities": pokemon['abilities'],
            "id": pokemon['id']
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

app.run()
