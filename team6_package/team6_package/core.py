from faker import Faker
import random
import csv
import json
import io  # For in-memory CSV handling

fake = Faker()

# Mapping field types to Faker functions
fake_functions = {
    'uuid': lambda: fake.uuid4(),  # UUID
    'boolean': lambda: random.choice([True, False]),
    'integer': lambda: random.randint(1, 999999),  # General integer
    'iso8601': lambda: fake.iso8601(),  # ISO8601 timestamp
    'float': lambda: round(random.uniform(-180.0, 180.0), 6),  # General float
    'datetime': lambda: fake.date_time_between(start_date='-2y', end_date='now'),
    'nullable_datetime': lambda: fake.date_time_between(start_date='-2y', end_date='now') if random.choice([True, False]) else None,
    'status': lambda: fake.word(ext_word_list=["active", "inactive", "pending"]),
    'name': lambda: fake.name(),
    'email': lambda: fake.email(),
    'word': lambda: fake.word(),
    'address': lambda: fake.address(),
    'id': lambda: fake.uuid4(),
    'application_type': lambda: random.choice([
        "Streaming", "Gaming", "Browsing",
        "Social Media", "Video Call",
        "Email", "E-commerce"
    ]),
    'signal_strength': lambda: random.randint(-120, -40),
    'latency': lambda: random.randint(10, 1000),
    'required_bandwidth': None,  # Handled in generate_data
    'allocated_bandwidth': lambda required: random.randint(int(required * 0.5), required),
    'resource_allocation': lambda: random.randint(1, 100),  # Percentage

    'user_role': lambda: fake.word(ext_word_list=["tenant", "admin", "operator"]),

    'action_type': lambda: fake.word(ext_word_list=["DELETE", "CREATE", "UPDATE", "READ"]),

    # Object-related data
    'object_type': lambda: fake.word(ext_word_list=["radio", "gateway"]),
    'object_model': lambda: fake.word(ext_word_list=["Indoor", "Outdoor"]),
    'object_status': lambda: fake.word(ext_word_list=["MARKED_FOR_DELETE", "ACTIVE", "INACTIVE"]),
    'object_description': lambda: f"{fake.word()} description",

    'carrier_name': lambda: fake.word(ext_word_list=["T-Mobile", "AT&T", "Verizon", "Cricket", "Sprint", "Mint"]),
    'ip': lambda: fake.ipv4(),


    # Edge-related data
    'edge_type': lambda: fake.word(ext_word_list=["PRIVATE_CELLULAR", "CARRIER_GATEWAY"]),
    'edge_ipsec_mode': lambda: fake.word(ext_word_list=["CERTIFICATE", "PSK"]),

    # Certificate-related data
    'cert': lambda: "-----BEGIN CERTIFICATE-----\n" + fake.sha256() + "\n-----END CERTIFICATE-----",
    'ipsec_key': lambda: "-----BEGIN RSA PRIVATE KEY-----\n" + fake.sha256() + "\n-----END RSA PRIVATE KEY-----",

    # SAS configuration data
    'cbsd_category': lambda: fake.word(ext_word_list=["A", "B"]),
    'plmn_id': lambda: f"{random.randint(100, 999)}{random.randint(10, 99)}",
    'frequency_selection_logic': lambda: ','.join(random.sample(
        ["Power", "Bandwidth", "Frequency", "Latency"], random.randint(2, 3)
    )),

    # Runtime-related data
    'software_version': lambda: f"{random.randint(10, 20)}.{random.randint(0, 99)}.{random.randint(0, 9999)}",
    'runtime_status': lambda: fake.word(ext_word_list=["INACTIVE", "ACTIVE", "REBOOTING"]),
    'tac': lambda: random.randint(1, 999),
    'max_ue': lambda: random.randint(1, 9999),

    # Security configurations
    'aes_integrity_level': lambda: random.randint(1, 3),
    'null_ciphering_level': lambda: random.randint(0, 2),
    'security_for_ciphering': lambda: fake.word(ext_word_list=["Optional", "Mandatory"]),
    'security_for_integrity': lambda: fake.word(ext_word_list=["Optional", "Mandatory"]),
    'snow3g_integrity_level': lambda: random.randint(1, 3),

    # Manufacturing data
    'serial_number': lambda: fake.sha1()[:12].upper(),
    'board_number': lambda: f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(100, 999)}",
    'assembly_number': lambda: f"{random.randint(900, 999)}-{random.randint(10, 99)}-{random.randint(400, 499)}",
    'assembly_revision': lambda: random.choice(["A0", "B0", "C1"]),
    'manufacturing_date': lambda: fake.date_between(start_date='-5y', end_date='today'),  

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

    # Location-related data
    'location_name': lambda: fake.city(),
    'location_tags': lambda: [fake.word() for _ in range(random.randint(1, 3))] if random.choice([True, False]) else None,
    'location_zoom': lambda: random.randint(1, 20),
    'location_type': lambda: fake.word(ext_word_list=["PRIVATE_CLOUD", "PUBLIC_CLOUD"]),
    'is_managed': lambda: random.choice([True, False]),
    'location_latitude': lambda: round(fake.latitude(), 6),
    'location_longitude': lambda: round(fake.longitude(), 6),
    'uptime': lambda: f"{random.randint(0, 99)}d {random.randint(0, 23)}h {random.randint(0, 59)}m {random.randint(0, 59)}s",
    'health': lambda: fake.word(ext_word_list=["GOOD", "BAD", "MARGINAL"])
}

def generate_data(schema, num_records):
    """Generate a list of dictionaries based on the JSON schema."""
    data = []
    for _ in range(num_records):
        row = {}
        for column, field_type in schema.items():
            field_type_lower = field_type.lower()
            
            if field_type_lower == 'required_bandwidth':
                # Custom logic for required_bandwidth
                app_type = row.get('application_type', None)
                if app_type in ["Browsing", "Email"]:
                    row[column] = random.randint(5, 20)
                elif app_type in ["Social Media", "E-commerce"]:
                    row[column] = random.randint(20, 50)
                else:  # Streaming, Gaming, Video Call
                    row[column] = random.randint(50, 200)
            
            elif field_type_lower == 'allocated_bandwidth':
                # Use the value of required_bandwidth to generate allocated_bandwidth
                required_bw = row.get('required_bandwidth', 50)
                row[column] = fake_functions['allocated_bandwidth'](required_bw)
            
            elif field_type_lower in fake_functions:
                # Use the corresponding Faker function
                row[column] = fake_functions[field_type_lower]()
            
            else:
                # Default to generating a word if the type is unknown
                row[column] = fake_functions['word']()
        
        data.append(row)
    return data

def save_to_csv(data, output_file=None):
    """
    Save data to a CSV file. 
    If `output_file` is None, return the CSV content as a StringIO object.
    """
    if not data:
        raise ValueError("No data to save.")

    fieldnames = data[0].keys()
    csv_buffer = io.StringIO()  # Create an in-memory string buffer

    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

    if output_file:
        with open(output_file, 'w', newline='') as file:
            file.write(csv_buffer.getvalue())
        print(f"Data saved to {output_file}")
    else:
        csv_buffer.seek(0)  # Reset buffer position to the beginning
        return csv_buffer  # Return the in-memory CSV object

def load_schema(schema_path):
    """Load the JSON schema from a file."""
    with open(schema_path, 'r') as file:
        return json.load(file)