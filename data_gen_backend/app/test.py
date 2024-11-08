from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import csv
import random
import json
from faker import Faker
import time
import os
from threading import Thread
from kafka import KafkaProducer
from kafka.errors import KafkaError
import uvicorn

fake = Faker()

app = FastAPI()

# CORS (Cross origin resource sharing) middleware to allow requests from the react app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kafka Configuration
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "data_topic")

# Initialize Kafka Producer with updated serializer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
    retries=5  # Retry up to 5 times on failure
)

# Define your fake data generation functions ensuring JSON serialization
fake_functions = {
    'int': lambda: random.randint(1000, 9999),
    'datetime': lambda: fake.date_time_between(start_date='-2y', end_date='now').isoformat(),
    'nullable_datetime': lambda: fake.date_time_between(start_date='-2y', end_date='now').isoformat() if random.choice([True, False]) else None,
    'version': lambda: random.randint(1, 100),
    'status': lambda: fake.word(ext_word_list=["active", "inactive", "pending"]),
    'name': lambda: fake.name(),
    'email': lambda: fake.email(),
    'word': lambda: fake.word(),
    'address': lambda: fake.address(),
    'phone': lambda: fake.phone_number(),
    # General-purpose data
    'uuid': lambda: fake.uuid4(),  # UUID
    'string': lambda: fake.word(),  # General string
    'timestamp': lambda: fake.date_time_between(
        start_date='-2y', end_date='now'
    ).strftime('%Y-%m-%d %H:%M:%S.%f%z'),  # Timestamp as string
    'iso8601': lambda: fake.iso8601(),  # ISO8601 timestamp as string
    'epoch': lambda: int(fake.unix_time()),  # Epoch timestamp as integer
    'integer': lambda: random.randint(1, 999999),  # General integer
    'float': lambda: round(random.uniform(-180.0, 180.0), 6),  # General float
    'boolean': lambda: random.choice([True, False]),
    
    # User-related data
    'user_id': lambda: fake.uuid4(),
    'user_ip': lambda: fake.ipv4(),
    'user_name': lambda: fake.name(),
    'user_role': lambda: fake.word(ext_word_list=["tenant", "admin", "operator"]),
    'user_email': lambda: fake.email(),
    
    # Action-related data
    'action_type': lambda: fake.word(ext_word_list=["DELETE", "CREATE", "UPDATE", "READ"]),
    
    # Object-related data
    'object_id': lambda: fake.uuid4(),
    'object_name': lambda: fake.word(),
    'object_type': lambda: fake.word(ext_word_list=["radio", "gateway"]),
    'object_model': lambda: fake.word(ext_word_list=["Indoor", "Outdoor"]),
    'object_status': lambda: fake.word(ext_word_list=["MARKED_FOR_DELETE", "ACTIVE", "INACTIVE"]),
    'object_description': lambda: f"{fake.word()} description",
    
    # Old Object-related data
    'old_object_id': lambda: fake.uuid4(),
    'old_object_name': lambda: fake.word(),
    'old_object_type': lambda: fake.word(),
    
    # Edge-related data
    'edge_id': lambda: fake.uuid4(),
    'edge_name': lambda: fake.word(),
    'edge_type': lambda: fake.word(ext_word_list=["PRIVATE_CELLULAR", "CARRIER_GATEWAY"]),
    'edge_ipsec_mode': lambda: fake.word(ext_word_list=["CERTIFICATE", "PSK"]),
    
    # Carrier-related data
    'carrier_id': lambda: fake.uuid4(),
    'carrier_name': lambda: f"{fake.company()} Operator",
    
    # Certificate-related data
    'ca_cert': lambda: "-----BEGIN CERTIFICATE-----\n" + fake.sha256() + "\n-----END CERTIFICATE-----",
    'ipsec_key': lambda: "-----BEGIN RSA PRIVATE KEY-----\n" + fake.sha256() + "\n-----END RSA PRIVATE KEY-----",
    'ipsec_cert': lambda: "-----BEGIN CERTIFICATE-----\n" + fake.sha256() + "\n-----END CERTIFICATE-----",
    
    # Location-related data
    'location_name': lambda: fake.city(),
    'location_tags': lambda: [fake.word() for _ in range(random.randint(1, 3))] if random.choice([True, False]) else None,
    'location_zoom': lambda: random.randint(1, 20),
    'location_latitude': lambda: round(fake.latitude(), 6),
    'location_longitude': lambda: round(fake.longitude(), 6),
    'location_type': lambda: fake.word(ext_word_list=["PRIVATE_CLOUD", "PUBLIC_CLOUD"]),
    'is_managed': lambda: random.choice([True, False]),
    
    # IP-related data
    'ip_pool': lambda: fake.ipv4(network=True),
    'static_ip_start': lambda: fake.ipv4(),
    'static_ip_end': lambda: fake.ipv4(),
    'ip_pool_netmask': lambda: '255.255.255.0',
    'mme_ip': lambda: fake.ipv4(),
    'interface_ip': lambda: fake.ipv4(),
    'right_subnet': lambda: f"{fake.ipv4()}/32",
    'left_source_ip': lambda: '%config',
    
    # Radio group data
    'radio_group_id': lambda: fake.uuid4(),
    'radio_group_name': lambda: fake.word(),
    
    # SAS configuration data
    'sas_enabled': lambda: random.choice([True, False]),
    'cbsd_category': lambda: fake.word(ext_word_list=["A", "B"]),
    'plmn_id': lambda: f"{random.randint(100, 999)}{random.randint(10, 99)}",
    'frequency_selection_logic': lambda: ','.join(random.sample(
        ["Power", "Bandwidth", "Frequency", "Latency"], random.randint(2, 3)
    )),
    
    # Runtime-related data
    'software_version': lambda: f"{random.randint(10, 20)}.{random.randint(0, 99)}.{random.randint(0, 9999)}",
    'runtime_status': lambda: fake.word(ext_word_list=["INACTIVE", "ACTIVE", "REBOOTING"]),
    'uptime': lambda: f"{random.randint(0, 99)}d {random.randint(0, 23)}h {random.randint(0, 59)}m {random.randint(0, 59)}s",
    'health': lambda: fake.word(ext_word_list=["GOOD", "BAD", "MARGINAL"]),
    'tac': lambda: random.randint(1, 999),
    'max_ue': lambda: random.randint(1, 9999),
    'gps_status': lambda: random.choice([True, False]),
    'item_number': lambda: f"{random.randint(1, 10)}",
    
    # Manufacturing data
    'vendor_type': lambda: fake.word(ext_word_list=["AIRSPAN", "NOKIA", "ERICSSON"]),
    'serial_number': lambda: fake.sha1()[:12].upper(),
    'board_number': lambda: f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(100, 999)}",
    'assembly_number': lambda: f"{random.randint(900, 999)}-{random.randint(10, 99)}-{random.randint(400, 499)}",
    'assembly_revision': lambda: random.choice(["A0", "B0", "C1"]),
    'manufacturing_date': lambda: fake.date(pattern="%d:%m:%Y"),
    
    # Security configurations
    'aes_integrity_level': lambda: random.randint(1, 3),
    'null_ciphering_level': lambda: random.randint(0, 2),
    'security_for_ciphering': lambda: fake.word(ext_word_list=["Optional", "Mandatory"]),
    'security_for_integrity': lambda: fake.word(ext_word_list=["Optional", "Mandatory"]),
    'snow3g_integrity_level': lambda: random.randint(1, 3),
    
    # Mobility parameters
    'a1': lambda: random.randint(30, 70),
    'a2': lambda: random.randint(30, 70),
    'a5_t1': lambda: random.randint(30, 70),
    'a5_t2': lambda: random.randint(30, 70),
    'hysteresis': lambda: random.randint(1, 10),
    'time_to_trigger': lambda: random.randint(100, 1000),
    
    # Status and additional info
    'request_status': lambda: fake.word(ext_word_list=["ACCEPTED", "REJECTED", "PENDING"]),
    'eci_auto_assign': lambda: random.choice([True, False]),
    'signature': lambda: fake.sha256(),
    'subframe_assignment': lambda: random.randint(0, 10),
    'special_subframe_pattern': lambda: random.randint(0, 10),
    'status_message': lambda: fake.sentence(),
    'install_certification_time': lambda: fake.iso8601(),
}

# Function to generate data based on the JSON schema
def generate_data(schema, num_records):
    data = []
    for _ in range(num_records):
        row = generate_record(schema)
        data.append(row)
        # Send each record to Kafka
        send_to_kafka(row)
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

def continuous_generation(schema, num_records, interval, output_file):
    while True:
        data = generate_data(schema, num_records)
        save_to_csv(data, output_file)
        time.sleep(interval)

def send_to_kafka(record):
    try:
        producer.send(KAFKA_TOPIC, value=record)
    except KafkaError as e:
        # Handle Kafka errors (e.g., log them)
        print(f"Failed to send record to Kafka: {e}")

@app.post("/generate-csv")
async def generate_csv(
    file: UploadFile = File(...),
    num_records: int = Form(...),
    interval: float = Form(...),
    mode: str = Form(...),
    custom_filename: str = Form(default="output")
):
    schema_data = await file.read()
    try:
        schema = json.loads(schema_data)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON file."}

    # Check that directory exists
    os.makedirs('generated_files', exist_ok=True)

    # Naming convention for the generated CSV file
    original_filename = file.filename.split('.')[0]  # Get the base name without extension
    output_file = f"generated_files/{custom_filename}.csv"
    interval_seconds = interval * 60  # minutes to seconds

    if mode == "stream":
        # Start continuous generation in a background thread
        thread = Thread(target=continuous_generation, args=(schema, num_records, interval_seconds, output_file), daemon=True)
        thread.start()
        return {
            "message": "CSV generation started in streaming mode!",
            "output_file": os.path.basename(output_file)  # Only send the filename
        }
    elif mode == "batch":
        data = generate_data(schema, num_records)  # Generate data immediately
        save_to_csv(data, output_file)
        return {
            "message": "CSV generated successfully!",
            "output_file": os.path.basename(output_file)  # Only send the filename
        }
    else:
        return {"error": "Invalid mode. Use 'batch' or 'stream'."}

@app.get("/download_csv/")
async def download_csv(filename: str):
    file_path = f"generated_files/{filename}" 
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='text/csv', filename=filename)
    return {"error": "File not found."}

@app.on_event("shutdown")
def shutdown_event():
    # Ensure all messages are sent before shutdown
    producer.flush()
    producer.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Command to run:
# uvicorn your_module_name:app --reload
