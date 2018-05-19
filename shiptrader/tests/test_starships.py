from django.test import TestCase
from rest_framework.reverse import reverse

from shiptrader.models import Starship


class TestStarshipView(TestCase):

    @classmethod
    def setUpTestData(cls):
        ships = get_ship_test_data()

        Starship.objects.create(**ships[0])
        Starship.objects.create(**ships[1])

        cls.maxDiff = None

    def test_can_list_starships(self):
        response = self.client.get(reverse('starship-list'))
        self.assertEqual(response.status_code, 200)

        starships = response.data
        self.assertEqual(len(starships), 2)

        expected_data = get_ship_test_data()

        self.assertGreater(starships[0].pop('id'), 0)
        self.assertDictEqual(starships[0], expected_data[0])

        self.assertGreater(starships[1].pop('id'), 0)
        self.assertDictEqual(starships[1], expected_data[1])


def get_ship_test_data():
    return [
        {
            'name': 'Ship 1',
            'model': 'Model 1',
            'starship_class': 'Class 1',
            'manufacturer': 'Manufacturer 1',
            'length': 11.0,
            'hyperdrive_rating': 12.0,
            'cargo_capacity': 13,
            'crew': 14,
            'passengers': 15
        },
        {
            'name': 'Ship 2',
            'model': 'Model 2',
            'starship_class': 'Class 2',
            'manufacturer': 'Manufacturer 2',
            'length': 21.0,
            'hyperdrive_rating': 22.0,
            'cargo_capacity': 23,
            'crew': 24,
            'passengers': 25
        }
    ]
