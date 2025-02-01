## Welcome 

1. [Flow Innovation](#flow-innovation)
2. [Motivation](#motivation)
3. [Features](#features)
4. [Tech Stack](#tech-stack)
5. [Installation and Setup](#installation-and-setup)
6. [Usage](#usage)
7. [Impact](#impact)
8. [Innovation](#innovation)
9. [Future Enhancements](#future-enhancements)

# Flow Innovation

Flow Innovation is a web application designed to empower users to uncover the truth and explore innovation through fact-checking and discovery tools. Built with a Flask backend and a React frontend, the platform provides users with a seamless experience in a sleek dark-mode interface.


## Motivation

> "Despite unprecedented access to information and resources, our generation’s innovation rate does not match its potential.  
>  
> Many breakthroughs today focus on refinement rather than groundbreaking progress.  
>  
> While immersive tech, better cellphones, and self-driving cars are impressive, they often feel incremental rather than transformative.  
>  
> It feels as though we’ve hit a barrier—one that shouldn’t exist in 2025."  
>  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Israel

During our team’s brainstorming session, Ivan shared his thoughts on the significance of addressing misinformation. He suggested that AI and machine learning could be pivotal in verifying claims, ensuring that users receive credible information. Additionally, Ivan pointed out how mainstream media often centers around negative stories, which can create a skewed perception of progress. Inspired by these ideas, we decided to build Flow Innovation.

In today’s digital age, misinformation spreads rapidly, shaping public opinion and influencing critical decisions. While fact-checking exists, it’s often buried beneath sensationalized content, making truth harder to access.

At the same time, innovation and scientific progress often take a backseat in mainstream media. Instead of inspiring stories about groundbreaking research and technological advancements, most headlines focus on controversy, negativity, and entertainment. This creates a skewed perception that humanity is stagnating rather than progressing.

Flow Innovation was created to combat these issues by:
- Using AI-powered fact-checking to verify claims and provide users with credible information quickly.
- Highlighting new inventions and scientific breakthroughs to inspire curiosity and progress.

Our goal is to promote truth, innovation, and progress—ensuring that people have access to accurate information and a renewed belief in humanity’s forward momentum.

## Features

- **Fact-Checking**: Input claims to verify their authenticity and receive detailed results from reliable sources.
- **Innovation Feed**: Explore a curated feed of modern innovations and breakthroughs.
- **Dark Mode Interface**: Designed with accessibility and aesthetics in mind for a user-friendly experience.
- **Collaborative Development**: Built collaboratively by two engineers to deliver a robust and scalable solution.

## Tech Stack

- **Frontend**: React with modern JavaScript and CSS for a responsive and interactive user interface.
- **Backend**: Flask for handling API endpoints and server-side logic.
- **Database**: SQLite for lightweight and efficient data storage.
- **Styling**: Custom CSS for a sleek dark mode theme.

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Rendon-04/flow_innovation.git
   cd flow_innovation
   ```

2. **Backend Setup:**
   - Navigate to the `backend` folder:
     ```bash
     cd backend
     ```
   - Create a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Start the Flask server:
     ```bash
     python app.py
     ```

3. **Frontend Setup:**
   - Navigate to the `frontend` folder:
     ```bash
     cd ../frontend
     ```
   - Install dependencies:
     ```bash
     npm install
     ```
   - Start the development server:
     ```bash
     npm start
     ```

4. **Access the Application:**
   Open your browser and navigate to `http://localhost:3000` to view the application.

## Usage
- Explore the innovation feed for curated insights into modern advancements.
- Use the fact-checking feature to verify claims.

## Impact

Misinformation is one of the most urgent global challenges today, with the proliferation of false claims online affecting everything from public health to political discourse. Alongside this issue, innovative ideas and breakthroughs often struggle to gain the visibility they deserve, slowing progress in vital fields like technology, medicine, and sustainability.

Flow Innovation tackles these two interconnected problems head-on. First, by leveraging AI-driven fact-checking, the app helps users quickly verify claims, promoting truth and trust in the information they consume. Second, it provides a curated feed of groundbreaking innovations, ensuring that users stay informed about the latest advancements. This keeps them at the cutting edge of progress, sparking curiosity and inspiring action towards a more innovative and sustainable future.

Moreover, Flow Innovation doesn’t just highlight innovation — it tracks progress. By offering tools that help users set, track, and predict milestones in their own personal and professional journeys, the app encourages users to not only stay informed but also actively participate in shaping the future. This dual focus on fact-checking and progress empowers individuals to make informed decisions, contribute to meaningful change, and be part of a thriving, forward-thinking global community.

By tackling misinformation and boosting the visibility of innovation while actively fostering personal and collective progress, Flow Innovation empowers users to stay at the forefront of progress, both individually and globally.

## Innovation

Curious about how Flow Innovation tackles these challenges?  
Explore the innovative features and technologies behind the app by checking out our [backend README.md](./backend/README.md#innovation-bulb).

## Attributions

- **Ivan**: Contributed to the frontend development, including design and functionality. 
- For backend-specific attributions, please refer to the [Backend README.md](./backend/README.md#attributions).

## Future Enhancements
- Integration of AI/ML for advanced fact-checking capabilities.
- User accounts for personalized experiences and saved history.



