import argparse
import csv
import random
from faker import Faker

fake = Faker()

# Define schemas for each table
# For other/future tables can just add here following similar format
table_schemas = {
    'db_infos': {
        'id': lambda: random.randint(1000, 9999),
        'created_at': lambda: fake.date_time_between(start_date='-2y', end_date='now'),
        'updated_at': lambda: fake.date_time_between(start_date='-2y', end_date='now'),
        'deleted_at': lambda: fake.date_time_between(start_date='-2y', end_date='now') if random.choice([True, False]) else None,
        'version': lambda: random.randint(1, 100),
        'status': lambda: fake.word(ext_word_list=["active", "inactive", "pending"])
    }
    # You can add more tables here with a similar structure
}

# List of available tables
table_names = list(table_schemas.keys())

# Function to display the tables and let the user select one
def select_table():
    print("Select a table to generate data for:")
    for i, table in enumerate(table_names):
        print(f"{i + 1}. {table}")

    while True:
        try:
            choice = int(input("Enter the number of the table: ")) - 1
            if 0 <= choice < len(table_names):
                return table_names[choice]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

# Function to generate data based on selected table schema
def generate_data(table_name, num_records):
    schema = table_schemas[table_name]
    data = []

    for _ in range(num_records):
        row = {column: generator() for column, generator in schema.items()}
        data.append(row)

    return data

# Function to save generated data to a CSV file
def save_to_csv(data, output_file):
    if data:
        fieldnames = data[0].keys()
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"Data saved to {output_file}")
    else:
        print("No data to save.")

def main():
    parser = argparse.ArgumentParser(description="Generate fake data for a table and save to CSV.")
    parser.add_argument('output', type=str, help='The output CSV file name')
    args = parser.parse_args()

    # Step 1: Select a table
    table_name = select_table()

    # Step 2: Ask how many records the user wants
    num_records = int(input(f"How many records do you want to generate for {table_name}? "))

    # Step 3: Generate data
    data = generate_data(table_name, num_records)

    # Step 4: Save the data to CSV
    save_to_csv(data, args.output)

if __name__ == "__main__":
    main()
