# Read the extracted data from the extracted_data.txt file
with open("extracted_data.txt", "r") as extracted_data_file:
    extracted_data = extracted_data_file.read()

# Define the beginning and ending text
beginning_text = "I am a student in high school and my board exam marks are:"
ending_text = "Based on my marks and subjects, can you suggest career paths that I could take?"

# Create the content for the question.txt file
question_content = f"{beginning_text}\n\n{extracted_data}\n\n{ending_text}"

# Write the content to the question.txt file
with open("question.txt", "w") as question_file:
    question_file.write(question_content)

print("Question created and saved to question.txt.")
