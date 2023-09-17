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
