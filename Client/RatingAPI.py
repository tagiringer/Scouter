from bs4 import BeautifulSoup
import requests
import re

def trunc(input_string):
    val_ind = input_string.index('value=')
    
    length = len(input_string)
    value = input_string[val_ind:length]
    value = value[7:-3]

    if value.find("*") != -1:
        star_ind = value.index("*")
        return value[:-(len(value)-star_ind)]
    

    return value

def tournament_formatter(raw_tournament_output, inc):     

    res = re.split('<|>', raw_tournament_output)

    #print(res[8])

    # if len(res) < 38 and len(res) > 15:
    #     print("Failure at {}".format(inc))
    #     return
    # elif len(res) < 15:
    #     print('Too Small')
    #     return
    # elif res[8] is None:
    #     print('----NONE----')
    #     print(res[8])
    #     return
    # elif res[8] == r'\n':
    #     print(res[8])
    #     print('----/n----')
    #     return

    if len(res) < 38:        
        return

    


    if res[8] and res[16] and res[22] and res[28] and res[36] and res[30] and res[38]:

            fbs = res[28][:-7]
            fbq = res[36][:-7]

            tournament_dict = {
                "TournamentId":res[8],
                "TournamentName":res[16],
                "TournamentSection":res[22],
                "BeforeStandardRating":fbs,
                "AfterStandardRating":res[30],
                "BeforeQuickRating":fbq,
                "AfterQuickRating":res[38],
            }
    else:
        tournament_dict = {}
    

    return tournament_dict

def clean_tournaments(tournament_dict):
    # Cleans tournament information
    for t in range(1, len(tournament_dict.keys())):
        if tournament_dict.get(t) is None or len(tournament_dict.get(t)) == 0:
            tournament_dict.pop(t)

    # Renumbers the keys
    new_tournament_dict = {}    
   
    count = 0
    for item in tournament_dict.values():
        new_tournament_dict.update({count:item})
        count = count + 1   

    return new_tournament_dict



def get_tournament_history(uscf_id):

    url = "https://www.uschess.org/msa/MbrDtlTnmtHst.php?{}".format(uscf_id)
    r = requests.get(url)
    doc = BeautifulSoup(r.text, "html.parser")

    td_strings = doc.find_all('tr')

    i = 1
    raw_tournament_dict = {}
    for tournament in td_strings:        

        x = str(tournament)
        raw_tournament_dict.update({i:tournament_formatter(x, i)})
        i = i + 1
        
    
    for j in range(1, len(raw_tournament_dict.keys())):
        j_item = raw_tournament_dict.get(j, {})
        

    # Checks if tournament history is empty
    counter = 1
    for k in range(1, len(raw_tournament_dict.keys())):
        if raw_tournament_dict.get(k) is None or len(raw_tournament_dict.get(k)) == 0:
            counter = counter + 1
    
    if counter == len(raw_tournament_dict.keys()):
        print("No tournament history found")
        return
    
            
            


    master_tournament_dict = clean_tournaments(raw_tournament_dict)

    #print(master_tournament_dict)
    

    return master_tournament_dict
    

def get_rating_profile(uscf_id):
    url = "https://www.uschess.org/msa/thin.php"       

    r = requests.post(url, data={'memid':uscf_id, 'mode':"Lookup"})

    doc = BeautifulSoup(r.text, "html.parser")
    inputs_strings = doc.findAll('input')
    casted_inputs = []

    for element in inputs_strings:
        casted_inputs.append(str(element))


    rating_info = {
        "id":trunc(casted_inputs[0]),
        "name":trunc(casted_inputs[4]),
        "standard":trunc(casted_inputs[5]),
        "quick":trunc(casted_inputs[6])
    }

    return rating_info

def get_member_results(member_query_string):
    
    url = 'https://www.uschess.org/assets/msa_joomla/MbrLst.php'

    r = requests.post(url, data={'eMbrKey':member_query_string})
    doc = BeautifulSoup(r.text, "html.parser")

    res_strings = doc.findAll('pre')
    extract = res_strings.pop()
    rawMembers = extract.text.split('\n')

    members = []
    for member in rawMembers:
        uscfID = member.split(' ')[0]
        if uscfID.isdigit():
            members.append(member)

    dic = {}
    for member in members:
        memberDetails = member.split(' ')
        uscf_id = memberDetails.pop(0)
        dic.update({uscf_id: memberDetails})

    print(dic)
    return dic

    



        
        







#uscf_id = '11292097'

#print(get_rating_profile('15014980'))

#get_tournament_history("15014980")
#get_tournament_history("15014995")
#get_tournament_history("11292097")









