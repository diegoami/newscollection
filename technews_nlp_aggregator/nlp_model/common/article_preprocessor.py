import re



class TechArticlesPreprocessor():
    regexprs_year = [
        re.compile(r'\b(20|19)(\d+)\b')
    ]


    regexprs_hour = [
        re.compile(r'\b((1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp][Mm]))\b'),
        re.compile(r'\b((1[0-2]|0?[1-9]):([0-5][0-9])([AaPp][Mm]))\b'),
        re.compile(r'\b(1[0-2]|0?[1-9]):([0-5][0-9])\b'),
        re.compile(r'\b((1[0-2]|0?[1-9])-(1[0-2]|0?[1-9])([AaPp][Mm]))\b')
    ]

    regexprs_percentage = [
        re.compile(r'\b((\d+)(\.\d+)?)(?=%)\b')
    ]

    regexprs_percentage2 = [
        re.compile(r'\b((\d+)(\.\d+)?)\spercent\b')
    ]

    regexprs_money = [
        # re.compile(r'\b[\$\£\€]{1}(\d+)(\,\d+)?(\,\d+)?(\.\d+)?\b')
        re.compile(r'[\$\£\€]{1}(\d+)([\,\.]\d+)\b'),
        re.compile(r'[\$\£\€]{1}(\d+)\b')
    ]

    monthExpr = 'January|February|March|April|May|June|July|August|September|October|November|December'
    regexprs_dates = [
        re.compile(r'\b(%s)(\s[0-9]{1,2},\s20[0-9]{1,4}(th)?)' % monthExpr,re.VERBOSE),
        re.compile(r'\b(%s)(\s[0-9]{1,4})(th)?' % monthExpr,re.VERBOSE),
    ]

    regexprs_month = [
        re.compile(r'\bJanuary|February|March|April|May|June|July|August|September|October|November|December\b')
    ]

    regexprs_dayofweek = [
        re.compile(r'\bMonday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday\b')
    ]

    regexprs_decpart = [
        re.compile(r'(?<=\d)\.\d+\b'),
        re.compile(r'(?<=\d)\.\d+(?=[a-zA-Z])')
    ]
    digit_to_zero = str.maketrans("1234567890","0000000000")

    regexprs_year = [
        re.compile(r'\b(20)[01]\d\b'),
        re.compile(r'\b(19)[4-9]\d\b')

    ]

    regexprs_saxon = [
        re.compile(r'\B(s’)(?=\W)'),
    ]

    regexprs_saxon2 = [
        re.compile(r'(?<=\w)(’s)(?=\W)'),
    ]

    regexprs_hyphen = [
        re.compile(r'(?<=\w)(—)(?=\W)'),
    ]

    regexprs_url = [
        re.compile(r'\bhttp[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\b')
    ]

    def regexpr_func(self, str, regexprs):
        def replace_func(doc):
            for regexp in regexprs:
                doc = regexp.sub(str, doc)
            return doc
        return replace_func



    def process(self, doc):

        doc = self.regexpr_func('s', self.regexprs_saxon)(doc)
        doc = self.regexpr_func('', self.regexprs_saxon2)(doc)
        doc = self.regexpr_func('', self.regexprs_hyphen)(doc)
        doc = doc.replace("‘", '').replace("’", '').replace('“', '').replace('”', '')


        doc = self.regexpr_func('DATE', self.regexprs_dates)(doc)
        doc = self.regexpr_func('MONTH', self.regexprs_month)(doc)
        doc = self.regexpr_func('YEAR', self.regexprs_year)(doc)

        doc = self.regexpr_func('TIMEOFDAY',self.regexprs_hour)(doc)
        doc = self.regexpr_func('DAYOFWEEK', self.regexprs_dayofweek)(doc)


        doc = doc.translate(self.digit_to_zero)
        doc = self.regexpr_func('', self.regexprs_decpart)(doc)

        doc = self.regexpr_func('PERCENTAGE', self.regexprs_percentage)(doc)
        doc = self.regexpr_func('PERCENTAGE%', self.regexprs_percentage2)(doc)

        doc = self.regexpr_func('URL', self.regexprs_url)(doc)
        #doc = self.regexpr_func('#MONEY', self.regexprs_money)(doc)


        return doc



if __name__ == '__main__':
    prepr = TechArticlesPreprocessor()
    texts = [
      " 02:12 AM 03:14 PM 30% some other text  12.3% ",
      "I want 20 percent, 30 percent, 10 percent, 20% ",
      "$124,000 €243,23 £12.245 $124",
       "January 23, 2017 and March 6",
         "On January I went home until 2013 and woke up in 1972, then it was 2017 and not 201 ",
        " to optimize users’ mobile experience",
        " April 6th from 2-4pm I paid 30.32m to somebody ",
        " @somehandle has written with the tag #silent on twitter",
        " Visit us on http://www.amicabile.com to know more",
        "Uber’s new Asia chief wants to work with governments and taxi firms not against them",
        "While open source machine learning projects like Google's TensorFlow and Amazon's DSSTNE lower the bar"
    ]

    for text in texts:
        print(prepr.process(text))
