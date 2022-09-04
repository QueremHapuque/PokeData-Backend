from flask import Flask
from flask_restx import Api, Resource

from src.server.instance import server

app, api = server.app, server.api

poke = [
    {
        'id': 1,
        'name': 'pikachu', 
    },
    {
        'id': 2,
        'name': 'charizard', 
    },
    {
        'id': 3,
        'name': 'bubasauro', 
    }
]

@api.route('/pokes')
class PokeList(Resource):
    def get(self):
        return poke