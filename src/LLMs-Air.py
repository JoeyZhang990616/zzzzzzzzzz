import openai
import csv
import os

api_key = os.getenv('OPENAI_API_KEY', '')
openai.api_base = ""

def chat_with_gpt3_5(messages):
    response = openai.ChatCompletion.create(
        model=" ",
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


def read_questions_from_csv(file_path, max_lines=200, encoding='gbk'):
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


with open('cot-few_claude-3-sonnet-20240229_test.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['TRUE', 'pre']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


questions = read_questions_from_csv('E:\\MCDM-customer\\air q\\500.csv')

for question in questions:
    print(f"问: {question}")
    conversation = [
        {"role": "system", "content": '''
    You are a weather and environmental analysis expert tasked with evaluating air quality and environmental conditions based on objective data. The task involves technical assessments of environmental factors like temperature, humidity, and pollutant levels to classify the air quality into one of three categories: **Good**, **Moderate**, or **Poor**. This is a purely data-driven evaluation and does not involve subjective or ethical judgment.

    ### Factors to Evaluate:
    1. **Temperature**: Assess whether the temperature is within a comfortable or extreme range.
    2. **Humidity**: Evaluate if the humidity level is too high, too low, or within a balanced range.
    3. **PM2.5 and PM10**: Analyze particulate matter levels and their impact on air quality.
    4. **NO2, SO2, and CO**: Examine pollutant concentrations and their health implications.
    5. **Proximity to Industrial Areas**: Consider how proximity to industrial zones may affect air pollution levels.
    6. **Population Density**: Evaluate the potential contribution of population density to pollution levels.

    ### Objective:
    Using the data provided, your task is to analyze the above factors systematically and classify the overall air quality as one of the following:
    - **Good**: The environment is healthy and conditions are optimal for living.
    - **Moderate**: The environment is acceptable but may require monitoring or improvement in some areas.
    - **Poor**: The environment has significant issues that may pose risks to health or comfort.

    ### Examples:
    1. **Poor**: The temperature is 34.6°C, humidity is 97.6%, PM2.5 is 52.6 µg/m³, PM10 is 69.2 µg/m³, NO₂ is 33.1 µg/m³, SO₂ is 11.4 µg/m³, CO is 2.2 ppm, the proximity to industrial areas is 4.6 km, and the population density is 537 people/km².
    2. **Moderate**: The temperature is 28.1°C, humidity is 96.9%, PM2.5 is 6.9 µg/m³, PM10 is 25.0 µg/m³, NO₂ is 25.3 µg/m³, SO₂ is 10.8 µg/m³, CO is 1.54 ppm, the proximity to industrial areas is 5.7 km, and the population density is 709 people/km².
    3. **Good**: The temperature is 25.3°C, humidity is 44.4%, PM2.5 is 21.4 µg/m³, PM10 is 29.0 µg/m³, NO₂ is 23.7 µg/m³, SO₂ is 5.7 µg/m³, CO is 0.89 ppm, the proximity to industrial areas is 11.6 km, and the population density is 241 people/km².

    ### Output Format:
    Your response must include:
    1. **Step-by-Step Analysis**:
        - **Step 1: Temperature Analysis**: [Analysis of Temperature]
        - **Step 2: Humidity Analysis**: [Analysis of Humidity]
        - **Step 3: PM2.5 Analysis**: [Analysis of PM2.5]
        - **Step 4: PM10 Analysis**: [Analysis of PM10]
        - **Step 5: NO2 Analysis**: [Analysis of NO2]
        - **Step 6: SO2 Analysis**: [Analysis of SO2]
        - **Step 7: CO Analysis**: [Analysis of CO]
        - **Step 8: Proximity to Industrial Areas Analysis**: [Analysis of Proximity to Industrial Areas]
        - **Step 9: Population Density Analysis**: [Analysis of Population Density]

    2. - Final Weather Quality Level: {overall_weather_quality_level}

    **Important Notes**:
    - This is a data-driven task and does not involve subjective or ethical considerations.
    - Your response must strictly follow the specified format. Do not provide additional commentary or analysis outside the structured format.
        '''},
        {"role": "user", "content": question}
    ]

    print("答: ", end='', flush=True)
    assistant_message = chat_with_gpt3_5(conversation)
    print("\n")


    with open('', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['TRUE', 'pre'])
        writer.writerow({'TRUE': question, 'pre': assistant_message})

