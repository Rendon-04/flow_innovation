## Backend 🖥

This folder contains the backend implementation for Flow Innovation, a platform designed to combat misinformation and promote progress through AI-powered fact-checking, innovation news, and goal tracking.

## What you'll find here 🏛
1. [Backend Overview](#overview-globe_with_meridians)
2. [Features](#features-star)
3. [Technology Stack](#technology-stack-wrench)
4. [Innovation](#innovation-bulb)
5. [Running the Backend](#running-the-backend)
6. [Folder Structure](#folder-structure)
7. [API Endpoints](#api-endpoints)
8. [Attributions](#attributions)
9. [License](#license)
10.	[Contact Dev](#contact)
11. [Closing Statement](#closing-statement)
    
  
## Overview :globe_with_meridians:

The backend is developed using Python and Flask, serving as the foundation for:
- **AI-Powered Fact-Checking** – Validates claims using NLP and the Google Fact Check API.
- **Innovation News Feed** – Delivers curated news on breakthroughs using NewsAPI.
- **Goal Tracking & AI Insights** – Helps users set, track, and achieve goals, leveraging machine learning and Wolfram AI for predictions.
- **Secure User Authentication** – Manages accounts using JWT authentication.

The backend was primarily designed and developed by Bamidele Israel Anuoluwatomiwa, with the potential for future contributions.

## Features :star:

- **Fact-Checking API Integration**: Validates claims using the Google Fact Check API, with NLP-powered similarity detection to optimize requests.
- **Innovation News Feed**: Fetches and curates the latest advancements using NewsAPI.
- **Goal Tracking & AI Insights**:
  - Users can set goals, track progress, and get AI-powered predictions on milestone completion.
  - Wolfram API is integrated for clustering recommendations and predicting progress trends.
- **Secure Authentication**: Implements JWT-based authentication for user login and registration.

## Technology Stack :wrench:

- **Language**: Python
- **Framework**: Flask
- **Database**: SQLite (configurable)
- **APIs Used**:
  - **Google Fact Check API** – For verifying claims.
  - **NewsAPI** – For delivering innovation news.
  - **Wolfram API** – For AI-based goal tracking and recommendations.
- **Machine Learning**:
  - Uses spaCy for NLP-based text processing.
  - Implements TF-IDF + Cosine Similarity for claim verification.
  - Uses Linear Regression for progress prediction.
  - Applies K-Means Clustering for goal recommendations.

## Innovation :bulb:

Flow Innovation incorporates several innovative backend technologies and features that distinguish it from traditional apps:

1. AI-Powered Fact-Checking 🧐
The app leverages machine learning techniques like **TF-IDF Vectorization** and **Cosine Similarity** to check claims and determine their validity by comparing them with previously checked claims. If no match is found, it queries **Google’s Fact Check API** for real-time validation. This ensures that users have access to trustworthy and verified information quickly.

2. Personalized Progress Prediction 📈
Using **Linear Regression**, the app predicts the completion of user-set goals. The progress data gathered from users’ achievements is used to calculate and forecast when users will complete their milestones. This personalized insight provides actionable feedback for users to stay on track with their goals.

3. Wolfram Integration for Advanced Insights 🧠
The app integrates with **Wolfram’s API** for advanced progress analysis and goal recommendations. This provides users with deep insights into their progress, milestones, and future trajectories. Wolfram’s capabilities, such as clustering analysis and predictive modeling, are used to offer **personalized goal suggestions** and predict future achievements based on historical data.

4. AI-Powered Goal Recommendations 🎯
By analyzing the goals that a user has set and leveraging **Wolfram’s clustering algorithms**, the app generates **intelligent goal recommendations** that help users align their objectives with the most promising and impactful paths.

5. Innovation News Feed 📰
The backend integrates a **news service** that curates **innovation-related articles**, keeping users informed about the latest advancements in technology, sustainability, and more. This feature ensures that users are constantly exposed to groundbreaking ideas and innovations shaping the future.

6. Scalable Architecture 📦
The backend is built with scalability in mind, using the **Flask framework** and **SQLAlchemy ORM** for managing user data, goals, and progress. This ensures smooth data handling and the ability to scale as more users join the platform.

## Running the Backend

Follow these steps to set up and run the backend service:

 1. 📂Navigate to the backend folder:

```bash
cd backend
```

 2. 🐍Set up a virtual environment:

```bash
python -m venv venv  
source venv/bin/activate  # For Linux/Mac  
venv\Scripts\activate     # For Windows 
```  


 3. 📦Install dependencies:

```bash
pip install -r requirements.txt  
```

 4. ⚙️Configure environment variables:
Create a .env file in this folder with the following:

```bash
FACT_CHECK_API_KEY=your-google-api-key  
NEWS_API_KEY=your-newsapi-key  
WOLFRAM_API_URL=your-wolfram-api-endpoint  
DATABASE_URL=sqlite:///flow_innovation.db  
SECRET_KEY=your-secret-key  
```

 5. 🚀Run the server:

```bash
flask run  
```


The backend will now be accessible at `http://127.0.0.1:5000`.

## Folder Structure

```text
backend/  
├── app/  
│   ├── __init__.py        # Backend initialization  
│   ├── routes.py          # API route definitions  
│   ├── models.py          # Database models  
│   ├── services/          # External API integrations  
│   │   ├── news_service.py  
│   ├── config.py          # App configuration  
│   ├── extensions.py      # Database and JWT setup  
├── migrations/            # Database migration scripts
│   ├── alembic.ini        # Alembic configuration  
│   ├── env.py  
│   ├── script.py.mako  
│   ├── README.md          
├── manage.py              # Database migration manager  
├── requirements.txt       # Python dependencies  
├── .gitignore             # Git ignore file  
├── LICENSE                # Project license  
├── README.md              # Documentation
```


## API Endpoints

| Endpoint                  | Method   | Description |
|---------------------------|----------|-------------|
| /check_claim               | GET/POST | Fact-checks a claim using NLP and Google API. |
| /innovation_news           | GET      | Retrieves latest innovation articles via NewsAPI. |
| /register                  | POST     | Registers a new user. |
| /login                     | POST     | Authenticates user and returns JWT token. |
| /progress                  | POST     | Updates user progress. |
| /progress/<user_id>        | GET      | Retrieves a user’s progress with AI-based milestone prediction. |
| /goal                      | POST     | Creates a goal and provides AI-powered recommendations. |
| /goals                     | GET      | Retrieves all goals for a user. |
| /wolfram/progress_insights | POST     | Sends progress data to Wolfram for AI insights. |

## Attributions

This project utilizes several open-source libraries and models, which are integral to its functionality:

- **spaCy:** 🧠Natural language processing is powered by spaCy and the `en_core_web_sm` model.  
  [spaCy Documentation](https://spacy.io/)
  
- **scikit-learn:** 📊Machine learning functionality, including TF-IDF vectorization, clustering, and linear regression models, is powered by scikit-learn.  
  [scikit-learn Documentation](https://scikit-learn.org/)

- **Flask:** The backend is built using the Flask framework.  
  [Flask Documentation](https://flask.palletsprojects.com/)

- **NewsAPI:** 📰News data is retrieved using the NewsAPI Python package.  
  [NewsAPI Documentation](https://newsapi.org/)

- **Wolfram Client:** 🔍Data analysis insights are sent to Wolfram’s API using the Wolfram client.  
  [Wolfram Client Documentation](https://www.wolfram.com/wolfram-client/)

- **ChatGPT:** 🤖Natural language processing and AI-driven assistance are provided by OpenAI's ChatGPT.  
  [OpenAI Documentation](https://openai.com/)

- **Google Fact Check API:** Fact-checking claims are verified using the Google Fact Check API. The API is queried for relevant fact-checking results, which are stored and served if available.  
  [Google Fact Check API Documentation](https://developers.google.com/fact-check/tools/api)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any issues or feedback related to the backend:  

- **Lead Developer:** Bamidele Israel Anuoluwatomiwa  
- **Email:** [bamideleisrael04@icloud.com](mailto:bamideleisrael04@icloud.com)

## Closing Statement

Flow Innovation’s backend combines AI, NLP, and machine learning to address misinformation while fostering progress. With a scalable architecture and robust integrations, it lays the foundation for a more informed and innovative digital space.