import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weekly_reports.settings')
django.setup()
import pandas as pd
from reports.models import Vul
from network_infrastructure import network_names, network_range
from ipv4 import ListThem

path = os.getcwd() # Obtains the directory path where the script is stored.
filedict = dict([]) # Dictionary where the information extracted from the .csv file will be stored.
fileToSearch = (str(path) + '/upload/vul.csv') # Tuple that joins the directory path where the script is located and the subdirectories and name of the .csv file.
print(fileToSearch)
#1 Function that opens the file and extracts the predefined columns and their respective values. Once this is done, it stores them in the dictionary mentioned above.
def openfiles(filedict):
    for i in range(0, 3):
        if i == 0:
            colnames = ['source ip']
        elif i == 1:
            colnames = ['source time']
        elif i == 2:
            colnames = ['source port']
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
                    if i == 2:
                        word = "".join(str(df.loc[row].values))
                    else:
                        word = "".join(df.loc[row].values)
                    stringOld.append(word)
            filedict[i]=stringOld
#2 Function that compares the IPs from the db with the second to see if there are persistent IPs. It returns a dictionary containing the persistent IPs and their respective information stored on the db.
def Comp(stringtwo, persistent):
    total = 0
    new_vul = Vul.objects.all()
    print("The Following IPs Are Persistent And Contain The Following Data In The Database:")
    for ip in new_vul:
        if ip.ip in stringtwo:
            total += 1
            print(f"Persistent IP: {ip.ip} - {ip.port} - {ip.rede} - {ip.data_1} - {ip.data_2} - {ip.count}.")
            persistent[ip.ip] = (ip.port, ip.rede, ip.data_1, ip.data_2, ip.count)
    print(f"Total Persistent IPs: {total}.")
#3 Function that creates a dictionary with the IPs, the network which it belongs to, the first and last time it was registered on the .csv file, and the total number of occurrences.
def create_dict(filedict, listdic, rede):
    stringCreate = filedict[0]
    stringDate = filedict[1]
    stringPort = filedict[2]
    stringcom = list(set(filedict[0]))
    sortedDict = dict([])
    sortedDate = dict([])
    sortedPort = dict([])

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
            port = stringPort[val[w]]
            port = port.split('[')
            value = port[1]
            value = value.split(']')
            port = value[0]
        sortedPort[d] = port
        sortedDate[d] = Date1, Date2

    for i in range(0, len(stringcom)):
        port = sortedPort[stringcom[i]]
        Date = sortedDate[stringcom[i]]
        Date1 = Date[0]
        Date2 = Date[1]
        listdic[i] = stringcom[i], port, rede[stringcom[i]], Date1, Date2, len(sortedDict[stringcom[i]])
#4 Function that imports the information extracted from the .csv file to the db. It checks whether the IP is persistent and updates its fields in the db, or creates new entries.
def import_to_db(listdic, persistent):
    for i in range(0, len(listdic)):
        sclice = list(listdic[i])
        if sclice[0] in persistent:
            data = persistent[sclice[0]]
            Vul.objects.filter(ip=sclice[0]).update(port= sclice[1])
            Vul.objects.filter(ip=sclice[0]).update(rede= sclice[2])
            if sclice[3] <= data[2]:
                Vul.objects.filter(ip=sclice[0]).update(data_1= sclice[3])
            if sclice[4] >= data[3]:
                Vul.objects.filter(ip=sclice[0]).update(data_2= sclice[4])
            val = int(data[4])
            value = val + sclice[5]
            Vul.objects.filter(ip=sclice[0]).update(count= value)
        else:
            new_vul = Vul(ip=sclice[0], port=sclice[1], rede=sclice[2], data_1=sclice[3], data_2=sclice[4], count=sclice[5])
            new_vul.save()
#5 Main function that contains local variables to store and pass the information to the previous functions. In the end it prints on the screen the information extracted of the .csv files.
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
main(filedict) # Invocation of the main function.