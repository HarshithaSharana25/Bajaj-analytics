import json
from datetime import datetime
import numpy as np
from collections import Counter

file_path = 'DataEngineeringQ2.json'
with open(file_path, 'r') as file:
    data = json.load(file)

def is_valid_indian_phone_number(phone_number):
    if phone_number.startswith('+91'):
        phone_number = phone_number[3:]
    elif phone_number.startswith('91'):
        phone_number = phone_number[2:]
    if phone_number.isdigit() and len(phone_number) == 10:
        number = int(phone_number)
        if 6000000000 <= number <= 9999999999:
            return True
    return False

valid_phone_count = 0
for record in data:
    phone_number = record.get('phoneNumber', '')
    is_valid = is_valid_indian_phone_number(phone_number)
    record['isValidMobile'] = is_valid
    if is_valid:
        valid_phone_count += 1

total_medicines = 0
records_with_medicines = 0
for record in data:
    medicines = record.get('consultationData', {}).get('medicines', [])
    if medicines:
        total_medicines += len(medicines)
        records_with_medicines += 1
average_medicines = total_medicines / records_with_medicines if records_with_medicines > 0 else 0
average_medicines_rounded = round(average_medicines, 2)

medicine_names = []
for record in data:
    medicines = record.get('consultationData', {}).get('medicines', [])
    for medicine in medicines:
        medicine_names.append(medicine.get('medicineName'))
medicine_frequency = Counter(medicine_names)
third_most_frequent = medicine_frequency.most_common(3)[2][0]

active_medicines = 0
inactive_medicines = 0
for record in data:
    medicines = record.get('consultationData', {}).get('medicines', [])
    for medicine in medicines:
        if medicine.get('isActive', False):
            active_medicines += 1
        else:
            inactive_medicines += 1
total_medicines_count = active_medicines + inactive_medicines
active_percentage = (active_medicines / total_medicines_count) * 100 if total_medicines_count > 0 else 0
inactive_percentage = (inactive_medicines / total_medicines_count) * 100 if total_medicines_count > 0 else 0
active_percentage_rounded = round(active_percentage, 2)
inactive_percentage_rounded = round(inactive_percentage, 2)

def calculate_age(birth_date):
    if birth_date:
        try:
            birth_date = datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            today = datetime.today()
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        except ValueError:
            return None
    return None

ages = []
medicine_counts = []
for record in data:
    birth_date = record.get('patientDetails', {}).get('birthDate')
    age = calculate_age(birth_date)
    medicines = record.get('consultationData', {}).get('medicines', [])
    medicine_count = len(medicines)
    if age is not None:
        ages.append(age)
        medicine_counts.append(medicine_count)
if ages and medicine_counts:
    correlation = np.corrcoef(ages, medicine_counts)[0, 1]
    correlation_rounded = round(correlation, 2)
else:
    correlation_rounded = None

results = {
    "valid_phone_count": valid_phone_count,
    "average_medicines": average_medicines_rounded,
    "third_most_frequent_medicine": third_most_frequent,
    "active_percentage": active_percentage_rounded,
    "inactive_percentage": inactive_percentage_rounded,
    "correlation": correlation_rounded
}

print(results)
