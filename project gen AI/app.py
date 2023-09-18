from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import requests
import logging
import json

app = Flask(__name__)
CORS(app)
logging.basicConfig(filename='app.log', level=logging.INFO)

# Function to store answers in a text file
@app.route('/upload-marksheet', methods=['POST'])
def upload_marksheet():
    if 'marksheet' not in request.files:
        return jsonify({'error': 'No marksheet part'})

    file = request.files['marksheet']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # You can save the file to a specific directory or process it as needed
    # For example, to save it to a directory:
    file.save('uploads/' + file.filename)

    return jsonify({'message': 'Marksheet uploaded successfully'})

def save_answers(answers):
    with open("answers.txt", "w") as file:
        json.dump(answers, file)

# Function to run the OCR process
def run_ocr():
    try:
        import re

        # Specify the URL of the PDF data extraction API
        url = "https://api.worqhat.com/api/ai/v2/pdf-extract"

        # Specify the path to the PDF file you want to extract data from
        pdf_file_path = "/content/Class X Original Marksheet.pdf"

        # Create a dictionary to hold the PDF file data
        files = {'file': (pdf_file_path, open(pdf_file_path, 'rb'))}

        # Specify your API token in the 'Authorization' header
        headers = {
            "Authorization": "Bearer sk-c9d067cb72fc47af953e9dfc8d26b9da"
        }

        # Send a POST request to the API with the PDF data
        response = requests.post(url, files=files, headers=headers)

        # Check the response from the API
        if response.status_code == 200:
            content = response.json().get("content", "No content available.")

            # Extract only the content part
            content_start = content.find("MARKS STATEMENT CUM CERTIFICATE")
            if content_start != -1:
                content = content[content_start:]

            # Clean up the content by removing extra spaces and formatting
            content = re.sub(r'\n{2,}', '\n', content)  # Remove consecutive line breaks
            content = content.replace(' :', ':')  # Remove spaces before colons

            # Print the formatted content
            print(content)

            # Export the result to a text file
            with open("prompt.txt", "w") as output_file:
                output_file.write(content)

            print("Result exported to 'prompt.txt'")
        else:
            print("Error:", response.text)
    except Exception as e:
        logging.error(f"Exception in OCR process: {str(e)}")

# Function to run text processing
def run_text_processing():
    try:
        # Read the extracted text from a text file
        with open("prompt.txt", "r") as file:
            text = file.read()

        # Split the text into lines
        lines = text.split('\n')

        # Initialize a flag to identify the start of the table
        table_started = False

        # Initialize lists to store Subject Names and Total Marks
        subject_names = []
        total_marks = []

        # Iterate through each line of the text
        for line in lines:
            if "SUB. CODE" in line:
                # Start of the table found
                table_started = True
            elif table_started and "|" in line:
                # Split the line using '|' as a delimiter
                columns = line.split('|')
                # Remove leading and trailing whitespace from each column
                columns = [col.strip() for col in columns]
                # Check if the columns have at least 6 elements (Subject Name and Total Marks)
                if len(columns) >= 6:
                    subject_name = columns[2]
                    total_mark = columns[5]
                    # Check if the Total Marks is a numeric value
                    if total_mark.isdigit():
                        subject_names.append(subject_name)
                        total_marks.append(total_mark)

        # Print the extracted Subject Names and Total Marks
        for subject, marks in zip(subject_names, total_marks):
            print(f"Subject Name: {subject}")
            print(f"Total Marks: {marks}")
            print()

        # Save the extracted data to a text file
        with open("extracted_data.txt", "w") as output_file:
            for subject, marks in zip(subject_names, total_marks):
                output_file.write(f"Subject Name: {subject}\n")
                output_file.write(f"Total Marks: {marks}\n")
                output_file.write("\n")
    except Exception as e:
        logging.error(f"Exception in text processing: {str(e)}")

# Function to run RIASEC score calculation
def run_riasec_score_calculation():
    try:
        from collections import defaultdict

        # Define the questions and corresponding RIASEC categories
        questions = [
            ("Do you enjoy working with your hands and tools?", "Realistic (R)"),
            ("Are you naturally curious and enjoy exploring new ideas?", "Investigative (I)"),
            ("Do you have a passion for creative activities like drawing, writing, or music?", "Artistic (A)"),
            ("Do you find fulfillment in helping and working with others?", "Social (S)"),
            ("Are you ambitious and enjoy taking on leadership roles?", "Enterprising (E)"),
            ("Do you prefer working in structured and organized environments?", "Conventional (C)"),
            ("Are you interested in working outdoors or in natural settings?", "General (Mixed RIASEC)"),
            ("Do you prefer a fast-paced and dynamic work environment?", "General (Mixed RIASEC)"),
            ("Do you enjoy working with machinery and technology?", "Realistic (R)"),
            ("Do you like conducting experiments and solving complex problems?", "Investigative (I)"),
            ("Do you have a talent for artistic and creative expression?", "Artistic (A)"),
            ("Do you enjoy teaching or mentoring others?", "Social (S)"),
            ("Do you have strong negotiation and persuasion skills?", "Enterprising (E)"),
            ("Do you prefer a neat and structured workspace?", "Conventional (C)"),
            ("Do you like spending time in nature and outdoor activities?", "General (Mixed RIASEC)"),
            ("Do you thrive in high-pressure and competitive situations?", "General (Mixed RIASEC)"),
            ("Are you mechanically inclined and good at fixing things?", "Realistic (R)"),
            ("Do you enjoy analyzing data and conducting research?", "Investigative (I)"),
            ("Are you skilled in playing musical instruments or creating art?", "Artistic (A)"),
            ("Do you excel in teamwork and collaboration?", "Social (S)")
        ]

        # Initialize a dictionary to store user responses
        user_responses = defaultdict(int)

        # Read the user's responses from a file
        with open("answers.txt", "r") as file:
            user_responses_list = [int(line.strip()) for line in file]

        if len(user_responses_list) != len(questions):
            logging.error("Number of responses does not match the number of questions.")
            return

        for (question, category), response in zip(questions, user_responses_list):
            category = category.split()[0]  # Extract the category abbreviation (e.g., "Realistic (R)" => "Realistic")
            user_responses[category] += response

        # Normalize the scores to a total of 100
        total_score = sum(user_responses.values())
        normalized_scores = {category: (score / total_score) * 100 for category, score in user_responses.items()}

        # Save the results to a text file
        with open("riasec_results.txt", "w") as file:
            file.write("RIASEC Scores:\n")
            for category, score in normalized_scores.items():
                file.write(f"{category}: {score:.2f}%\n")
    except Exception as e:
        logging.error(f"Exception in RIASEC score calculation: {str(e)}")

# Function to run prompt creation
def run_prompt_creation():
    try:
        with open("extracted_data.txt", "r") as extracted_data_file:
            extracted_data = extracted_data_file.read()

        with open("riasec_results.txt", "r") as riasec_data_file:
            riasec_data = riasec_data_file.read()

        # Define the beginning and ending text
        beginning_text = "I am a student in high school and my board exam marks are:"
        middle_text = "I also took the Holland Occupational Themes or the RIASEC codes test to figure out the best career and got the following scores:"
        ending_text = "Based on my marks and subjects, can you suggest career paths that I could take?"

        # Create the content for the question.txt file
        question_content = f"{beginning_text}\n\n{extracted_data}\n\n{middle_text}\n\n{riasec_data}\n\n{ending_text}"

        # Write the content to the question.txt file
        with open("question.txt", "w") as question_file:
            question_file.write(question_content)

        print("Question created and saved to question.txt.")
    except Exception as e:
        logging.error(f"Exception in prompt creation: {str(e)}")

# Route to receive messages from the frontend
@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        user_message = data.get('message')

        if user_message == "start_ocr":
            run_ocr()
            return jsonify({"response": "OCR process started."})

        if user_message == "start_text_processing":
            run_text_processing()
            return jsonify({"response": "Text processing started."})

        if user_message == "start_riasec_score_calculation":
            run_riasec_score_calculation()
            return jsonify({"response": "RIASEC score calculation started."})

        if user_message == "start_prompt_creation":
            run_prompt_creation()
            return jsonify({"response": "Prompt creation started."})

        # Forward the user's message to the Worqhat API
        worqhat_url = "https://api.worqhat.com/api/ai/content/v3"
        headers = {
            "Authorization": "Bearer sk-0988d888ee574422a01561e9bf5de02e",  # Replace with your actual API key
            "Content-Type": "application/json"
        }
        worqhat_data = {
            "question": user_message,
            "randomness": 0.4
        }
        response = requests.post(worqhat_url, headers=headers, json=worqhat_data)

        if response.status_code == 200:
            content = response.json().get("content")

            content = content.replace("\n\n", "\n")
            # worqhat_response = response.json().get("content")
            return jsonify({"response": content})

        # Log the error
        logging.error(f"Error in request to Worqhat API: {response.status_code} - {response.text}")

        return jsonify({"response": "Error communicating with Worqhat API"})

    except Exception as e:
        # Log the exception
        logging.error(f"Exception in send_message route: {str(e)}")
        return jsonify({"response": str(e)})

# Route to serve the aptitude test form
@app.route("/aptitude-test", methods=["GET", "POST"])
def aptitude_test():
    try:
        data = request.get_json()
        app.logger.info("Received data: %s", data)  # Log received data
        answers = data.get("answers")

        # Process and save answers here
        save_answers(answers)  # Save answers to a file or process as needed
        return jsonify({"success": True})  # Respond with success
    except Exception as e:
        app.logger.error("Error processing aptitude test form: %s", str(e))  # Log error
        return jsonify({"success": False, "error": str(e)})  # Respond with error

        return redirect(url_for("thank_you"))
    return render_template("./index2.html")

@app.route("/thank_you")
def thank_you():
    return "Thank you for submitting your answers!"

if __name__ == '__main__':
    app.run(debug=False)