import requests
import random
class Pokemon:
    def __init__(self, id = None):
        self.url = "https://pokeapi.co/api/v2/pokemon/"
        self.id = id
        self.pokemon = None
    
    def __str__(self):
        return f"{self.pokemon['name']} #{self.pokemon['id']}\n"
    
    def get(self):
        response = requests.get(self.url + self.id)
        data = response.json()
        # return data['name']
        self.pokemon = {
            'id': data['id'],
            'name': data['name'],
            'abilities': [item['ability']['name'] for item in data['abilities']],
            'specie': data['species']['url']
        }
        
class Pokedex:
    def __init__(self):
        self.url = "https://pokeapi.co/api/v2/pokemon/"
        self.pokemons = []
    
    def all(self):
        response = requests.get(self.url + "?limit=151")
        data = response.json()
        self.pokemons = [item['name'] for item in data['results']]
    
    def getPokemon(self, id):
        pokemon = Pokemon(id)
        pokemon.get()
        return pokemon
    
    def catch(self, pokemon):
        response = requests.get(pokemon['specie'])
        data = response.json()
        # print(data['capture_rate'])
        capture_rate = data['capture_rate']
        random_number = random.randint(1, 255)
        print(f"{random_number} <= {capture_rate}")
        if random_number <= capture_rate:
            print(f"You caught {data['name']}!\n")
        else:
            print(f"{data['name']} has escaped!\n")

    def search(self, term):
        print(f'Searching..."{term}"')
        hits = [pokemon for pokemon in self.pokemons if term in pokemon]
        return hits     
    
    def evolve(self, evolve_info):
        # Obtenemos el pokemon-specie donde encontramos el evolution_chain:
        response = requests.get(evolve_info['specie'])
        data = response.json()
        # Obtenemos la info que esta dentro del evotion-chain del pokemon:
        evolution = requests.get(data['evolution_chain']['url'])
        evolution_data = evolution.json()
        # Obtenemos la primera evolucion del pokemon:
        evolves_to_info = [item['species'] for item in evolution_data['chain']['evolves_to']]
        evolves_to = evolves_to_info[0]['name']
        print(f"Evolves to {evolves_to}")
        
pokedex = Pokedex()
# Get ALL pokemons
pokedex.all()

"""GET POKEMONS"""
# pikachu = pokedex.getPokemon("25")
# print(pikachu)
charmander = pokedex.getPokemon("4")
print(charmander)

"""CATCH POKEMONS"""
pokedex.catch(charmander.pokemon)
# pokedex.catch(pikachu.pokemon)

""""SEARCH POKEMONS"""
# hits = pokedex.search('char')
# print(hits)

"""EVOLVE POKEMONS"""
pokedex.evolve(charmander.pokemon)
