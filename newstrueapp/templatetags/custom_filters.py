from django import template
import re


register = template.Library()
words = ["черт", "редиска", "блин"]

@register.filter(name = 'censor')
def f(text_post):
    if not isinstance(text_post, str):
        raise ValueError("This is not a string")
    text_post_fix = text_post
    text_post = text_post.replace('!', ' ')
    text_post = text_post.replace('?', ' ')
    text_split = text_post.split()
    for word in text_split:
        if word.lower() in words:
            word_fix = str(word[0] + "*"*(len(word)-1))
            text_post_fix = text_post_fix.replace(word, word_fix)
    return text_post_fix



