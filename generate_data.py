import argparse
import csv
import random
import json
from faker import Faker
import time

fake = Faker()

# Mapping field types from JSON to corresponding Faker functions
fake_functions = {
    'int': lambda: random.randint(1000, 9999),
    'datetime': lambda: fake.date_time_between(start_date='-2y', end_date='now'),
    'nullable_datetime': lambda: fake.date_time_between(start_date='-2y', end_date='now') if random.choice(
        [True, False]) else None,
    'version': lambda: random.randint(1, 100),
    'status': lambda: fake.word(ext_word_list=["active", "inactive", "pending"]),
    'name': lambda: fake.name(),
    'email': lambda: fake.email(),
    'word': lambda: fake.word(),
    'address': lambda: fake.address(),
    'phone': lambda: fake.phone_number()  
}


# Function to generate data based on the JSON schema
def generate_data(schema, num_records):
    data = []

    for _ in range(num_records):
        row = generate_record(schema)
        data.append(row)

    return data

def generate_record(schema):
    row = {}
    for column, field_type in schema.items():
        if isinstance(field_type, str):
            if field_type in fake_functions:
                row[column] = fake_functions[field_type]()  #Generate data uisng faker functions
            else:
                raise ValueError(f"Unknown field type '{field_type}' in schema for column '{column}'")
        
        elif isinstance(field_type, dict):  #dictionary check
            row[column] = generate_record(field_type)  # Recursive call to generate data for nested dictionary

        elif isinstance(field_type, list):  #list check
            row[column] = []
            for _ in range(random.randint(1, 3)):  #generate a random number of records
                row[column].append(generate_record(field_type[0]))  #Assume the first item in the list defines the schema, could change 
            
        else:
            raise ValueError(f"Unsupported field type for column '{column}': {field_type}")
    
    return row


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
    parser = argparse.ArgumentParser(description="Generate fake data from a JSON schema and save to CSV.")
    parser.add_argument('schema', type=str, help='Path to the JSON schema file')
    parser.add_argument('output', type=str, help='The output CSV file name')
    args = parser.parse_args()

    # Load schema from JSON file
    try:
        with open(args.schema, 'r') as file:
            schema = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{args.schema}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: File '{args.schema}' is not a valid JSON file.")
        return

    # Ask how many records the user wants
    try:
        num_records = int(input(f"How many records do you want to generate? "))
    except ValueError:
        print("Please enter a valid number.")
        return
    
    # Ask for the time interval in minutes
    try:
        interval = float(input(f"Enter the time interval between each generation (in minutes): ")) * 60  # Convert minutes to seconds
    except ValueError:
        print("Please enter a valid time interval.")
        return

    print(f"Generating {num_records} records every {interval / 60} minutes...")

    while True:
        try:
            data = generate_data(schema, num_records)
            save_to_csv(data, args.output)
            time.sleep(interval)  # Sleep for the specified interval
        except ValueError as e:
            print(e)
            break

    # Save the data to CSV
    save_to_csv(data, args.output)


if __name__ == "__main__":
    main()