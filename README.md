# Sudan News Summarization and Analysis Automation

## Project Description

This project automates the process of gathering, processing, and summarizing news content related to Sudan. It uses email handling, PDF processing, web content fetching, and AI-powered summarization to keep up-to-date with specific topics, such as political events or regional developments. The system checks an email inbox for specific news sweep emails, extracts PDF attachments and links, converts web content to PDFs, and uses OpenAI's API to generate detailed summaries, which are then emailed to a specified recipient.

## Components

- **Email Handling (`imaplib`, `smtplib`):** Manages the retrieval and sending of emails, specifically targeting emails with certain subjects and handling PDF attachments.
- **PDF Processing (`fitz`, `requests`, `pdfkit`):** Handles the extraction of links from PDFs, fetches web content, and converts it to PDF format.
- **AI-Powered Summarization (`openai`):** Leverages OpenAI's API to generate detailed summaries of the news content in a bullet-point format.
- **Logging (`logging`):** Provides a logging mechanism to record events and errors for debugging and monitoring purposes.

## Workflow

1. **Email Retrieval and Processing:**
   - Connects to an email server (IMAP).
   - Searches for emails with a specific subject.
   - Extracts PDF attachments and fetches linked content.

2. **Content Summarization:**
   - Processes fetched content and generates additional PDFs as needed.
   - Summarizes the content using OpenAI's API, focusing on recent events in Sudan.

3. **Email Dispatch:**
   - Sends the generated summary to a specified email address.
   - Formats the email content appropriately.

## Requirements

- Python 3.x
- Libraries: `imaplib`, `email`, `os`, `smtplib`, `fitz`, `requests`, `pdfkit`, `uuid`, `datetime`, `openai`, `dotenv`
- OpenAI API key
- SMTP and IMAP server configuration (Outlook)
- Environment variables for email and API credentials

## Setup and Usage

1. **Environment Setup:**
   - Configure environment variables in a `.env` file.
   - Install necessary Python libraries.

2. **Execution:**
   - Run the main script to start the automated process.
   - Can be scheduled to run periodically using task schedulers.

## Logging and Error Handling

- Logs are maintained for monitoring and troubleshooting.

## Security

- Environment variables are used for sensitive data.
- Ensure `.env` file and log files are excluded from source control and secured.

## Note

- Configured for Outlook; adjust for other email services as needed.
- Assumes specific email subjects and content formats; may require script adjustments for variations.
