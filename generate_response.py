import os
import openai
import csv
from dotenv import load_dotenv
from loaders import split_file

load_dotenv()

# Load environment variables
open_ai_key = os.getenv("OPENAI_API_KEY")
open_ai_model = os.getenv("OPEN_AI_MODEL")
client = openai.OpenAI(api_key=open_ai_key)
file_path = os.getenv('DOCX_PATH')
chunks = split_file(file_path)

def generate_timeline(requirement_chunks):
    # Create messages for the chat model
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that specializes in Machine Learning (ML), Full-Stack (FS) and DevOps engineering. You are skilled at project management and timeline generation, with a strong understanding of software development processes and best practices."
                "Be mindful to avoid excessive durations in all the tasks, and suggest a practical timeline for efficient project delivery.")
        },
        {
            "role": "user",
            "content": (
                "Based on the following requirements, please create a comprehensive timeline for the project."
                "The timeline should include all tasks and their respective subtasks, "
                "along with estimated durations in both hours and days for each task.\n\n"
                f"{requirement_chunks}\n\n"
                "Output the timeline strictly in CSV format as follows:\n"
                "Phase,Task,Subtask,Total Time (Days),Total Time (Hours)\n"
                "Strictly ensure that task and subtask descriptions do not contain commas."
                "Do not include any additional text or explanations."
                "Strictly do not include '''  '''."
            )
        }
    ]

    # Call the OpenAI API to generate the timeline using chat completion
    response = client.chat.completions.create(
        model=open_ai_model,
        messages=messages,
        max_tokens=int(os.getenv('MAX_TOKENS')),
        n=1,
        temperature=float(os.getenv('TEMPERATURE')),
    )

    # Extract the generated timeline from the response
    timeline_text = response.choices[0].message.content

    # Save the timeline as a CSV file
    save_timeline_to_csv(timeline_text)
    return timeline_text

def save_timeline_to_csv(timeline_text):
    """
    Saves the provided timeline text to a CSV file.
    """
    # Define the CSV file path
    csv_file_path = 'project_timeline.csv'

    lines = timeline_text.strip().split('\n')
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for line in lines:
            row = line.split(',')
            writer.writerow(row)

    print(f"Timeline successfully saved to {csv_file_path}")

    return csv_file_path

# Example usage
generate_timeline(chunks)