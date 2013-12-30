from bear_tokens import *


def tokenize(input_str):
    ret_tokens = list()
    mytokenizer = Tokenizer(input_str)

    curr_token = mytokenizer.next_token()
    while curr_token.token_def != TokenDef.END_TOKENS:
        ret_tokens.append(curr_token)
        curr_token = mytokenizer.next_token()

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
            match = token.regex.match(self.input_str[self.curr_pos:])
            if match and token.type == WHITESPACE:
                self.curr_pos += match.end()
                return self.next_token()
            elif match:
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
            raise RuntimeError("Invalid token near char %d" % self.curr_pos)
