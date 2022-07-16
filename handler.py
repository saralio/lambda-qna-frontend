import urllib
from jinja2 import Environment, FileSystemLoader
from saral_utils.extractor.dynamo import DynamoDB
from saral_utils.utils.env import get_env_var, create_env_api_url
from saral_utils.utils.frontend import ShareLinks
from utils import normalize_links, normalize_options, links_exist, opt_markdown, qna_markdown


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
    has_links = links_exist(question)
    if has_links:
        links = normalize_links(links=question['links']['L'])
    else:
        links = None
    correct_option_text = 'Uh-oh! Your answer is incorrect. Correct answer is: ' + [
        opt['text'] for opt in options if opt['is_correct']][0]

    sl = ShareLinks()
    answer_url = create_env_api_url(url=f"answer.saral.club/qna/{question_id}")
    signup_url = sl.saral_website_link
    tweet_text = f"Check out this question by @data_question on #RStats: {answer_url}\n\nYou can subscribe at {signup_url} to get such questions daily in your inbox."
    tweet_encode = urllib.parse.quote_plus(tweet_text)   # type:ignore
    tweet_link = f'{sl.sharing_link}{tweet_encode}'

    navbar_links = {
        'signup_url': signup_url,
        'tweet_share_link': tweet_link,
        'youtube_link': sl.youtube_link,
        'donation_link': sl.donation_link,
        'feedback_link': sl.feedback_link,
        'twitter_account_link': sl.twitter_account_link
    }

    template_data = {
        'question_text': question_text,
        'answer_text': explaination_text,
        'options': options,
        'links': links,
        'has_links': has_links,
        'correct_option_text': correct_option_text,
        'navbar_links': navbar_links
    }

    env = Environment(loader=FileSystemLoader('.'))
    env.filters['qna_markdown'] = qna_markdown
    env.filters['opt_markdown'] = opt_markdown

    with open('./templates/qna-template.html', 'r') as file:
        html_template = file.read()

    template = env.from_string(html_template)
    content = template.render(question=template_data)

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