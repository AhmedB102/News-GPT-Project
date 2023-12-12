# pdf_processor.py
import fitz
import requests
import pdfkit
import uuid
from datetime import datetime
import os
import openai
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")


# Function to extract links from the PDF
def extract_links_from_pdf(pdf_path):
    links = []
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            links.extend(page.get_links())
    return [link["uri"] for link in links if link["uri"].startswith("http")]


# Function to fetch the content from URLs and convert to PDF
def fetch_and_convert_to_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Convert the HTML to PDF
        pdf_content = pdfkit.from_url(url, False, configuration=config)
        return pdf_content
    else:
        print(f"Failed to fetch {url}")
        return None


# Function to process the PDF, extract links, and update the assistant
def process_pdf_and_update_assistant(pdf_path):
    # Initialize the OpenAI client
    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        organization=os.getenv("OPENAI_ORGANISATION_ID"),
    )

    # Upload the initial PDF and add its ID to the file_ids list
    with open(pdf_path, "rb") as pdf_file:
        initial_file = client.files.create(file=pdf_file, purpose="assistants")
    file_ids = [initial_file.id]

    # Extract links and process them
    links = extract_links_from_pdf(pdf_path)
    for url in links[1:]:
        try:
            pdf_content = fetch_and_convert_to_pdf(url)
            if pdf_content:
                domain_name = url.split("//")[-1].split("/")[0].replace("www.", "")
                base_domain_name = domain_name.split(".")[0]
                unique_id = uuid.uuid4()
                timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M")
                output_pdf_path = f"{base_domain_name}_{unique_id}_{timestamp}.pdf"

                with open(output_pdf_path, "wb") as pdf_file:
                    pdf_file.write(pdf_content)

                with open(output_pdf_path, "rb") as pdf_file:
                    response = client.files.create(file=pdf_file, purpose="assistants")
                    file_ids.append(response.id)
                
                os.remove(output_pdf_path)
        except Exception as e:
            print(e)

    

    # Update the assistant with the new file
    client.beta.assistants.update(
        assistant_id=os.getenv("ASSISTANT_ID"), file_ids=file_ids[:19]
    )


# This function can now be imported and called from another script
