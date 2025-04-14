🧠 Sentiment Analysis Backend – Setup Guide (Windows)
This guide will help you run the backend for the Sentiment Analyser project locally on your Windows machine – even if you're new to backend development!

📦 What You Need to Install
Before running the backend, you need to install a few tools:

✅ 1. Python 3.8 – 3.11
TensorFlow doesn't work on Python 3.12 yet, so make sure to install a compatible version.

Download Python 3.10 or 3.9 from the official site:
👉 https://www.python.org/downloads/

During installation, check the box that says "Add Python to PATH" and then click Install Now.

✅ 2. Git (optional but helpful)
Download Git from:
👉 https://git-scm.com/downloads

This lets you clone the project from GitHub easily.

🔄 How to Set Everything Up
Step 1: Clone or Download the Project
You can either:

Clone via Git:

bash
Copy
Edit
git clone https://github.com/TheDroidbrand/sentiment-analyser.git
cd sentiment-analyser
Or:

Click "Code" > "Download ZIP" on the GitHub repo, then extract it and open the folder.

Step 2: Create a Virtual Environment (Recommended)
This keeps your Python packages organized and avoids conflicts.

Open Command Prompt in the project folder and run:

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate
You should now see (venv) at the beginning of your command line.

Step 3: Install the Requirements
Now install all the Python packages the backend needs:

bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt doesn't exist or is outdated, you can manually install the main packages:

bash
Copy
Edit
pip install fastapi uvicorn tensorflow
Step 4: Run the Backend Server with Uvicorn
To launch the server, run:

bash
Copy
Edit
uvicorn main:app --reload
⚠️ Replace main with the name of your Python file (without .py) if it's different.

You should see output like:

nginx
Copy
Edit
Uvicorn running on http://127.0.0.1:8000
Now go to your browser and open:
👉 http://127.0.0.1:8000
or test the interactive API docs here:
👉 http://127.0.0.1:8000/docs

✅ You're Done!
The backend is now running and ready to connect to the frontend or be tested using the API docs.

If you run into any issues, feel free to reach out or drop an issue in the GitHub repo.






**🚀 Running the FastAPI Backend Locally (Mac)**
This guide helps you set up and run the backend on your Mac and access the interactive API docs.

📦 Prerequisites
Ensure that you have the following installed:

Python 3.9+
Check by running: python3 --version

pip (Python's package installer)
Check by running: pip --version

🛠️ Setup Instructions
Follow these steps to get the backend running smoothly.

1. Clone the Repository
Clone the backend repository to your local machine:

bash
Copy
Edit
git clone https://github.com/your-username/sentiment-analyzer.git
cd sentiment-analyzer/backend
2. Set Up a Virtual Environment (Recommended)
It’s a good practice to use a virtual environment for your project to keep dependencies isolated. Run these commands to create and activate one:

bash
Copy
Edit
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
You’ll know the virtual environment is active when the prompt changes to include (venv).

3. Install Dependencies
Now, install all the required dependencies (including TensorFlow and others you mentioned):

bash
Copy
Edit
pip install -r requirements.txt
If the requirements.txt file doesn't exist, you can install the dependencies manually. Here's the basic list including TensorFlow, FastAPI, and other necessary packages:

bash
Copy
Edit
pip install fastapi uvicorn tensorflow pydantic
🛠️ Common Missing Dependencies
If you have additional dependencies that were needed (e.g., for audio or visual analysis), you can manually add them to the requirements.txt. Some common ones might be:

bash
Copy
Edit
pip install torch librosa opencv-python
Make sure that you have all the required dependencies listed in your requirements.txt or installed via pip.

4. Run the FastAPI Server
Start the server with the following command:

bash
Copy
Edit
uvicorn main:app --reload
This will launch the server at:

cpp
Copy
Edit
http://127.0.0.1:8000
📄 View the Docs
Once the server is running, you can view the interactive API documentation in your browser:

Swagger UI:
http://127.0.0.1:8000/docs

ReDoc (alternative UI):
http://127.0.0.1:8000/redoc

You can use these to test the API endpoints directly from the browser.

✅ Stopping the Server
Press Ctrl + C in your terminal to stop the server when you're done.

⚠️ Troubleshooting Missing Dependencies
If you encounter issues like missing TensorFlow or other dependencies, simply run:

bash
Copy
Edit
pip install tensorflow
For audio-related issues (e.g., librosa), install it with:

bash
Copy
Edit
pip install librosa
For visual analysis, you might need:

bash
Copy
Edit
pip install opencv-python
