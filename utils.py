import markdown
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


def base_markdown(html_text, extension, extension_configs):
    html = markdown.markdown(
        html_text, 
        extensions=extension,
        extension_configs=extension_configs)
    return html

def qna_markdown(text):
    html = base_markdown(text, ['markdown.extensions.fenced_code', 'markdown.extensions.codehilite'], {
        'markdown.extensions.codehilite': {
            'pygments_style': 'material',
            'noclasses': True,
            'cssstyles': 'padding: 10px 10px 10px 20px; margin: 1% 3% 1% 3%'
        }
    })
    return html

def opt_markdown(text):
    html = base_markdown(text, ['markdown.extensions.fenced_code', 'markdown.extensions.codehilite'], {
        'markdown.extensions.codehilite': {
            'pygments_style': 'material',
            'noclasses': True,
        }
    })
    return html