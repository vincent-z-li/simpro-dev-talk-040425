import os
from api.services.ingest_service import ingest_documents

if __name__ == "__main__":
    data_dir = "./data/guides"
    if not os.path.exists(data_dir):
        print(f"Creating data directory: {data_dir}")
        os.makedirs(data_dir, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
    if not pdf_files:
        print(f"No PDF files found in {data_dir}")
        print("Please add PDF files to continue")
    else:
        print(f"Found {len(pdf_files)} PDF files: {pdf_files}")
        print("Ingesting documents...")
        success = ingest_documents(data_dir)
        if success:
            print("Documents ingested successfully!")
        else:
            print("Failed to ingest documents")