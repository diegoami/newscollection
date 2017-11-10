class TokenizeInfo():
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def get_tokenized_article(self, title, doc):
        return self.tokenizer.tokenize_doc(title, doc)
