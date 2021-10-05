from typing import Dict, Optional


Tag = str
Tags = list[Tag]
TagsDictionary = Dict[str, Tags]


def resolve_tag(product_tags: Tags, search_tags: Tags) -> Optional[Tag]:
    """
    제품의 태그(product_tags)에서 찾으려는 태그(search_tags)를 찾아냅니다.
    """
    for product_tag in product_tags:
       for category_tag in search_tags:
           if product_tag == category_tag:
               return category_tag
    
    return None