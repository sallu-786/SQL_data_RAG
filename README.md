Flask Chatbot and Data Management App


This repository contains a Flask application that serves as a chatbot interface and data management system, integrating Azure OpenAI for chat responses and SQLite for database operations. The app is designed to handle chat interactions, log conversations, and manage data entries through a REST API.


Features


Chatbot Interface: Interact with the chatbot powered by Azure OpenAI.
Data Management: Perform CRUD operations on a SQLite database.
Logging: Save and download chat logs in Excel format.
Authentication: Basic authentication for accessing certain routes.

Installation:


1. Clone the repository:


     git clone https://github.com/yourusername/flask-chatbot-app.git
     cd flask-chatbot-app


2. Create and activate a virtual environment:


     python -m venv my_env
     my_env/Scripts/activate #activate virtual environment on windows
3. Install dependencies:


     pip install -r requirements.txt


4. Set up environment variables:


     Create a .env file in the project root and add your Azure OpenAI credentials:
     AZURE_OPENAI_ENDPOINT=your_endpoint     #if you dont have Azure Open Ai API and want to use local model please check my repository at: 
     AZURE_OPENAI_API_KEY=your_api_key


5. Run the application:


     python app.py
