import urllib.request
import re


opengraph_tag_pattern = re.compile(r'(og:\w*)"\s(content=\".*?\")')


def get_opengraph_tags(link):
    with urllib.request.urlopen(link) as f:
        data = f.read().decode('utf-8')
    opengraph_tags = {}
    og_tags = re.findall(opengraph_tag_pattern, data)
    for tag in og_tags:
        tag_type = tag[0].split(':')[1]
        tag_content = tag[1].split('="')[-1]
        opengraph_tags[tag_type] = tag_content
    return opengraph_tags
