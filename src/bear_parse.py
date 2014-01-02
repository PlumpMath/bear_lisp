import bear_tokenize

from bear_tokens import *

_grammar_rules = {}
class GrammarRule:
    def __init__(self, name):
        # rofl what is code reuse
        _grammar_rules[name] = self
        self.name = name
        self.productions = []

    def add_production(self, production):
        self.productions.append(production)

    def __repr__(self):
        return "GrammarRule({ \"name\": \"%s\" })" % self.name


# rule() and token() aid in forward referencing of rules
def rule(rule_name):
    return lambda: _grammar_rules[rule_name]

def token(token_name):
    return lambda: TOKEN_DICT[token_name]


"""
This parser works on grammars expressed in Chomsky Normal Form, or at least
close to it as the one below.
"""

# Here is how we define 'a bunch of S-Expressions'
sexprs = GrammarRule('sexprs')
sexprs.add_production([rule('sexpr'), rule('sexprs')])
sexprs.add_production([rule('sexpr')])

# A single S-Expression
sexpr = GrammarRule('sexpr')
sexpr.add_production([rule('list')])
sexpr.add_production([rule('atom')])

# An atom
atom = GrammarRule('atom')
atom.add_production([token(SYMBOL)])
atom.add_production([token(LIT_NUMBER)])
atom.add_production([token(LIT_STRING)])

# A list
bear_list = GrammarRule('list')
bear_list.add_production([rule('left_paren'), rule('listend')])
bear_list.add_production([rule('left_paren'), rule('right_paren')])

listend = GrammarRule('listend')
listend.add_production([rule('sexprs'), rule('right_paren')])
listend.add_production([rule('sexprs'), rule('listend')])

# I think CNF demands that terminals need their own productions...
left_paren = GrammarRule('left_paren')
left_paren.add_production([token(LEFT_PAREN)])
right_paren = GrammarRule('right_paren')
right_paren.add_production([token(RIGHT_PAREN)])


def parse(input_str):
    """Constructs a parse tree from bear lisp code using the CYK algorithm"""

    def find_terminal_produtions_for(token):
        """Finds the set of all grammar rules that produce a terminal symbol"""

        def grammar_rule_has_terminal(grammar_rule, token):
            """Finds whether or not a grammar rule can produce a terminal"""
            for production in grammar_rule.productions:
                production = map(lambda x: x(), production)
                produces = any(map(
                    lambda p: isinstance(p, TokenDef) and
                              token.token_def.type == p.type,
                    production))
                if produces:
                    return True
            return False

        grammar_rules = _grammar_rules.values()
        return set(filter(lambda gr: grammar_rule_has_terminal(gr, token),
                          grammar_rules))


    def expand_symbol(symbol_set):
        """Finds the set of all grammar rules equivalent to the given
        
        For example, if you are given the set {`atom`} you will get
        {`atom`, `sexpr`, `sexprs`}

        """
        curr_expanding = set(symbol_set)
        expanded = set(symbol_set)

        grammar_rules = _grammar_rules.values()

        # If changes occur, you must search again
        still_expanding = True
        while still_expanding:
            still_expanding = False
            for grammar_symbol in curr_expanding:
                # Determine if this symbol is produced 1-1 in any rules
                for grammar_rule in grammar_rules:
                    for production in grammar_rule.productions:
                        if (len(production) == 1 and
                            production[0]() in curr_expanding and
                            grammar_rule not in expanded):
                                expanded.add(grammar_rule)
                                still_expanding = True
            curr_expanding = set(expanded)
        return expanded


    def find_producing_rules(symbol1, symbol2):
        """Finds a grammar rule that produces the pair of symbols"""
        grammar_rules = _grammar_rules.values()
        producing_rules = set()

        for grammar_rule in grammar_rules:
            for production in grammar_rule.productions:
                if (len(production) == 2 and
                    production[0]() in symbol1 and
                    production[1]() in symbol2):
                    producing_rules.add(grammar_rule)
        return producing_rules


    # Tokenize Code
    tokens = bear_tokenize.tokenize(input_str)

    # init cyk
    prod_tree = [map(expand_symbol, map(find_terminal_produtions_for, tokens))]
    # Keep track of child nodes
    children = [map(lambda _: set(), prod_tree[0])]
   
    # Work our way up to the root of the parse tree
    # TODO this will loop infinitely on syntactically incorrect input
    while len(prod_tree[-1]) > 1:
        last_iter = prod_tree[-1]

        # Generate the next parse tree level
        next_iter = list()
        next_children = list()

        skip_next = False  # Flag used to skip iterations of symbol pairs
        # Look for producing rules for pairs of symbols in the last iteration
        for i in xrange(len(last_iter)):
            if skip_next:
                skip_next = False
                continue

            if i == (len(last_iter) - 1):
                next_iter.append(last_iter[i])
                next_children.append([i])
                continue


            symbol1, symbol2 = last_iter[i], last_iter[i + 1]
            producing_rules = find_producing_rules(symbol1, symbol2)
            if producing_rules:
                skip_next = True
                next_iter.append(producing_rules)
                next_children.append([i, i + 1])
            else:
                next_iter.append(symbol1)
                next_children.append([i])

        prod_tree.append(map(expand_symbol, next_iter))
        children.append(next_children)
    
    # We have here a vert rudimentary parse tree
    prod_tree.reverse()
    return prod_tree
