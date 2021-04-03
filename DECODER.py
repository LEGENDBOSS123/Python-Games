
def reverse(ANSWER):
    l = ""
    for i in ANSWER:
        l = i+l
    return l

def get_number(question):
    l = int(question[-1])
    
    num = 0
    multi = 1
    question.pop()
    for i in range(l):
        num+=int(question[-1])*multi
        multi=multi*10
        question.pop()
    return num
def find_rank(rank, number, alphabet_LIST):
    index = rank+number%len(alphabet_LIST)
    opp_index = len(alphabet_LIST)-index
    return alphabet_LIST[opp_index%len(alphabet_LIST)]
def setup_dictionary(dictionary, number, alphabet_CAP, alphabet_LOW):
    rank = 0
    for i in alphabet_CAP:
        dictionary.update([(find_rank(rank,number,alphabet_CAP),i)])
        rank+=1
    rank = 0
    for i in alphabet_LOW:
        dictionary.update([(find_rank(rank,number,alphabet_LOW),i)])
        rank+=1
   
def decode(question, dictionary):
    ANSWER = ""

    for i in question:
        try:
            ANSWER = ANSWER+str(dictionary[i])
        except:
            ANSWER = ANSWER+str(i)
    
    return reverse(ANSWER)

alphabet_CAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_LOW = "abcdefghijklmnopqrstuvwxyz"
question = list(input("TYPE THE CODE: "))
number = get_number(question)%26

dictionary = {}
setup_dictionary(dictionary, number,alphabet_CAP,alphabet_LOW)

question = decode(question, dictionary)
print(question)
