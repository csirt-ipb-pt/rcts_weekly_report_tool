import os
import csv
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weekly_reports.settings')
django.setup()
from reports.models import Mal, Other, Vul, Record

path = os.getcwd() # Obtains the directory path where the script is stored.
fileToSearch = list((str(path) + '/upload/all_other.csv', str(path) + '/upload/all_mal.csv', str(path) + '/upload/all_vul.csv')) # List of files to create.
table = list((Other.objects.all(), Mal.objects.all(), Vul.objects.all(), Record.objects.all())) # List of DB Tables
# For loop that extracts the contents of the database and stores them on individual .csv files.
for num in range(0, len(fileToSearch)):
    try:
        with open(fileToSearch[num], 'w+', newline='') as tempFile:
            value = table[num]

            if num != 3:
                writer = csv.writer(tempFile)
                if num == 0 or num == 1:
                    writer.writerow(['source ip', 'source time'])
                elif num == 2:
                    writer.writerow(['source ip', 'source port', 'source time'])

            for ip in value:
                if num == 0 or num == 1:
                    for i in range(0, int(ip.count)):
                        if i == (int(ip.count) - 1):
                            writer.writerow([ip.ip, ip.data_2])
                        else:
                            writer.writerow([ip.ip, ip.data_1])
                elif num == 2:
                    for i in range(0, int(ip.count)):
                        if i == (int(ip.count) - 1):
                            writer.writerow([ip.ip, ip.port, ip.data_2])
                        else:
                            writer.writerow([ip.ip, ip.port, ip.data_1])

    except IOError:
        print(f"File \"{fileToSearch[num]}\" Can't Be Accessed!")