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
user_responses = {}

# Function to read user responses from a file
def read_user_responses_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            return [int(line.strip()) for line in lines]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except ValueError:
        print("Invalid response in the file.")
        return None

# Function to calculate and print RIASEC scores
def calculate_riasec_scores(responses):
    if len(responses) != len(questions):
        print("Number of responses does not match the number of questions.")
        return

    print("\nRIASEC Scores:")
    total_score = 0
    for (question, category), response in zip(questions, responses):
        category = category.split()[0]  # Extract the category abbreviation (e.g., "Realistic (R)" => "Realistic")
        user_responses[category] = response
        total_score += response
        print(f"{category}: {response}")

    # Normalize the scores to a total of 100
    normalized_scores = {category: (score / total_score) * 100 for category, score in user_responses.items()}

    print("\nNormalized RIASEC Scores (out of 100):")
    for category, score in normalized_scores.items():
        print(f"{category}: {score:.2f}%")

    return normalized_scores

if __name__ == "__main__":
    user_responses = {}  # Reset user_responses
    user_responses_list = read_user_responses_from_file("answers.txt")
    
    if user_responses_list is not None:
        results = calculate_riasec_scores(user_responses_list)
        
        if results:
            with open("riasec_results.txt", "w") as file:
                file.write("RIASEC Scores:\n")
                for category, score in results.items():
                    file.write(f"{category}: {score:.2f}%\n")
