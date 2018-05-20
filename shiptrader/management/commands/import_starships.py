import requests
from django.core.management.base import BaseCommand

from shiptrader.models import Starship


class Command(BaseCommand):
    help = 'Retrieves starship data from the swapi.co api '

    def handle(self, *args, **options):

        url = 'https://swapi.co/api/starships/'
        starships = []

        while url is not None:
            response = requests.get(url)
            response_json = response.json()
            url = response_json['next']
            starships += [build_starship(result) for result in response_json['results']]

        Starship.objects.all().delete()
        Starship.objects.bulk_create(starships)


def build_starship(data):
    return Starship(name=data['name'],
                    model=data['model'],
                    starship_class=data['starship_class'],
                    manufacturer=data['manufacturer'],
                    length=float(convert_unknown(data['length'])),
                    hyperdrive_rating=float(convert_unknown(data['hyperdrive_rating'])),
                    cargo_capacity=int(convert_unknown(data['cargo_capacity'])),
                    crew=int(convert_unknown(data['crew'])),
                    passengers=int(convert_unknown(data['passengers'])))


def convert_unknown(value):
    return value.replace(',', '.') if value != 'unknown' else 0
