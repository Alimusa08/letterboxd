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
    ssd = soup.find('div', class_ = 'pagination').find_all('a')
    ssk = [str(i) for i in ssd]
    length = int(ssk[-1].split('>')[1].split('<')[0])
    table = soup.find('ul', class_ = 'poster-list -p70 -grid film-list clear')
    titles_location = table.find_all('img')
    titles_prep = [str(title).split('''"''') for title in titles_location]
    titles = []
    
    if len(ssd) > 0:
        for i in range(1, length+1):
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
    url_pages = soup.find('div', class_ = 'pagination').find_all('a')
    ssk = [str(i) for i in url_pages]
    length = int(ssk[-1].split('>')[1].split('<')[0])
    table = soup.find('ul', class_ = 'poster-list -p125 -grid -scaled128')
    titles_location = table.find_all('img')
    titles_prep = [str(title).split('''"''') for title in titles_location]
    titles = []
    
    if len(url_pages) > 0:
            for i in range(1, length+1):
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
    
    intersection = set(list1).intersection(list2)
    movies_mean = (len(set(list1))+len(set(list2)))/2
    percentage1= round((len(intersection) / movies_mean )*100)
    
    intersection2 = list(set(watchlist1).intersection(watchlist2))
    watchlist_min = min(len(watchlist1), len(watchlist2))
    percentage2 = round((len(intersection2) / watchlist_min )*100)
    
    recommendation = random.choice(intersection2)
    
    percentage = percentage1*0.65 + percentage2*0.35
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
        comparation = Compares()
        comparation.username1 = username1
        comparation.username2 = username2
        comparation.percentage = percentage
        comparation.save()
    obb = get_object_or_404(Compares, username1=username1, username2=username2)
    return render(request, 'result.html', {'obb': obb,
                                           'recommendation': recommendation})
# Create your views here.
