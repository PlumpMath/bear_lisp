import re

# Token Type Enumeration
WHITESPACE = 'WHITESPACE'
LEFT_PAREN = 'LEFT_PAREN'
RIGHT_PAREN = 'RIGHT_PAREN'
QUOTE = 'QUOTE'
SYMBOL = 'SYMBOL'
LIT_NUMBER = 'LIT_NUMBER'
LIT_STRING = 'LIT_STRING'
END_TOKENS = 'END_TOKENS'


class TokenDef:
    def __init__(self, tok_dict):
        self.name = tok_dict['name']
        self.regex = tok_dict['regex']
        self.type= tok_dict['type']

TokenDef.END_TOKENS = TokenDef({
    "name": END_TOKENS,
    "regex": "",
    "type": END_TOKENS
})


class Token:
    def __init__(self, tok_def, literal):
        self.token_def = tok_def
        self.literal = literal

    def __repr__(self):
        return "Token({ type: \"%s\", literal: \"%s\" })" % (
                self.token_def.name, self.literal)


TOKEN_INFO = [
    {
        "name": 'Whitespace',
        "regex": """\s+""",
        "type": WHITESPACE
    },
    {
        "name": 'Left Paren',
        "regex": """\(""",
        "type": LEFT_PAREN
    },
    {
        "name": 'Right Paren',
        "regex": """\)""",
        "type": RIGHT_PAREN
    },
    {
        "name": 'Quote',
        "regex": """'""",
        "type": QUOTE
    },
    {
        "name": 'Symbol',
        "regex": ("""(?:[a-zA-Z]|[!\$%&\*\+\-:<=>\?@\^_~])"""
                  """(?:[a-zA-Z]|[\d!\$%&\*\+\-:<=>\?@\^_~])*"""),
        "type": SYMBOL
    },
    {
        "name": 'Literal Number',
        "regex": """\d+(?:\.\d+)?""",
        "type": LIT_NUMBER
    },
    {
        "name": 'Literal String',
        "regex": """\"(?:\\.|[^"])*\"""",
        "type": LIT_STRING
    }
]

COMPILED_TOKENS = list()
for token_def in TOKEN_INFO:
    compiled = dict(token_def)
    compiled["regex"] = re.compile(compiled["regex"])
    COMPILED_TOKENS.append(TokenDef(compiled))

TOKEN_DICT = dict()
for token_def in COMPILED_TOKENS:
    TOKEN_DICT[token_def.type] = token_def
