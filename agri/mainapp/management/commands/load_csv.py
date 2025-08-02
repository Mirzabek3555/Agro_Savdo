import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from mainapp.models import CropCalendar  # Adjust to your app name

class Command(BaseCommand):
    help = 'Load crop calendar data from CSV'

    def handle(self, *args, **kwargs):
        file_path = '/home/antsy/Downloads/Crop_Calendar_Data_All.csv'  # Update with correct path

        with open(file_path, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                CropCalendar.objects.create(
                    crop_name=row.get('Crop', '').strip(),
                    planting_start=datetime.strptime(row['Early Sowing'], '%Y-%m-%d').date(),
                    planting_end=datetime.strptime(row['Later Sowing'], '%Y-%m-%d').date(),
                    harvesting_start=datetime.strptime(row['Early harvest'], '%Y-%m-%d').date(),
                    harvesting_end=datetime.strptime(row['Late harvest'], '%Y-%m-%d').date(),
                    region=row.get('region', '')
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded crop calendar data!'))
