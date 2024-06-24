from django.test import TestCase
from datetime import datetime, date
from .utils import get_data
date_str = "20240624T115225.000Z"

# Extrahovat datum
extracted_date_str = date_str[:8]  # "20240624"

# Převést na formát datetime
extracted_date = datetime.strptime(extracted_date_str, '%Y%m%d').date()
# print(extracted_date, date.today())
# Create your tests here.
print(get_data.battle_log("#232Q0U9PJLP"))
