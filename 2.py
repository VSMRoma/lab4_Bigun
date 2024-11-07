import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Define the function to categorize age
def age_category(age):
    if age < 18:
        return 'younger_18'
    elif 18 <= age <= 45:
        return '18-45'
    elif 45 < age <= 70:
        return '45-70'
    else:
        return 'older_70'

# Define the function to categorize employees and create Excel sheets
def categorize_employees(csv_filename, xlsx_filename):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_filename, encoding='utf-8')
    except FileNotFoundError:
        print("Повідомлення про відсутність або проблеми при відкритті файлу CSV")
        return
    except pd.errors.EmptyDataError:
        print("Файл CSV порожній")
        return
    except Exception as e:
        print(f"Помилка при відкритті файлу CSV: {str(e)}")
        return

    # Convert the 'Дата народження' column to datetime format
    df['Дата народження'] = pd.to_datetime(df['Дата народження'], errors='coerce')

    # Calculate the age of each employee
    df['Вік'] = df['Дата народження'].apply(
        lambda x: datetime.now().year - x.year - ((datetime.now().month, datetime.now().day) < (x.month, x.day))
    )

    # Apply the age category function to each employee's age
    df['Категорія'] = df['Вік'].apply(age_category)

    try:
        # Write to an Excel file with multiple sheets
        with pd.ExcelWriter(xlsx_filename, engine='openpyxl') as writer:
            df.index += 1
            df.index.name = 'No'
            df.to_excel(writer, sheet_name='all', index=True)

            # Write separate sheets based on the age category
            df[df['Категорія'] == 'younger_18'].to_excel(writer, sheet_name='younger_18', index=True)
            df[df['Категорія'] == '18-45'].to_excel(writer, sheet_name='18-45', index=True)
            df[df['Категорія'] == '45-70'].to_excel(writer, sheet_name='45-70', index=True)
            df[df['Категорія'] == 'older_70'].to_excel(writer, sheet_name='older_70', index=True)

        print("Ok")
    except Exception as e:
        print("Повідомлення про неможливість створення XLSX файлу:", str(e))

# Call the function with the given filenames
categorize_employees('employees.csv', 'employees.xlsx')
