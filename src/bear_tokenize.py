import re


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


TOKENS = [
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
for token_def in TOKENS:
    compiled = dict(token_def)
    compiled["regex"] = re.compile(compiled["regex"])
    COMPILED_TOKENS.append(TokenDef(compiled))


def tokenize(input_str):
    ret_tokens = list()
    mytokenizer = Tokenizer(input_str)

    curr_token = ''
    while curr_token != TokenDef.END_TOKENS:
        curr_token = mytokenizer.next_token()
        ret_tokens.append(curr_token)

    return ret_tokens


class Tokenizer:
    def __init__(self, input_str):
        self.input_str = input_str
        self.curr_pos = 0
    
    def next_token(self):
        if self.curr_pos == len(self.input_str):
            return Token(TokenDef.END_TOKENS, "")

        match = None
        for token in COMPILED_TOKENS:
            # Check and see if we're sitting on one of our guys
            match = token.regex.match(self.input_str[self.curr_pos:])
            if match:
                match_token = token
                break
            else:
                continue

        if match:
            end_point = self.curr_pos + match.end()
            literal = self.input_str[self.curr_pos:end_point]

            ret_token = Token(match_token, literal)

            self.curr_pos += match.end()
            return ret_token
        else:
            # TODO
            # LOL so helpful
            raise RuntimeError("Invalid token")
