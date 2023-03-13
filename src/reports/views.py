import sys
import os
import random
import mimetypes
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Other, Vul, Mal, Search
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OtherSerializer, MalSerializer, VulSerializer, SearchSerializer
from subprocess import run,PIPE
from network_infrastructure import network_names, network_range
from ipv4 import check_ipv4_in

# Create your views here.
path = os.getcwd() # Obtains the directory path.
password = os.environ.get('PASSWORD') # Password to protect the content inside the zip file.
fileToSearch = [(str(path) + '/upload/other.csv'), (str(path) + '/upload/vul.csv'), (str(path) + '/upload/mal.csv'), (str(path) + '/upload/other.txt'), (str(path) + '/upload/vul.txt'), (str(path) + '/upload/mal.txt'), (str(path) + '/upload/csv.zip'), (str(path) + '/upload/all_other.csv'), (str(path) + '/upload/all_mal.csv'), (str(path) + '/upload/all_vul.csv')] # List that joins the directory path and the subdirectories and names of the .csv files.

# Function that checks if the IP belongs to a network.
def ListThem(ip, rede):
    for i in range(0, len(network_names)):
        x = tuple(network_range[network_names[i]])
        if check_ipv4_in(ip, *x) == True:
            rede[ip] = network_names[i]
            break

# Search API.
class SearchAPIView(APIView):
    serializer_class = SearchSerializer

    def get_queryset(self):
            search = Search.objects.all()
            return search

    def get(self, request, *args, **kwargs):
        try:
            ip = request.query_params.get('ip')
            if ip != None and ip != "":
                r = dict([])
                try:
                    ListThem(ip, r)
                except:
                    message = str(f"IP: {ip} does not belong to any of the defined Networks!")
                    return Response(message)
                else:
                    if ip not in r.keys():
                        message = str(f"IP: {ip} does not belong to any of the defined Networks!")
                    else:
                        message = str(f"IP: {ip} belongs to Network: {r[ip]} - {network_range[r[ip]][0]} - {network_range[r[ip]][1]}")
                    return Response(message)
            else:
                message = None
                return Response(message)
        except:
            message = None
            return Response(message)

# Other API.
class OtherAPIView(APIView):
    serializer_class = OtherSerializer

    def get_queryset(self):
        other = Other.objects.all()
        return other

    def get(self, request, *args, **kwargs):
        try:
            ip = request.query_params.get('ip')
            if ip != None:
                try:
                    other = Other.objects.get(ip=ip)
                except:
                    message = str(f"No IP {ip} on the Database!")
                    return Response(message)
                else:
                    serializer = OtherSerializer(other)
            else:
                other = self.get_queryset()
                serializer = OtherSerializer(other, many=True)
        except:
            other = self.get_queryset()
            serializer = OtherSerializer(other, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        other_data = request.data

        try:
            other = Other.objects.get(ip=other_data["ip"])
            if other != None:
                message = str("IP already exist on the Database!")

                return Response(message)
        except:
            new_other = Other.objects.create(ip=other_data["ip"], rede=other_data["rede"], data_1=other_data["data_1"], data_2=other_data["data_2"], count=other_data["count"])

            new_other.save()
            serializer = OtherSerializer(new_other)

            return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        ip = request.query_params.get('ip')
        try:
            other_object = Other.objects.get(ip=ip)
        except:
            message = str(f"No IP {ip} on the Database!")
            return Response(message)
        else:
            data = request.data

            other_object.rede = data["rede"]
            other_object.data_1 = data["data_1"]
            other_object.data_2 = data["data_2"]
            other_object.count = data["count"]

            other_object.save()

            serializer = OtherSerializer(other_object)
        return Response(serializer.data)

# Malware API.
class MalAPIView(APIView):
    serializer_class = MalSerializer

    def get_queryset(self):
        mal = Mal.objects.all()
        return mal

    def get(self, request, *args, **kwargs):
        try:
            ip = request.query_params.get('ip')
            if ip != None:
                try:
                    mal = Mal.objects.get(ip=ip)
                except:
                    message = str(f"No IP {ip} on the Database!")
                    return Response(message)
                else:
                    serializer = MalSerializer(mal)
            else:
                mal = self.get_queryset()
                serializer = MalSerializer(mal, many=True)
        except:
            mal = self.get_queryset()
            serializer = MalSerializer(mal, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        mal_data = request.data

        try:
            mal = Mal.objects.get(ip=mal_data["ip"])
            if mal != None:
                message = str("IP already exist on the Database!")

                return Response(message)
        except:
            new_mal = Mal.objects.create(ip=mal_data["ip"], rede=mal_data["rede"], data_1=mal_data["data_1"], data_2=mal_data["data_2"], count=mal_data["count"])

            new_mal.save()
            serializer = MalSerializer(new_mal)

            return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        ip = request.query_params.get('ip')
        try:
            mal_object = Mal.objects.get(ip=ip)
        except:
            message = str(f"No IP {ip} on the Database!")
            return Response(message)
        else:
            data = request.data

            mal_object.rede = data["rede"]
            mal_object.data_1 = data["data_1"]
            mal_object.data_2 = data["data_2"]
            mal_object.count = data["count"]

            mal_object.save()

            serializer = MalSerializer(mal_object)
        return Response(serializer.data)

# Vulnerability API.
class VulAPIView(APIView):
    serializer_class = VulSerializer

    def get_queryset(self):
        vul = Vul.objects.all()
        return vul

    def get(self, request, *args, **kwargs):
        try:
            ip = request.query_params.get('ip')
            if ip != None:
                try:
                    vul = Vul.objects.get(ip=ip)
                except:
                    message = str(f"No IP {ip} on the Database!")
                    return Response(message)
                else:
                    serializer = VulSerializer(vul)
            else:
                vul = self.get_queryset()
                serializer = VulSerializer(vul, many=True)
        except:
            vul = self.get_queryset()
            serializer = VulSerializer(vul, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        vul_data = request.data

        try:
            vul = Vul.objects.get(ip=vul_data["ip"])
            if vul != None:
                message = str("IP already exist on the Database!")

                return Response(message)
        except:
            new_vul = Vul.objects.create(ip=vul_data["ip"], port=vul_data["port"], rede=vul_data["rede"], data_1=vul_data["data_1"], data_2=vul_data["data_2"], count=vul_data["count"])

            new_vul.save()
            serializer = VulSerializer(new_vul)

            return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        ip = request.query_params.get('ip')
        try:
            vul_object = Vul.objects.get(ip=ip)
        except:
            message = str(f"No IP {ip} on the Database!")
            return Response(message)
        else:
            data = request.data

            vul_object.port = data["port"]
            vul_object.rede = data["rede"]
            vul_object.data_1 = data["data_1"]
            vul_object.data_2 = data["data_2"]
            vul_object.count = data["count"]

            vul_object.save()

            serializer = VulSerializer(vul_object)
        return Response(serializer.data)

@login_required # Home view.
def home(request):
    count = User.objects.count()
    mal = Mal.objects.count()
    other = Other.objects.count()
    vul = Vul.objects.count()
    dict_all = dict([])
    dict_tables = dict([])
    list_all = list()
    list_val = list((Other.objects.all(), Mal.objects.all(), Vul.objects.all()))
    int_other = int(0)
    int_mal = int(0)
    int_vul = int(0)
    for i in range(0, len(list_val)):
        value = list_val[i]
        for num in value:
            if num.rede not in list_all:
                list_all.append(num.rede)
    for z in list_all:
        other_counter = int(0)
        mal_counter = int(0)
        vul_counter = int(0)
        counter = int(0)
        for y in range(0, len(list_val)):
            value = list_val[y]
            for num in value:
                if z in num.rede:
                    if y == 0:
                        other_counter += int(num.count)
                        int_other += int(num.count)
                    elif y == 1:
                        mal_counter += int(num.count)
                        int_mal += int(num.count)
                    elif y == 2:
                        vul_counter += int(num.count)
                        int_vul += int(num.count)
        counter += int(other_counter + mal_counter + vul_counter)
        dict_tables[z] = (other_counter, mal_counter, vul_counter ,counter)
        dict_all[z] = (counter)
    int_counter = int(int_other + int_mal + int_vul)
    total = list((int_other, int_mal, int_vul, int_counter))
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(list_all))]
    try:
        for key, values in dict_tables.items():
            p = 100 * float(values[3])/float(total[3])
            dict_tables[key] = (values[0], values[1], values[2], values[3], f"{round(p, 2)}%")
        p = 100 * float(total[3])/float(total[3])
        total = list((total[0], total[1], total[2], total[3], f"{round(p, 2)}%"))
    except:
        pass
    if 'search' in request.GET:
        search_term = request.GET['search']
        vulsearch = Vul.objects.all().filter(ip=search_term)
        if len(vulsearch) == 0:
            vulsearch = None
        else:
            vulsearch = (f"IP: \"{search_term}\" found on Vulnerability Reports!")
        malsearch = Mal.objects.all().filter(ip=search_term)
        if len(malsearch) == 0:
            malsearch = None
        else:
            malsearch = (f"IP: \"{search_term}\" found on Malware Reports!")
        othersearch = Other.objects.all().filter(ip=search_term)
        if len(othersearch) == 0:
            othersearch = None
        else:
            othersearch = (f"IP: \"{search_term}\" found on Other Reports!")
        search_result = list((vulsearch, malsearch, othersearch))
    else:
        search_result = None
    if 'search_net' in request.GET:
        search_term = request.GET['search_net']
        r = dict([])
        try:
            ListThem(search_term, r)
        except:
            search_network = None
        else:
            if search_term not in r.keys():
                search_network = str(f"IP: {search_term} does not belong to any of the defined Networks!")
            else:
                search_network = str(f"IP: {search_term} belongs to Network: {r[search_term]} - {network_range[r[search_term]][0]} - {network_range[r[search_term]][1]}")
    else:
        search_network = None
    context = {
        'count': count,
        'Mal': mal,
        'Other': other,
        'Vul': vul,
        'ip': network_range,
        'search_result': search_result,
        'search_network': search_network,
        'Table': dict_tables,
        'Pie': dict_all,
        'Total': total,
        'colors': color,
        'nbar': 'home'
    }
    return render(request, 'home.html', context)

@login_required # Other list view with upload and search bar.
def other_list_view(request):
    count1 = Other.objects.count()
    other_list = Other.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(other_list, 50)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    if 'search' in request.GET:
        search_term = request.GET['search']
        other = Other.objects.all().filter(ip=search_term)
        if len(other) == 0:
            other = Other.objects.all().filter(rede=search_term)
        count2 = len(other)
    else:
        other = None
        count2 = 0
    if request.method == 'POST':
        uploaded_file = request.FILES['other']
        fs = FileSystemStorage()
        fs.save('other.csv', uploaded_file)
        out = run([sys.executable,'other.py'], shell=False,stdout=PIPE)
        out = str(out)
        out = out.replace("\")", "").split("\\n")
        list_text = list(out)
        del list_text[0]
        os.remove(fileToSearch[0])
        file_txt = open(fileToSearch[3], "w")
        for values in list_text:
            file_txt.write(str(values) + "\n")
        file_txt.close()
    else:
        list_text = ""
    context = {
        'object_list': queryset,
        'Other' : other,
        'data1':list_text,
        'Count1': count1,
        'Count2': count2,
        'nbar': 'other'
    }
    return render(request, "other/other.html", context)

@login_required # Other download.
def download_other(request):
    filename = 'other.txt'
    fl = open(fileToSearch[3], 'r')
    mime_type, _ = mimetypes.guess_type(fileToSearch[3])
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    os.remove(fileToSearch[3])
    return response

@login_required # Vulnerability list view with upload and search bar.
def vul_list_view(request):
    count1 = Vul.objects.count()
    vul_list = Vul.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(vul_list, 50)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    if 'search' in request.GET:
        search_term = request.GET['search']
        vul = Vul.objects.all().filter(ip=search_term)
        if len(vul) == 0:
            vul = Vul.objects.all().filter(port=search_term)
        if len(vul) == 0:
            vul = Vul.objects.all().filter(rede=search_term)
        count2 = len(vul)
    else:
        vul = None
        count2 = 0
    if request.method == 'POST':
        uploaded_file = request.FILES['vul']
        fs = FileSystemStorage()
        fs.save('vul.csv', uploaded_file)
        out = run([sys.executable,'vul.py'], shell=False,stdout=PIPE)
        out = str(out)
        out = out.replace("\")", "").split("\\n")
        list_text = list(out)
        del list_text[0]
        os.remove(fileToSearch[1])
        file_txt = open(fileToSearch[4], "w")
        for values in list_text:
            file_txt.write(str(values) + "\n")
        file_txt.close()
    else:
        list_text = ""
    context = {
        'object_list': queryset,
        'Vul' : vul,
        'data1':list_text,
        'Count1': count1,
        'Count2': count2,
        'nbar': 'vul'
    }
    return render(request, "vul/vul.html", context)

@login_required # Vulnerability download.
def download_vul(request):
    filename = 'vul.txt'
    fl = open(fileToSearch[4], 'r')
    mime_type, _ = mimetypes.guess_type(fileToSearch[4])
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    os.remove(fileToSearch[4])
    return response

@login_required # Malware list view with upload and search bar.
def mal_list_view(request):
    count1 = Mal.objects.count()
    mal_list = Mal.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(mal_list, 50)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    if 'search' in request.GET:
        search_term = request.GET['search']
        mal = Mal.objects.all().filter(ip=search_term)
        if len(mal) == 0:
            mal = Mal.objects.all().filter(rede=search_term)
        count2 = len(mal)
    else:
        mal = None
        count2 = 0
    if request.method == 'POST':
        uploaded_file = request.FILES['mal']
        fs = FileSystemStorage()
        fs.save('mal.csv', uploaded_file)
        out = run([sys.executable,'mal.py'], shell=False,stdout=PIPE)
        out = str(out)
        out = out.replace("\")", "").split("\\n")
        list_text = list(out)
        del list_text[0]
        os.remove(fileToSearch[2])
        file_txt = open(fileToSearch[5], "w")
        for values in list_text:
            file_txt.write(str(values) + "\n")
        file_txt.close()
    else:
        list_text = ""
    context = {
        'object_list': queryset,
        'Mal' : mal,
        'data1':list_text,
        'Count1': count1,
        'Count2': count2,
        'nbar': 'mal'
    }
    return render(request, "mal/mal.html", context)

@login_required # Malware download.
def download_mal(request):
    filename = 'mal.txt'
    fl = open(fileToSearch[5], 'r')
    mime_type, _ = mimetypes.guess_type(fileToSearch[5])
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    os.remove(fileToSearch[5])
    return response

@login_required # Extract view.
def extract(request):
    os.system('python3 extract.py')
    if password:
        os.system(f"zip --password {password} -r ./upload/csv.zip ./upload/")
    else:
        os.system('zip -r ./upload/csv.zip ./upload/')
    filename = 'csv.zip'
    fl = open(fileToSearch[6], 'rb')
    response = HttpResponse(fl, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    for i in range(6, 9):
        os.remove(fileToSearch[i])
    return response