'''This is a code I wrote where I could not use
any packages to work with data files. To see the questions I attempted to answer,
please see the Question.pdf file in the Data Handling Code file.
Excuting the code will print out the answers. I am proud of this code because I am so used
to depending on packages in pyhton  but having the chance to not use a package and write code
from scratch helped me better understand the theory behind a lot of the packages I use, like pandas.'''

def main():

    #all Diabetes fields

    inpatient_columns = ['ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1',  'ICD9_DGNS_CD_2',  'ICD9_DGNS_CD_3',  'ICD9_DGNS_CD_4',  'ICD9_DGNS_CD_5',  'ICD9_DGNS_CD_6',  'ICD9_DGNS_CD_7',  'ICD9_DGNS_CD_8',  'ICD9_DGNS_CD_9',  'ICD9_DGNS_CD_10' ]
    outpatient_columns = ['ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1',  'ICD9_DGNS_CD_2',  'ICD9_DGNS_CD_3',  'ICD9_DGNS_CD_4',  'ICD9_DGNS_CD_5',  'ICD9_DGNS_CD_6',  'ICD9_DGNS_CD_7',  'ICD9_DGNS_CD_8',  'ICD9_DGNS_CD_9',  'ICD9_DGNS_CD_10' ]
    carrier_columns = ['ICD9_DGNS_CD_1', 'ICD9_DGNS_CD_2', 'ICD9_DGNS_CD_3', 'ICD9_DGNS_CD_4','ICD9_DGNS_CD_5', 'ICD9_DGNS_CD_6', 'ICD9_DGNS_CD_7',
                   'ICD9_DGNS_CD_8',  'LINE_ICD9_DGNS_CD_1', 'LINE_ICD9_DGNS_CD_2', 'LINE_ICD9_DGNS_CD_3', 'LINE_ICD9_DGNS_CD_4', 'LINE_ICD9_DGNS_CD_5','LINE_ICD9_DGNS_CD_6', 'LINE_ICD9_DGNS_CD_7', 'LINE_ICD9_DGNS_CD_8', 'LINE_ICD9_DGNS_CD_9', 'LINE_ICD9_DGNS_CD_10', 'LINE_ICD9_DGNS_CD_11', 'LINE_ICD9_DGNS_CD_12', 'LINE_ICD9_DGNS_CD_13']

    #import all files

    inpatient=file_to_list('raw/inpatient/inpatient.txt')
    outpatient=file_to_list('raw//outpatient/outpatient.txt')
    carrier= file_to_list('raw/carrier/carrier.txt')
    beneficiary=file_to_list('raw/beneficiary/beneficiary.txt')
    prescription=file_to_list('raw/prescription/prescription.txt')
    li = [i.strip() for i in open("lookup/lovastatin.txt").readlines()]

    total = inpatient+outpatient+carrier


    '''Question 1'''
    #get all claims from 2009
    inpatient_nine= date_search(inpatient)
    outpatient_nine= date_search(outpatient)
    carrier_nine= date_search(carrier)

    #get all 2009 claims that are for diabetic members
    inpatient_search= code_search(inpatient_nine, inpatient_columns)
    outpatient_search= code_search(outpatient_nine, outpatient_columns)
    carrier_search= code_search(carrier_nine, carrier_columns)

    #get all unique members in Node 1
    node_1 = inpatient_search + outpatient_search + carrier_search
    un=unique_members(node_1)

    '''Question 2'''

    lovastatin_prescribe = []
    for q in prescription:
        if q['PROD_SRVC_ID'] in li:
            lovastatin_prescribe.append(q)
    node_2 = []
    for n in node_1:
        for l in lovastatin_prescribe:
            if n['DESYNPUF_ID'] == l['DESYNPUF_ID']:
                dt1= Date(n['CLM_FROM_DT'])
                dt2= Date(l['SRVC_DT'])
                dtdiff=getDifference(dt2, dt1)
                if 0<= dtdiff <=365:
                    node_2.append(n)

    ui_2=unique_members(node_2)
    '''Question 3'''
    node_3 = []
    for member in node_2:
        for bene in beneficiary:
            if member['DESYNPUF_ID'] == bene['DESYNPUF_ID']:
                did= Date(member['CLM_FROM_DT'])
                dob= Date(bene['BENE_BIRTH_DT'])
                age= getDifference(did, dob)
                age = age/365
                if age >= 65:
                    node_3.append(member)

    ui_3=unique_members(node_3)
    return ("There are {} unique patients in Node 1, {} unique patients in Node 2 and {} unique patients in Node 3.".format(len(un), len(ui_2), len(ui_3)))


'''Function to turn each file into a list of dictionaries'''

def file_to_list(file_path):
    my_list = []
    with open(file_path, 'r') as i:
        lines = i.readlines() # list containing lines of file
        columns = [] # To store column names

        i = 1
        for line in lines:
            line = line.strip() # remove leading/trailing white spaces
            if line:
                if i == 1:
                    columns = [item.strip() for item in line.split(',')]
                    i = i + 1
                else:
                    d = {} # dictionary to store file data (each line)
                    data = [item.strip() for item in line.split(',')]
                    for index, elem in enumerate(data):
                        d[columns[index]] = data[index]
                    my_list.append(d)
    return my_list

'''Function to find dates that are in 2009'''

def date_search(list):
    nine_list = []
    for p in list:
        if p['CLM_FROM_DT'].startswith('2009'):
            nine_list.append(p)
    return nine_list


'''Function to search for diabetes code in multiple columns'''
def code_search(my_list, columns):
    diabetes = []
    for p in my_list:
        for i in columns:
            if p[i].startswith('250'):
                diabetes.append(p)
    return diabetes


'''CLASS TO CALCULATE DATE DIFFERENCES'''

class Date:
    def __init__(self, date):
        date = str(date)
        self.y = int(date[0:4])
        self.m = int(date[4:6])
        self.d = int(date[-2:])
monthDays = [31, 28, 31, 30, 31, 30,
                        31, 31, 30, 31, 30, 31 ]
#account for Leap Years
def countLeapYears(d):

    years = d.y
    if (d.m <= 2) :
        years-= 1
    return int(years / 4 - years / 100 + years / 400 )

#Get Date Difference
def getDifference(dt1, dt2) :


    n1 = dt1.y * 365 + dt1.d

    for i in range(0, dt1.m - 1) :
        n1 += monthDays[i]

    n1 += countLeapYears(dt1)

    n2 = dt2.y * 365 + dt2.d
    for i in range(0, dt2.m - 1) :
        n2 += monthDays[i]
    n2 += countLeapYears(dt2)

    return (n1 - n2)

'''Function to get count of unique members in each node'''
def unique_members(ls):
    auxiliaryList = []
    for word in ls:
        if word['DESYNPUF_ID']  not in auxiliaryList:
            auxiliaryList.append(word['DESYNPUF_ID'])
    return auxiliaryList


if __name__ == '__main__':
   result= main()
   print(result)
