"""
Author: Jim Soiland
Date: 8/6/2016
Purpose: Text-mining exercise with medical notes
    *parses strings with dates of many formats (See below)
    *ranks the original input data by the dates in each string
    *Can assume anything formatted XX/XX/XX is MM/DD/YY
    *Anything marked with blank month or year is the 
        first of that month and year respectively
"""
def date_sorter():
    """This function will read in a file with a bunch of strings from ddates.txt.
    Each line of the file has a date in one of many formats:
        #first four captured by exp_1
        test_string = 'This String has many dates. 04/20/2009; 04/20/09; 4/20/09; 4/3/09; 6/2008; 12/2009;'
        #next four captured by exp_2
        test_string += 'Feb 2009; Sep 2009; Oct 2010'
        test_string += 'Mar-20-2009; Mar 20, 2009; March 20, 2009; Mar. 20, 2009; Mar 20 2009;'
        test_string += 'Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009'
        test_string += ' 2009; 2010'  
    The point of this function is to sort the index based on the dates in each line of the file
    where the row number of the file is the starting index"""
    import pandas as pd
    import re
    import numpy as np
    import string
    import datetime
    pd.options.display.max_colwidth = 999
    months = '(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
    months_dict = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    month_abbrevs={'Jan':'January',
                   'Feb':'February',
                   'Mar':'March',
                   'Apr':'April',
                   'May:':'May',
                   'Jun':'June',
                   'Jul':'July',
                   'Aug':'August',
                   'Sep':'September',
                   'Oct':'October',
                   'Nov':'November',
                   'Dec':'December'}
    numeric_suffixes = '(?:st|nd|rd|th)'
    doc = []
    with open('dates.txt') as file:
        for line in file:
            doc.append(line)

    def make_date(p_string):
        #now we have a bunch of dates
        #but they're saved in various formats
        #so lets try and format them
        some_date = datetime.datetime.strptime('01Jan1900', '%d%b%Y').date()
        format_list = []
        format_list.append('%d%b%Y')
        format_list.append('%b%Y')
        format_list.append('%b%d%Y')
        format_list.append('%m/%d/%Y')
        format_list.append('%m/%d/%y')
        format_list.append('%m/%Y')
        format_list.append('%Y')
        for format_str in format_list:   
            try:
                #dayMMMYear
                some_date = datetime.datetime.strptime(p_string, format_str).date()
            except:
                pass
        return some_date

    def extract_dates(p_string):
        t=re.findall(full_exp,p_string)
        t.sort(key = lambda s: len(s), reverse=True)
        #t is a list of *potential* dates
        #loop through the list to find a valid date
        for maybe_date in t:
            my_string= re.sub('[,.]','',maybe_date)
            my_string= re.sub('[-]','/',my_string)
            for token in my_string.split():  
                for abbr in month_abbrevs:
                    if token.startswith(abbr):
                        my_string=re.sub(token,abbr,my_string)
                    else:
                        junk=0
            my_string=re.sub(' ','',my_string) 
            date_val=make_date(my_string)
            if date_val > datetime.datetime.strptime('01Jan1900', '%d%b%Y').date():
                return date_val
            else:
                junk=0
        return date_val



    search_expr=[]
    search_expr.append('\d{1,2}'+numeric_suffixes+'?[, ]+'+
         months+'[a-z]*[., ]+\d{2,4}')
    #Another permutation using abbreviations: this time with month, day, year
    search_expr.append(months+'[a-z]*[. -]*\d{1,2}'+numeric_suffixes+'?(?:[, -]+\d{1,4})')
    #parse just text based month an year. This has to be a separate expression because
    #if the above expressions have their day numbers set to optional, each will detect and 
    #overly simplified version of the other
    search_expr.append( months+'[a-z]*[. ]*(?:[, ]+\d{1,4})')
    #finally, just detect numbers. This is the least sensitive soit has to be tacked onto the end
    search_expr.append('[0-1]?\d{1}[/-]\d{1,2}[/-]?\d{2,4}')
    search_expr.append('\d{4}')
    full_exp = '|'.join(search_expr)
    data = pd.DataFrame(doc,columns=['text'])
    data['the_date'] = data['text'].apply(lambda x: extract_dates(x))
    data['ind_val'] = data.index
    data.sort_values(['the_date','ind_val'],inplace=True)
    return data.index