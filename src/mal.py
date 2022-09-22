import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weekly_reports.settings')
django.setup()
import pandas as pd
from reports.models import Mal
from network_infrastructure import network_names, network_range

path = os.getcwd() # Obtains the directory path where the script is stored.
filedict = dict([]) # Dictionary where the information extracted from the .csv file will be stored.
wordlist = network_names # A list containing the names of the networks.

ip_dict = network_range # Dictionary composed of network names, and their respective ranges.

fileToSearch = (str(path) + '/upload/mal.csv') # Tuple that joins the directory path where the script is located and the subdirectories and name of the .csv file.
print(fileToSearch)
# Function that removes "." of the IPs and returns them.
def convert_ipv4(ip):
    return tuple(int(n) for n in ip.split('.'))
# Function that compares the IP with the Network range.
def check_ipv4_in(addr, start, end):
    return convert_ipv4(start) <= convert_ipv4(addr) <= convert_ipv4(end)
#1 Function that opens the file and extracts the predefined columns and their respective values. Once this is done, it stores them in the dictionary mentioned above.
def openfiles(filedict):
    for i in range(0, 2):
        if i == 0:
            colnames = ['source ip']
        elif i == 1:
            colnames = ['source time']
        stringOld = [ ]
        try:
            tempFile = open( fileToSearch, 'r+' )
        except IOError:
            print(f"File \"{fileToSearch}\" Can't Be Accessed!")
        else:
            with tempFile:
                df = pd.read_csv(fileToSearch, skipinitialspace=True, usecols=colnames)
                if i == 0:
                    print(f"Total Records From File: {len(df.index)}.")
                for row in df.index:
                    word = "".join(df.loc[row].values)
                    stringOld.append(word)
            filedict[i]=stringOld
#2 Function that compares the IPs from the db with the second to see if there are persistent IPs. It returns a dictionary containing the persistent IPs and their respective information stored on the db.
def Comp(stringtwo, persistent):
    total = 0
    new_mal = Mal.objects.all()
    print("The Following IPs Are Persistent And Contain The Following Data In The Database:")
    for ip in new_mal:
        if ip.ip in stringtwo:
            total += 1
            print(f"Persistent IP: {ip.ip} - {ip.rede} - {ip.data_1} - {ip.data_2} - {ip.count}.")
            persistent[ip.ip] = (ip.rede, ip.data_1, ip.data_2, ip.count)
    print(f"Total Persistent IPs: {total}.")
#3 Function that compares the IPs from the .csv file and sees in which network it belongs to. It returns a dictionary containing that information.
def ListThem(stringcom, rede):
    cont = 0
    stringone = stringcom
    for z in stringone:
        cont += 1
        for i in range(0, len(wordlist)):
            x = tuple(ip_dict[wordlist[i]])
            if check_ipv4_in(z, *x) == True:
                rede[z] = network_names[i]
                break
#4 Function that creates a dictionary with the IPs, the network which it belongs to, the first and last time it was registered on the .csv file, and the total number of occurrences.
def create_dict(filedict, listdic, rede):
    stringCreate = filedict[0]
    stringDate = filedict[1]
    stringcom = list(set(filedict[0]))
    sortedDict = dict([])
    sortedDate = dict([])

    for ip in stringcom:
        num = list()
        for z in range(0, len(stringCreate)):
            if stringCreate[z] == ip:
                num.append(z)
        sortedDict[ip] = (num)

    for d in stringcom:
        val = list(sortedDict[d])
        Date1 = stringDate[val[0]]
        Date2 = ""
        for w in range(0, len(val)):
            if  stringDate[val[w]] <= Date1:
                Date1 = stringDate[val[w]]
            if stringDate[val[w]] >= Date2:
                Date2 = stringDate[val[w]]
        sortedDate[d] = Date1, Date2

    for i in range(0, len(stringcom)):
        Date = sortedDate[stringcom[i]]
        Date1 = Date[0]
        Date2 = Date[1]
        listdic[i] = stringcom[i], rede[stringcom[i]], Date1, Date2, len(sortedDict[stringcom[i]])
#5 Function that imports the information extracted from the .csv file to the db. It checks whether the IP is persistent and updates its fields in the db, or creates new entries.
def import_to_db(listdic, persistent):
    for i in range(0, len(listdic)):
        sclice = list(listdic[i])
        if sclice[0] in persistent:
            data = persistent[sclice[0]]
            Mal.objects.filter(ip=sclice[0]).update(rede= sclice[1])
            if sclice[2] <= data[1]:
                Mal.objects.filter(ip=sclice[0]).update(data_1= sclice[2])
            if sclice[3] >= data[2]:
                Mal.objects.filter(ip=sclice[0]).update(data_2= sclice[3])
            val = int(data[3])
            value = val + sclice[4]
            Mal.objects.filter(ip=sclice[0]).update(count= value)
        else:
            new_mal = Mal(ip=sclice[0], rede=sclice[1], data_1=sclice[2], data_2=sclice[3], count=sclice[4])
            new_mal.save()
#6 Main function that contains local variables to store and pass the information to the previous functions. In the end it prints on the screen the information extracted of the .csv files.
def main(filedict):
    listdic = dict([])
    rede = dict([])
    persistent = dict([])
    openfiles(filedict)
    stringNew = list(set(filedict[0]))
    print(f"Total IPs: {len(stringNew)}.")
    Comp(stringNew, persistent)
    ListThem(stringNew, rede)
    create_dict(filedict, listdic, rede)
    print("IPs Extracted From The Report And Their Data:")
    for i in range(0, len(listdic)):
        sclice = list(listdic[i])
        print(f"{i + 1} - {sclice}")
    import_to_db(listdic, persistent)
# Invocation of the main function.
main(filedict)