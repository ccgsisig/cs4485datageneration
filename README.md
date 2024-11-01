# CS 4485 AG Team 7 Repository - Data Generation

### Team Members

- Sisi Aarukapalli (SXA200073@utdallas.edu)
- Aarian Ahsan (ATA200003@utdallas.edu)
- Riyasat Rashid (RXR190059@utdallas.edu)
- Edgar Lara Sanchez (EXL1900014@utdallas.edu)
- Korbin Schulz (KKS200002@utdallas.edu)
- Luigi Victorelli (LBV210000@utdallas.edu)

### Summary
The goal of this project is to design and implement a data pipeline that generates data and stores it in CSV format for analysis and processing. It will involve the generation, storage, and transfer of data using pipelines, as well as exclude more advanced features like database sharding but may use basic data management techniques. This project aims to showcase the following items: 
- **Performance:** *The system should generate and transfer 1 GB of data within 30 minutes.*
- **Security:** *Data transfer should occur over secure protocols such as HTTPS.*
- **Usability:** *The system should provide a simple command-line interface for easy operation.*
- **Reliability:** *The system must ensure no data loss during transfer with 99.9% uptime.*
- **Maintainability:** *The codebase should be modular and well-documented to ensure ease of future development and updates.*

### Functional Requrements 
- **Synthetic Data**
  - The system will generate synthetic data based on a pre-defined schema.
  - Status: *Pending Completion*

- **Exporting**
  - The system will export the generated data into CSV files.
  - Status: *Pending Completion*
 
- **Storage**
  - The system will transfer generated CSV files to a specified storage location (local or cloud).
  - Status: *Pending Complete*

- **Debugging**
  - The system will provide basic error logging and reporting capabilities.
  - Status: *Pending Complete*

### Integration Guide
- We made a Python module that includes fake generated data.
- The other teams need to contact us if they are ready to integrate with our use case.
- Once contacted, we provide the necessary files to the team with the guide of how to integrate with our files.

### Starting Up Project
To start up backend (FastAPI): 
  - Start up venv 
  - Run --> 'pip install -r requirements.txt'
  - Run --> 'uvicorn main:app --reload'

To start up frontend (Vite (react)): 
  - 'npm install'
  - 'npm run dev'

Backend: http://localhost:8000 (API endpoint)

Frontend: http://localhost:5173 (React app)
