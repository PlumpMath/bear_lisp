import bear_tokenize

from bear_tokens import *

_grammar_rules = {}
class GrammarRule:
    def __init__(self, name):
        _grammar_rules[name] = self
        self.productions = []

    def add_production(self, production):
        self.productions.append(production)

# rule() and token() aid in forward referencing of rules
def rule(rule_name):
    return lambda: _grammar_rules[rule_name]

def token(token_name):
    return lambda: TOKEN_DICT[token_name]


# A module is a bunch of S-Expressions
module = GrammarRule('module')
module.add_production([rule('sexprs')])

# Here is how we define 'a bunch of S-Expressions'
sexprs = GrammarRule('sexprs')
sexprs.add_production([rule('sexpr'), rule('sexprs')])
sexprs.add_production([rule('sexpr')])

# A single S-Expression
sexpr = GrammarRule('sexpr')
sexpr.add_production([rule('list')])
sexpr.add_production([rule('atom')])

# A list
bear_list = GrammarRule('list')
bear_list.add_production([token(LEFT_PAREN), rule('listend')])

listend = GrammarRule('listend')
listend.add_production([rule('sexprs'), token(RIGHT_PAREN)])
listend.add_production([token(RIGHT_PAREN)])

# An atom
atom = GrammarRule('atom')
atom.add_production([token(SYMBOL)])
atom.add_production([token(LIT_NUMBER)])
atom.add_production([token(LIT_STRING)])


def parse(input_str):
    # Tokenize Code
    tokens = bear_tokenize.tokenize(input_str)

    for token in tokens:
        print token.__repr__()
