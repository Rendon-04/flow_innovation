# Backend  

This folder contains the backend implementation for the project. It serves as the foundation for API integrations, data management, and server-side logic, supporting key features of the overall application.  

## Overview  
The backend is developed using Python and Flask, powering essential features such as:  
- Fact-checking using the Google Fact Checker API.  
- Delivering an innovation and progress news feed.  
- Providing APIs for educational tools and resources to inspire creativity and development.  

The backend was primarily designed and developed by **Bamidele Israel Anuoluwatomiwa**, with the possibility of future contributions from collaborators.  

## Features  
- **Fact-Checking API Integration**: Validates claims by interacting with external APIs.  
- **Innovation News Feed**: Provides updates and curated content to inspire progress.  
- **Educational Resources**: Supplies learning tools and recommendations for fostering innovation.  

## Technology Stack  
- **Language**: Python  
- **Framework**: Flask  
- **Database**: SQLite (can be replaced if necessary)  
- **Environment Variables**: Uses a `.env` file for API keys and configurations.  

## Running the Backend  
Follow these steps to set up and run the backend service:  

1. Navigate to the backend folder:  
   ```bash  
   cd backend  

	2.	Set up a virtual environment:

python -m venv venv  
source venv/bin/activate  # For Linux/Mac  
venv\Scripts\activate     # For Windows  


	3.	Install dependencies:

pip install -r requirements.txt  


	4.	Configure environment variables:
Create a .env file in this folder with the following:

GOOGLE_API_KEY=your-google-fact-checker-api-key  
DATABASE_URL=sqlite:///app.db  


	5.	Run the server:

flask run  



The backend will now be accessible at http://127.0.0.1:5000.

Folder Structure

backend/  
├── __init__.py        # Backend initialization  
├── routes/            # API route definitions  
├── models.py          # Database models  
├── utils.py           # Helper functions  
├── services/          # External API integrations  
├── migrations/        # Database migration scripts  
├── tests/             # Test cases  
└── requirements.txt   # Python dependencies  

License

This project is licensed under the MIT License.

Contact

For any issues or feedback related to the backend:
	•	Lead Developer: Bamidele Israel Anuoluwatomiwa
	•	Email: bamideleisrael04@icloud.com