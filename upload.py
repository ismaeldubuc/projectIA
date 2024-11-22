import os
import PyPDF2
import re
import boto3
from io import BytesIO
from botocore.exceptions import ClientError
import yaml
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def load_config():
    with open("config.yaml", 'r') as file:
        return yaml.safe_load(file)

def get_pdf_from_s3(bucket_name, pdf_key, region_name):
    """Download PDF file from S3 and return it as BytesIO object"""
    # Vérifier que les credentials sont présents
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials not found in environment variables")
        
    try:
        s3_client = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        response = s3_client.get_object(Bucket=bucket_name, Key=pdf_key)
        return BytesIO(response['Body'].read())
    except ClientError as e:
        print(f"Error downloading file from S3: {e}")
        return None

def convert_pdf_to_text():
    # Load configuration
    config = load_config()
    aws_config = config.get('aws', {})
    
    # Get PDF from S3
    pdf_file = get_pdf_from_s3(
        aws_config['bucket_name'],
        aws_config['pdf_key'],
        aws_config['region_name']
    )
    
    if pdf_file:
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            text = ''
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                if page.extract_text():
                    text += page.extract_text() + " "
            
            # Normalize whitespace and clean up text
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Split text into chunks by sentences
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 1000:
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
                    
            if current_chunk:
                chunks.append(current_chunk)
                
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")
                    
            print(f"PDF content from S3 has been appended to vault.txt")
            
        except Exception as e:
            print(f"Error processing PDF: {e}")
    else:
        print("Failed to retrieve PDF from S3")

if __name__ == "__main__":
    convert_pdf_to_text()