import json
from urllib.parse import urlencode

from django.test import TestCase
from rest_framework.reverse import reverse

from shiptrader.models import Starship, Listing


class TestStarshipView(TestCase):

    @classmethod
    def setUpTestData(cls):
        ships = get_ship_test_data()

        for ship in ships:
            Starship.objects.create(**ship)

    def tearDown(self):
        Listing.objects.all().delete()

    def test_can_get_starships(self):
        response = self.client.get(reverse('starship-list'))
        self.assertEqual(response.status_code, 200)

        starships = response.data
        expected_data = get_ship_test_data()

        self.assertEqual(len(starships), len(expected_data))

        for i in range(len(expected_data)):
            self.assertGreater(starships[i].pop('id'), 0)
            self.assertDictEqual(starships[i], expected_data[i])

    def test_can_get_listings(self):
        ship = Starship.objects.get(name='Ship 1')

        self.client.post(reverse('listing-list'), {'name': 'New Listing 1', 'price': 5,
                                                   'ship_type': ship.id, 'active': False})

        listing = Listing.objects.all().first()

        self.assertEqual(listing.name, 'New Listing 1')
        self.assertEqual(listing.price, 5)
        self.assertEqual(listing.ship_type, ship)
        self.assertEqual(listing.active, False)

    def test_can_create_listings(self):

        ship = Starship.objects.get(name='Ship 1')
        Listing.objects.create(name='Another New Listing', price=10, ship_type=ship)

        response = self.client.get(reverse('listing-list'))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Another New Listing')
        self.assertEqual(response.data[0]['ship_type'], ship.id)
        self.assertEqual(response.data[0]['price'], 10)
        self.assertEqual(response.data[0]['active'], True)

    def test_can_filter_by_class(self):
        for ship in Starship.objects.all():
            Listing.objects.create(name='Listing', price=10, ship_type=ship)

        url = '{0}?{1}'.format(reverse('listing-list'),
                               urlencode({'ship_type__starship_class': 'Class 2'}))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        ship_ids = [s.id for s in Starship.objects.filter(starship_class='Class 2')]
        self.assertTrue(response.data[0]['ship_type'] in ship_ids)
        self.assertTrue(response.data[1]['ship_type'] in ship_ids)

    def test_can_sort_by_price(self):
        ships = Starship.objects.all()
        Listing.objects.create(name='Listing', price=10, ship_type=ships[0])
        Listing.objects.create(name='Listing', price=20, ship_type=ships[1])
        Listing.objects.create(name='Listing', price=15, ship_type=ships[2])

        response = self.client.get('{0}?{1}'.format(reverse('listing-list'), urlencode({'ordering': '-price'})))
        self.assertEqual(response.data[0]['price'], 20)
        self.assertEqual(response.data[1]['price'], 15)
        self.assertEqual(response.data[2]['price'], 10)

        response = self.client.get('{0}?{1}'.format(reverse('listing-list'), urlencode({'ordering': 'price'})))
        self.assertEqual(response.data[0]['price'], 10)
        self.assertEqual(response.data[1]['price'], 15)
        self.assertEqual(response.data[2]['price'], 20)

    def test_can_sort_by_created(self):
        ships = Starship.objects.all()
        Listing.objects.create(name='Listing A', price=1, ship_type=ships[0])
        Listing.objects.create(name='Listing B', price=1, ship_type=ships[1])
        Listing.objects.create(name='Listing C', price=1, ship_type=ships[2])

        response = self.client.get('{0}?{1}'.format(reverse('listing-list'), urlencode({'ordering': '-created'})))
        self.assertEqual(response.data[0]['name'], 'Listing C')
        self.assertEqual(response.data[1]['name'], 'Listing B')
        self.assertEqual(response.data[2]['name'], 'Listing A')

        response = self.client.get('{0}?{1}'.format(reverse('listing-list'), urlencode({'ordering': 'created'})))
        self.assertEqual(response.data[0]['name'], 'Listing A')
        self.assertEqual(response.data[1]['name'], 'Listing B')
        self.assertEqual(response.data[2]['name'], 'Listing C')

    def test_can_toggle_active(self):

        listing = Listing.objects.create(name='Listing', price=10, ship_type=Starship.objects.first(), active=False)

        print(reverse('listing-detail', args=[listing.id]))

        response = self.client.patch(reverse('listing-detail', args=[listing.id]), json.dumps({'active': True}),
                                     content_type='application/json')
        listing = Listing.objects.get(id=listing.id)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(listing.active)


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
            'name': 'Ship 2a',
            'model': 'Model 2a',
            'starship_class': 'Class 2',
            'manufacturer': 'Manufacturer 2',
            'length': 21.0,
            'hyperdrive_rating': 22.0,
            'cargo_capacity': 23,
            'crew': 24,
            'passengers': 25
        },
        {
            'name': 'Ship 2b',
            'model': 'Model 2b',
            'starship_class': 'Class 2',
            'manufacturer': 'Manufacturer 2',
            'length': 21.0,
            'hyperdrive_rating': 22.0,
            'cargo_capacity': 23,
            'crew': 24,
            'passengers': 25
        }

    ]
