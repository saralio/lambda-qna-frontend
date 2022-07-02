import json
from pprint import pprint

with open('sample-questions.json', 'r') as file:
    questions = json.load(file)

# to get the question id -> at this point just getting question data in enough. We will do later to fetch from db
# at this point just develop using local data

#TODO: [SAR-67] fetch question from dynamodb based on question-id
#TODO: [SAR-68] modify html file to show question and answer as a quiz

def send_qna(event, context):


    question_id = event['pathParameters']['question_id']
    question_text='None'
    explaination_text='None'

    for question in questions['questions']:
        question = question['Item']
        id = question['id']['S']
        if id == question_id:
            question_text = question['questionText']['S']
            explaination_text = question['explainationText']['S']

    with open('qna.html', 'r') as file:
        html = file.read()
    
    content = html.format(question_id=question_id, question_text=question_text, explaination_text=explaination_text)
    response = {
        "statusCode": 200,
        "body": content,
        "headers": {
            "Content-Type": "text/html",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "Get"
        }
    }

    return response
