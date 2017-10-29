class TokenizeInfo():
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def get_tokenized_article(self, title, document):
        return self.tokenizer.tokenize_doc(title, document)
