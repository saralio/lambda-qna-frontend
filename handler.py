from saral_utils.extractor.dynamo import DynamoDB
from saral_utils.utils.env import get_env_var
from typing import List, Dict


#TODO: [SAR-69] add normalize_options, image_exists, link_exists, normalize_links function to saral-utils
def normalize_options(options: List) -> List[Dict[str, str]]:
    """normalizes a dictionary from dynamodb, specific to options

    Args:
        options (List[str]): options of a question from table `saral-questions`

    Returns:
        List[Dict[str, str]]: a list with normalized options in dictonary format. Of the form [{'is_correct':..., 'text':..., 'image_path_exists':...}]
    """    
    flat = []
    for option in options:
        opt = {}
        option = option['M']
        opt['is_correct'] = option['correct']['BOOL']
        opt['text'] = option['text']['S']
        opt['image_path_exist'] = True if 'S' in option['imagePath'].keys() else False

        flat.append(opt)
    return flat

def image_exist(question: Dict) -> bool:
    """for a given question from `saral-questions` table check if the question has any image associated with it whether in question or in option

    Args:
        question (Dict): question data

    Returns:
        bool: True if image exist either in question text or in options otherwise False
    """
    que_image_exist = True if 'L' in question['questionImagePath'].keys(
    ) else False

    options = question['options']['L']
    flatten_option = normalize_options(options)
    opt_image_exist = any([True for opt in flatten_option if opt['image_path_exist']])

    if que_image_exist or opt_image_exist:
        return True
    else:
        return False

def links_exist(question: Dict) -> bool:
    """checks if the question has any links for further reading

    Args:
        question (Dict): question dictionary from `saral-question` dynamo table

    Returns:
        bool: True if links exist otherwise False
    """
    return True if 'L' in question['links'].keys() else False

def normalize_links(links: List) -> List[str]:
    """returns a list of normalized links

    Args:
        links (List): A list of unsanatized links from question's data, of the form of `[{'S': 'exte'}, {'S': 'ete'}, ...]`

    Returns:
        List[str]: returns a santized list of links, of the form of `['xyz', 'tywer', 'tet', ...]`
    """

    santazied_links = []
    for link in links:
        santazied_links.append(link['S'])
    
    return santazied_links


def send_qna(event, context):
    
    # get the question id
    question_id = event['pathParameters']['question_id']
    print(f'Requested Question Id: {question_id}')

    env = get_env_var(env='MY_ENV')
    region = get_env_var(env='MY_REGION')
    que_table = f'saral-questions-{env}'
    db = DynamoDB(table=que_table, env=env, region=region)
    question = db.get_item(key={'topic': {'S': 'Programming'}, 'id': {'S': question_id}})

    # extract question metadata
    question_text = question['questionText']['S']
    options = normalize_options(question['options']['L'])
    explaination_text = question['explainationText']['S']
    if links_exist(question):
        links = normalize_links(links=question['links']['L'])
    else:
        links = None


    with open('qna.html', 'r') as file:
        html = file.read()
    
    #TODO: [SAR-68] modify html file to show question and answer as a quiz
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
