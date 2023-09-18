# SkillSet-Sherpa
This README provides instructions on how to deploy the SkillSet Sherpa application that utilizes Flask, Flask-CORS, and other components. The chatbot allows users to take an aptitude test through "aptitude.html" and communicate with the chatbot in "index.html." The backend is implemented in "app.py," and styling is provided by "style.css." The chatbot functionality is enhanced using "aptitude.js."

## Prerequisites
Before deploying the chatbot, ensure you have the following prerequisites installed on your system:

Python 3.x

Flask

Flask-CORS

## Getting Started
Clone the repository to your local machine:
```git clone https://github.com/yourusername/your-chatbot-repo.git```

Navigate to the project directory:
```cd your-chatbot-repo```

Install the required Python packages using pip:

```pip install -r requirements.txt```

## Running SkillSet Sherpa
Start the Flask server:
```python app.py```
This will start the server, and you should see output indicating that the server is running, typically on ```http://127.0.0.1:5000/.```


Access the chatbot interface by opening "index.html" in your web browser:
```http://127.0.0.1:5000/```

To take the aptitude test, navigate to:

```http://127.0.0.1:5000/aptitude.html```

## Chatbot Features

The chatbot interface is provided in ```index.html``` where users can interact with the chatbot.
The aptitude test can be taken through "aptitude.html," and the results can be processed by the backend in ```app.py``` where the output of the ```aptitude.html``` file is calculated and a proper output is generated that guides the user to a proper career path.

## Customization
You can customize the chatbot by modifying the HTML, CSS, and JavaScript files to tailor our chatbot's behavior and appearance according to your requirements.

## Deployment
FFor production deployment, consider using a web hosting service or platform like Heroku or AWS to make your chatbot accessible over the internet. Ensure that you handle environment variables securely for sensitive data such as your API key.
