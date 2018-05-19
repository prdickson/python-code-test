from django.core.management import call_command
from django.test import TestCase
from rest_framework.reverse import reverse

from shiptrader.models import Starship


class TestImportStarships(TestCase):

    def test_can_import_starships(self):

        call_command('import_starships')
        starships = Starship.objects.all()
        self.assertGreater(len(starships), 0)

        executor = next(filter(lambda s: s.name == 'Executor', starships))

        self.assertEqual(executor.name, 'Executor')
        self.assertEqual(executor.model, 'Executor-class star dreadnought')
        self.assertEqual(executor.starship_class, 'Star dreadnought')
        self.assertEqual(executor.manufacturer, 'Kuat Drive Yards, Fondor Shipyards')

        self.assertEqual(executor.length, 19000.0)
        self.assertEqual(executor.hyperdrive_rating, 2.0)
        self.assertEqual(executor.cargo_capacity, 250000000)

        self.assertEqual(executor.crew, 279144)
        self.assertEqual(executor.passengers, 38000)
