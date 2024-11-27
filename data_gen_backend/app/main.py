from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import csv
import random
import json
import os
import asyncio
from faker import Faker

# Import the factory function to create introspectors
from introspectors.factory import create_introspector
fake = Faker()

app = FastAPI()

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIRECTORY = os.path.join(BASE_DIR, "generated_files")
os.makedirs(CSV_DIRECTORY, exist_ok=True)  # Ensure the directory exists

# CORS middleware to allow requests from the React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_functions = {
    'int': lambda: random.randint(1000, 9999),
    'datetime': lambda: fake.date_time_between(start_date='-2y', end_date='now'),
    'nullable_datetime': lambda: fake.date_time_between(start_date='-2y', end_date='now') if random.choice([True, False]) else None,
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
                row[column] = fake_functions[field_type]()
            else:
                raise ValueError(f"Unknown field type '{field_type}' in schema for column '{column}'")
        elif isinstance(field_type, dict):
            row[column] = generate_record(field_type)  # Recursive call for nested dictionary
        elif isinstance(field_type, list):
            row[column] = [generate_record(field_type[0]) for _ in range(random.randint(1, 3))]
        else:
            raise ValueError(f"Unsupported field type for column '{column}': {field_type}")
    return row

def save_to_csv(data, output_file):
    if data:
        fieldnames = data[0].keys()
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    else:
        raise ValueError("No data to save.")



async def continuous_generation(schema, num_records, interval, output_file):
    try:
        while True:
            data = generate_data(schema, num_records)
            save_to_csv(data, output_file)
            await asyncio.sleep(interval)  # Use asyncio.sleep to avoid blocking
    except Exception as e:
        print(f"Error during data generation: {e}")

# Initialize Introspector using the factory function
try:
    inspector = create_introspector('csv', directory_path=CSV_DIRECTORY)
except ValueError as ve:
    print(f"Introspector initialization error: {ve}")
    inspector = None  # Handle initialization failure if necessary

@app.post("/generate-csv")
async def generate_csv(file: UploadFile = File(...), num_records: int = Form(...), interval: float = Form(...), mode: str = Form(...), custom_filename: str = Form(default="output")):
    schema_data = await file.read()
    try:
        schema = json.loads(schema_data)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON file."}

    # Check that directory exists
    os.makedirs('generated_files', exist_ok=True)

    # Naming convention for the generated CSV file
    original_filename = file.filename.split('.')[0]  # Get the base name without extension
    output_file = os.path.join(CSV_DIRECTORY, f"{custom_filename}.csv")
    interval_seconds = interval * 60  # minutes to seconds

    if mode == "stream":
        # Start continuous generation
        asyncio.create_task(continuous_generation(schema, num_records, interval_seconds, output_file))
        return {
            "message": "CSV generation started in streaming mode!",
            "output_file": output_file.split('/')[-1]  # Only send the filename
        }
    elif mode == "batch":
        data = generate_data(schema, num_records)  # Generate data immediately
        save_to_csv(data, output_file)
        return {
            "message": "CSV generated successfully!",
            "output_file": output_file.split('/')[-1]  # Only send the filename
        }
    else:
        return {"error": "Invalid mode. Use 'batch' or 'stream'."}

@app.get("/download_csv/")
async def download_csv(filename: str):
    file_path = os.path.join(CSV_DIRECTORY, filename) 
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='text/csv', filename=filename)
    return {"error": "File not found."}

# Introspection Endpoints
@app.get("/introspect/tables")
async def get_csv_tables():
    if inspector is None:
        raise HTTPException(status_code=500, detail="Introspector not initialized.")
    try:
        tables = inspector.get_table_names()
        return {"tables": tables}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/introspect/metadata/{table_name}")
async def get_table_metadata(table_name: str):
    if inspector is None:
        raise HTTPException(status_code=500, detail="Introspector not initialized.")
    try:
        metadata = inspector.get_table_metadata(table_name)
        return {
            "name": metadata.name,
            "row_count": metadata.row_count,
            "columns": metadata.columns,
            "file_path": metadata.file_path
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
