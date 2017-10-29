import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

excl_1 = [',', 'the', '.', 'to', 'and', 'a', 'of', '’', 'in', 'that', 's', 'it', 'is', 'for', 'with', 'on', 'you', 'as', '“', '”', 'be', 'this', 'but', 'are', 'from',  'its', 'at', 'can', 'an', 'have', 'we', 'has', 'i', 'by', 't',  'your', 'or', 'was', 'they', '—', ':', '(', ')', 'their', 'like', 'which', 'not', 'one', 'also','will']
excl_2 = ['about', 'if', 'what', 'up', 'so', 'there', 'all', 'he', 'said', 'other', 'some', 'just', 'when', 'into',  'been', 'how', 'now', 'than', 'them',  'said',  'while', 'who', 'our',   'get', 're', 'could',  'use', 'would', 'way', 'only', 'make', '?', 'his']

excl_3 = [ 'do', 'these', 'says', 'were', 'had',  'see', 'after', 'us', 'no', 'where', 'may', 'through', 'those',  'my', 'don', 'two',  'because',  'll', 'same', 'take',  'around',  'made',  '–',  'then', 'both', 'any', ';',  'before', 'going', 'being',  'here', 'able',  'down', 'lot', 'right', 'she', 'her']

excl_4 = ['-','@','\'s','``','\'\'' ,'&', '\'', '`', '!', '[', ']', '‘', '=', '…']

not_excl_1 =['need', 'using', 'more', 'new', '$', 'company', 'out','people','google','time', 'data', 'app', 'game', 'service', 'video'
             'companies', 'apple', 'over', 'million', 'first', 'year', 'even', 'most', 'much', 'users', 'well', 'today', 'technology', 'last', 'want'
            ,'many','world', 'work','ai', 'still', 'own', 'help', 'team','years', 'back', 'games','market', 'uber',  'better', 'part', 'product', 'facebook', 'might',
            'very', 'good', 'think', 'vr', 've','next', '2017', 'something', 'including', 'amazon', 'tech',
             'business','startup', 'billion', 'since', 'watch', 'mobile']


excl_all = excl_1 + excl_2 + excl_3 + excl_4
class SimpleTokenExcluder:

    def process(self,token_list):
        return token_list

    def is_token_allowed(self, token):
        return True


class TechArticlesTokenExcluder:

    def process(self,token_list):
        logging.info("Tokens before pruning : {}".format(len(token_list)))
        tokens_after = [ t for t in token_list if t not in excl_all]
        logging.info("Tokens after pruning : {}".format(len(tokens_after)))
        return tokens_after

    def is_token_allowed(self, token):
        return token not in excl_all

