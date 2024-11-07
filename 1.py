import csv
from faker import Faker
import random

fake = Faker('uk_UA')
male_patronymics = [
    "Олександрович", "Михайлович", "Сергійович", "Іванович",
    "Володимирович", "Павлович", "Анатолійович", "Юрійович",
    "Андрійович", "Петрович"
]
female_patronymics = [
    "Олександрівна", "Михайлівна", "Сергіївна", "Іванівна",
    "Володимирівна", "Павлівна", "Анатоліївна", "Юріївна",
    "Андріївна", "Петрівна"
]


def generate_employee_data(gender):
    first_name = fake.first_name_male() if gender == 'male' else fake.first_name_female()
    last_name = fake.last_name()
    patronymic = random.choice(male_patronymics) if gender == 'male' else random.choice(female_patronymics)
    birth_date = fake.date_of_birth(minimum_age=16, maximum_age=85)
    position = fake.job()
    city = fake.city()
    address = fake.address()
    phone = fake.phone_number()
    email = fake.email()

    return [
        last_name, first_name, patronymic,
        'Чоловіча' if gender == 'male' else 'Жіноча',
        birth_date, position, city, address, phone, email
    ]


def save_to_csv(filename, num_records):
    num_male = int(num_records * 0.6)  # 60% чоловіків
    num_female = num_records - num_male  # 40% жінок

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Прізвище', 'Ім’я', 'По-батькові', 'Стать', 'Дата народження',
            'Посада', 'Місто проживання', 'Адреса проживання', 'Телефон', 'Email'
        ])

        for _ in range(num_male):
            writer.writerow(generate_employee_data('male'))

        for _ in range(num_female):
            writer.writerow(generate_employee_data('female'))


# Generate 2000 records and save to 'employees.csv'
save_to_csv('employees.csv', 2000)
