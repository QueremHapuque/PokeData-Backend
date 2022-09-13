import json
import pandas as pd
from pokeColuna import pokeId

dsP = pd.read_parquet('pokemon.parquet')
dsP = pokeId(dsP)

ds = open('pokemon.json')
dsjson = json.load(ds)

def list_Vulnerabilities(id):

    vulnerabilities = {
            "normal": float(*id['normal_attack_effectiveness'].values()),
            "fire": float(*id['fire_attack_effectiveness'].values()),
            "water": float(*id['water_attack_effectiveness'].values()),
            "electric": float(*id['electric_attack_effectiveness'].values()),
            "grass": float(*id['grass_attack_effectiveness'].values()),
            "ice": float(*id['ice_attack_effectiveness'].values()),
            "fighting": float(*id['fighting_attack_effectiveness'].values()),
            "poison": float(*id['poison_attack_effectiveness'].values()),
            "ground": float(*id['ground_attack_effectiveness'].values()),
            "fly": float(*id['fly_attack_effectiveness'].values()),
            "pyschic": float(*id['psychic_attack_effectiveness'].values()),
            "bug": float(*id['bug_attack_effectiveness'].values()),
            "rock": float(*id['rock_attack_effectiveness'].values()),
            "ghost": float(*id['ghost_attack_effectiveness'].values()),
            "dragon": float(*id['dragon_attack_effectiveness'].values()),
            "dark": float(*id['dark_attack_effectiveness'].values()),
            "steel": float(*id['steel_attack_effectiveness'].values()),
            "fairy": float(*id['fairy_attack_effectiveness'].values())
        }

    return vulnerabilities

