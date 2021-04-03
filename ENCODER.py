def find_rank(rank, number, alphabet_LIST):
    index = rank+number%len(alphabet_LIST)
    opp_index = len(alphabet_LIST)-index
    return alphabet_LIST[opp_index%len(alphabet_LIST)]

def setup_dictionary(dictionary, number, alphabet_CAP, alphabet_LOW):
    rank = 0
    for i in alphabet_CAP:
        dictionary.update([(i,find_rank(rank,number,alphabet_CAP))])
        rank+=1
    rank = 0
    for i in alphabet_LOW:
        dictionary.update([(i,find_rank(rank,number,alphabet_LOW))])
        rank+=1
def reverse(ANSWER):
    l = ""
    for i in ANSWER:
        l = i+l
    return l
    
    


alphabet_CAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_LOW = "abcdefghijklmnopqrstuvwxyz"

question = input("TYPE THE CODE: ")
permute = 0
for i in question:
    permute+=ord(i)



dictionary = {}

setup_dictionary(dictionary, permute, alphabet_CAP, alphabet_LOW)

ANSWER = ""

for i in question:
    try:
        ANSWER = ANSWER+str(dictionary[i])
    except:
        ANSWER = ANSWER+str(i)
ANSWER = reverse(ANSWER)
        
ANSWER = ANSWER + str(permute) + str(len(str(permute)))     
print(ANSWER)   
