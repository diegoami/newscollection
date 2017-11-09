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
        re.compile(r'\b(%s)(\s[0-9]{1,2},\s20[0-9]{1,2}(th)?)\b' % monthExpr,re.VERBOSE),
        re.compile(r'\b(%s)(\s[0-9]{1,2})(th)?\b' % monthExpr,re.VERBOSE),


    ]

    regexprs_month = [
        re.compile(r'\bJanuary|February|March|April|May|June|July|August|September|October|November|December\b')
    ]

    regexprs_year = [
        re.compile(r'\b(20)[01]\d\b'),
        re.compile(r'\b(19)[4-9]\d\b')

    ]

    regexprs_saxon = [
        re.compile(r'\B(s’)(?=\W)')
    ]

    def replace_hours(self, doc):
        for regexp in self.regexprs_hour:
            doc = regexp.sub('#TIMEOFDAY', doc)

        return doc

    def replace_percentage(self, doc):
        for regexp in self.regexprs_percentage:
            doc = regexp.sub('#PERCENTAGE', doc)

        for regexp in self.regexprs_percentage2:
            doc = regexp.sub('#PERCENTAGE%', doc)


        return doc


    def replace_money(self, doc):
        for regexp in self.regexprs_money:
            doc = regexp.sub('#MONEY', doc)
        return doc

    def replace_dates(self, doc):
        for regexp in self.regexprs_dates:
            doc = regexp.sub('#DATE', doc)
        return doc

    def replace_months(self, doc):
        for regexp in self.regexprs_month:
            doc = regexp.sub('#MONTH', doc)
        return doc

    def replace_years(self, doc):
        for regexp in self.regexprs_year:
            doc = regexp.sub('#YEAR', doc)
        return doc

    def replace_asaxon(self, doc):
        for regexp in self.regexprs_saxon:
            doc = regexp.sub('s', doc)
        return doc

    def process(self, doc):
        doc = doc.replace("‘", '').replace("’", '')
        doc = self.replace_hours(doc)
        doc = self.replace_percentage(doc)
        doc = self.replace_money(doc)
        doc = self.replace_dates(doc)
        doc = self.replace_months(doc)
        doc = self.replace_years(doc)
        doc = self.replace_asaxon(doc)

        return doc



if __name__ == '__main__':
    prepr = TechArticlesPreprocessor()
    text =" 02:12 AM 03:14 PM 30% some other text  12.3% "
    text2 = "I want 20 percent, 30 percent, 10 percent, 20% "
    text3 = "$124,000 €243,23 £12.245 $124"
    text4  = "January 23, 2017 and March 6"
    text5 = "On January I went home until 2013 and woke up in 1972, then it was 2017 and not 201 "
    text6 = " to optimize users’ mobile experience"
    text7 = " April 6th from 2-4pm"

    print(prepr.process(text))
    print(prepr.process(text2))
    print(prepr.process(text3))
    print(prepr.process(text4))
    print(prepr.process(text5))
    print(prepr.process(text6))
    print(prepr.process(text7))
