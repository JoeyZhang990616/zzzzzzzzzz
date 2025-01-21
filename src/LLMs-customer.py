import openai
import csv
import os

api_key = os.getenv('OPENAI_API_KEY', '')
openai.api_base = ""

def chat_with_gpt3_5(messages):
    response = openai.ChatCompletion.create(
        model="",
        messages=messages,
        api_key=api_key,
        stream=True,

    )

    full_response = ""
    for chunk in response:
        if 'choices' in chunk and len(chunk['choices']) > 0:
            content = chunk['choices'][0].get('delta', {}).get('content', '')
            if content:
                print(content, end='', flush=True)
                full_response += content
    print()
    return full_response


def read_questions_from_csv(file_path, max_lines=200, encoding='utf-8'):
    questions = []
    try:
        with open(file_path, 'r', encoding=encoding, errors='replace') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i < max_lines:
                    if row:
                        questions.append(row[0])
                else:
                    break
    except Exception as e:
        print(f"Error reading file: {e}")
    return questions



questions = read_questions_from_csv('')

for question in questions:
    # print(f"问: {question}")
    conversation = [
        {"role": "system", "content": '''
     You are a customer satisfaction expert tasked with evaluating a customer's overall satisfaction based on the following factors:
     - **Product Quality Rating** (Scale: 1 to 10)
     - **Service Quality Rating** (Scale: 1 to 10)
     - **Purchase Frequency** (e.g., number of purchases)
     - **Feedback Level** (Scale: 1 to 3)
     - **Loyalty Level** (Scale: 1 to 3)
     - **Satisfaction Score** (Numeric value)

     **Examples**:
     1. **Poor**: Customer 38434 has a product quality rating of 3, a service quality rating of 4, a purchase frequency of 10, a feedback level of 1, a loyalty level of 2, and a satisfaction score of 89.74.
     2. **Average**: Customer 38435 has a product quality rating of 9, a service quality rating of 10, a purchase frequency of 12, a feedback level of 1, a loyalty level of 1, and a satisfaction score of 100.0.
     3. **Good**: Customer 38436 has a product quality rating of 8, a service quality rating of 4, a purchase frequency of 15, a feedback level of 3, a loyalty level of 3, and a satisfaction score of 100.0.

     When evaluating, use step-by-step reasoning internally to assess each factor before determining the overall satisfaction level. Your reasoning should include:
     1. Analysis of the Product and Service Quality.
     2. Frequency of purchases and its implication on satisfaction.
     3. Feedback and Loyalty Level as indicators of long-term satisfaction.
     4. Satisfaction Score as a numerical anchor for the evaluation.

     **Rules**:
     1. Perform reasoning internally using Chain of Thought (CoT).
     2. Only output the final result in the following format:
        Final Satisfaction Level: {overall_satisfaction_level}

     Do not include any reasoning or intermediate steps in your output.
         '''},
        {"role": "user", "content": question}
    ]

    print("答: ", end='', flush=True)
    assistant_message = chat_with_gpt3_5(conversation)
    print("\n")


    with open('', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['TRUE', 'pre'])
        writer.writerow({'TRUE': question, 'pre': assistant_message})
