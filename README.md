Python-flask based Retrieval augmented Generation Chatbot and Database Management App


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


3. Create and activate a virtual environment:


     python -m venv my_env


     my_env/Scripts/activate #activate virtual environment on windows

   
4. Install dependencies:


     pip install -r requirement.txt


5. Set up environment variables:


     Create a .env file in the project root and add your Azure OpenAI credentials:

 #if you dont have Azure Open Ai API and want to use local model please check my repository at:  https://github.com/sallu-786/flask_chatbot_local

 
     AZURE_OPENAI_ENDPOINT=your_endpoint

     AZURE_OPENAI_API_KEY=your_api_key


7. Run the application:


     python app.py




Main Page Interface:


   ![image](https://github.com/user-attachments/assets/01ecdebb-6a74-4d1c-8f28-133dc7b48cc4)


Admin Page for Database Management:


![image](https://github.com/user-attachments/assets/1af32e1c-b531-4b8c-add7-9228671c2e97)

Log page for viewing chat log:

![image](https://github.com/user-attachments/assets/8436e86f-286f-4881-8769-893cf982542a)


   

