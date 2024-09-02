from django.shortcuts import render, get_object_or_404
from bs4 import BeautifulSoup
from django.http import HttpResponse
from .models import Compares
import random
import requests

def find_movies(username):
    url = f'https://letterboxd.com/{username}/films/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    ssd = []
    ssk = []
    length = 0
    if soup.find('div', class_ = 'pagination'):
        ssd = soup.find('div', class_ = 'pagination').find_all('a')
        ssk = [str(i) for i in ssd]
        length = int(ssk[-1].split('>')[1].split('<')[0])
        
    table = soup.find('ul', class_ = 'poster-list -p70 -grid film-list clear')
    titles_location = table.find_all('img')
    titles_prep = [str(title).split('''"''') for title in titles_location]
    titles = [i[1] for i in titles_prep]
    
    if len(ssd) > 0:
        for i in range(2, length):
            url = f"https://letterboxd.com/{username}/films/page/{i}"
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'lxml')
            table = soup.find('ul', class_ = 'poster-list -p70 -grid film-list clear')
            titles_location = table.find_all('img')
            titles_prep = [str(title).split('''"''') for title in titles_location]
            titles_temp = [i[1] for i in titles_prep]
            titles += titles_temp
    return titles

def find_watchlist(username):
    url = f'https://letterboxd.com/{username}/watchlist/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    ssd = []
    ssk = []
    length = 0
    table = []
    titles_location = ""
    titles_prep = []
    titles = []
    if soup.find('div', class_ = 'pagination'):
        ssd = soup.find('div', class_ = 'pagination').find_all('a')
        ssk = [str(i) for i in ssd]
        length = int(ssk[-1].split('>')[1].split('<')[0])
    if soup.find('ul', class_ = 'poster-list -p125 -grid -scaled128'):
        table = soup.find('ul', class_ = 'poster-list -p125 -grid -scaled128')
        titles_location = table.find_all('img')
        titles_prep = [str(title).split('''"''') for title in titles_location]
        titles = [i[1] for i in titles_prep]
    
    if len(ssd) > 0:
            for i in range(2, length):
                url = f"https://letterboxd.com/{username}/watchlist/page/{i}"
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'lxml')
                table = soup.find('ul', class_ = 'poster-list -p125 -grid -scaled128')
                titles_location = table.find_all('img')
                titles_prep = [str(title).split('''"''') for title in titles_location]
                titles_temp = [i[1] for i in titles_prep]
                titles += titles_temp
    return titles

def compare(username1, username2):
    list1 = find_movies(username1)
    list2 = find_movies(username2)
    watchlist1 = find_watchlist(username1)
    watchlist2 = find_watchlist(username2)
    watchlist = watchlist1 + watchlist2
    recommendation = ""
    percentage = 0
    intersection2 =[]
    
    intersection = set(list1).intersection(list2)
    movies_mean = (len(set(list1))+len(set(list2)))/2
    percentage1= round((len(intersection) / movies_mean )*100)
    if len(watchlist1)>0 and len(watchlist2)> 0:
        intersection2 = list(set(watchlist1).intersection(watchlist2))
        watchlist_min = min(len(watchlist1), len(watchlist2))
        percentage2 = round((len(intersection2) / watchlist_min )*100)
        percentage = percentage1*0.65 + percentage2*0.35
        if intersection2 == []:
            recommendation = random.choice(watchlist)
        elif intersection2 != []:
            recommendation = random.choice(intersection2)
    else:
        percentage = percentage1    
    
    return percentage, recommendation

def web(request):
    return render(request, 'index.html')

def result(request):
    data = request.POST
    username1 = data['username1']
    username2 = data['username2']
    percentage, recommendation = compare(username1, username2)
    try:
        comparation = Compares.objects.get(username1 = username1, username2=username2, percentage=percentage)
    except:
        Compares.objects.create(username1= username1, username2= username2, percentage= percentage)
    obb = Compares.objects.filter(username1=username1, username2=username2).latest('co_time')
    return render(request, 'result.html', {'obb': obb,
                                           'recommendation': recommendation})
# Create your views here.
