from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Email Configuration 
SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Function to dynamically generate a response based on the query

def generate_response(query):
    query = query.lower()  
    
    if 'flask' in query:
        return "Flask is a micro web framework for Python. It's great for building web applications!"
    elif 'python' in query:
        return "Python is a high-level programming language known for its readability and simplicity."
    elif 'weather' in query:
        return "I can provide weather updates, but you need to integrate an external API for real-time data."
    else:
        return f"Sorry, I don't understand the query: '{query}'. Please try asking something else."

# Route to handle POST requests
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({'error': 'Invalid payload. Please provide a query.'}), 400

    query = data['query']
    response = generate_response(query)

    # Send the email
    try:
        send_email(query, response)
        return jsonify({'message': 'Email sent successfully!', 'query': query, 'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to send an email
def send_email(query, response):
    # Compose the email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  # You can send it to yourself or someone else
    msg['Subject'] = 'Query Response from Webhook'

    # Email body
    body = f"Query: {query}\n\nResponse: {response}"
    msg.attach(MIMEText(body, 'plain'))

    # Send email via SMTP
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
