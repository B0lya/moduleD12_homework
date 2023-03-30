from django import template
 
register = template.Library()

censor_words = [
    "блин",
    "дурак",
    "пипец",
]

@register.filter(name='censor')
def censor(value, arg):
    for word in censor_words:
        value = str(value).replace(word, "***")

    return str(value)