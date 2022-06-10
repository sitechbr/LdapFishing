import csv
import os
from datetime import date
import GetLdapEmail
import SendMes

def ch_org():
    ch = ''
    switcher = {
        1: "CIT",
        2: "ADM",
        3: "OBR",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    while True:
        print("""Choosing an organization 
                          1: Центр информационных технологий
                          2: ADM
                          0: EXIT""")
        ch = int(input())
        if ch in switcher:
            data = GetLdapEmail.selectAd(switcher.get(ch))
            gen_csv(data,switcher.get(ch))
            main_menu()
        else:
            print ("Code not found")



def gen_csv(data,org):
    PATH = 'result'
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    f = open(f"./result/{org} {date.today()}.csv",'w')
    f.writelines("%s\n" % row for row in data)
    f.close()

def chFile2Send():
    PATH = './sender/'
    files ={}
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    print ("""Do you want to specify the path to the email folder?
            Default: ./sender(y/n)""")
    ch = input()
    match ch:
       case "y":
            PATH = input()
       case _:
            print(PATH)
    ls = os.listdir(PATH)
    i= 1
    print ("Select file:")
    for name in ls:
        print (f"press {i} to select {name}")
        files[i] = name
        i+=1
    print ("Input 0 to exit main menu")

    try:
        ch = int(input())
    except ValueError:
        print("did you make the right choice?")

    if ch in files:
        fileCSV = PATH + files.get(ch)
        read_csv(fileCSV)
    else:
        main_menu()

def read_csv(file):
    emails={}
    with open(file, encoding="utf-8") as csvfile:
        reader =csv.DictReader(csvfile)
        for row in reader:
            if "Submit" in row['status']:
                print(f"{row['email']}:{row['first_name']}")
                emails[row['email']] = row['first_name']
        print ("send message (y/n)")
        ch = input()
        match ch:
            case "y":
                for email, name in emails.items():
                    print(email, '->', name)
                    #SendMes.send(email,name)
            case _:
                main_menu()




def main_menu():
    ch = -1
    while (ch != 0):
        print("""Enter 
                      1: generate csv file to fishing"
                      2: send message to users
                      0: exit""")

        try:
            ch = int(input())
        except ValueError:
            print("did you make the right choice?")
        match ch:
            case 1:
                ch_org()
            case 2:
                chFile2Send()
            case 0:
                exit()
            case _:
                print("Code not found")


if __name__ == '__main__':
    main_menu()
