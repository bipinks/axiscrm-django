# <project>/<app>/management/commands/seed.py
from django.core.management.base import BaseCommand
import random

# python manage.py seed --mode=refresh
from django.db.backends.base.schema import logger

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    pass
    # logger.info("Delete Address instances")
    # Address.objects.all().delete()


def create_address(self):
    """Creates an address object combining different elements from the list"""

    self.stdout.write("Creating address")

    street_flats = ["#221 B", "#101 A", "#550I", "#420G", "#A13"]
    street_localities = ["Bakers Street", "Rajori Gardens", "Park Street", "MG Road", "Indiranagar"]
    pincodes = ["101234", "101232", "101231", "101236", "101239"]

    address = Address(
        street_flat=random.choice(street_flats),
        street_locality=random.choice(street_localities),
        pincode=random.choice(pincodes),
    )
    address.save()
    logger.info("{} address created.".format(address))

    return address


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Creating 15 addresses
    for i in range(15):
        create_address(self)
