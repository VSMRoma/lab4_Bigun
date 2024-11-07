import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Function to categorize the age of employees
def age_category(age):
    if age < 18:
        return 'younger_18'
    elif 18 <= age <= 45:
        return '18-45'
    elif 45 < age <= 70:
        return '45-70'
    else:
        return 'older_70'

# Function to analyze the CSV file and generate plots
def analyze_csv(csv_filename):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_filename, encoding='utf-8')
    except FileNotFoundError:
        print("Повідомлення про відсутність або проблеми при відкритті файлу CSV")
        return

    print("Ok")

    # Gender distribution pie chart
    gender_counts = df['Стать'].value_counts()
    print(gender_counts)
    gender_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title('Статевий розподіл')
    plt.show()

    # Calculate age and categorize based on the date of birth
    df['Дата народження'] = pd.to_datetime(df['Дата народження'], errors='coerce')
    df['Вік'] = df['Дата народження'].apply(
        lambda x: datetime.now().year - x.year - ((datetime.now().month, datetime.now().day) < (x.month, x.day))
    )
    df['Категорія'] = df['Вік'].apply(age_category)

    # Age category distribution bar chart
    category_counts = df['Категорія'].value_counts()
    print(category_counts)
    category_counts.plot(kind='bar')
    plt.title('Кількість працівників за віковими категоріями')
    plt.show()

    # Gender distribution within each age category
    for category in ['younger_18', '18-45', '45-70', 'older_70']:
        sub_df = df[df['Категорія'] == category]
        gender_category_counts = sub_df['Стать'].value_counts()
        print(f"Категорія {category}:")
        print(gender_category_counts)
        gender_category_counts.plot(kind='bar')
        plt.title(f'Статевий розподіл у категорії {category}')
        plt.show()

# Call the function to analyze the data
analyze_csv('employees.csv')
