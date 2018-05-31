import os
import csv
import json
import requests
from lxml import etree
from django.shortcuts import render
from django.core.paginator import Paginator
from showscore.models import Score
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

# Create your views here.
from django.http import HttpResponse

index_htm = 'https://bangumi.bilibili.com/anime/index'
season_api = 'https://bangumi.bilibili.com/web_api/season/index_global'
#'https://bangumi.bilibili.com/web_api/season/index_global'
#'?page=1&page_size=20&version=0&is_finish=0&start_year=0&tag_id=&index_type=1&index_sort=0&quarter=0'
bangumi='https://bangumi.bilibili.com/jsonp/seasoninfo/{0}.ver'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
}
#?callback=seasonListCallback
def index(request):
    #anime_data = Score.objects.all()
    limit = 20
    anime_data = Score.objects.order_by("-score", "-count")
    paginator = Paginator(anime_data, limit)
    page = request.GET.get('page')
    try:
        anime_data = paginator.page(page)
    except PageNotAnInteger:
        anime_data = paginator.page(1)
    except EmptyPage:
        anime_data = paginator.page(paginator.num_pages)
    context = {
        'anime':anime_data,
    }
    return render(request, 'index.html', context = context)

def collect(request):
    index_html = requests.get(index_htm, headers=headers).content
    html_etree = etree.HTML(index_html)
    years = html_etree.xpath('//div[contains(@class,"tab_year")]/a[contains(@class,"tab-i ckc")]/text()')
    years_list = [int(x) for x in years if x.isdigit()]  #获取年份列表得到[2018,2017,2017...]
    get_bangumi(years_list)
    anime_data = Score.objects.all()
    context = {
        'anime':anime_data,
    }
    return render(request, 'index.html', context = context)

def get_bangumi(year_list):
    def bgm_index(year, season, page):
        params = (
            ('page', page),
            ('page_size', '20'),
            ('version', '0'),
            ('is_finish', '0'),
            ('start_year', year),
            ('tag_id', ''),
            ('index_type', '2'),
            ('index_sort', '0'),
            ('quarter', season),
        )
        result = requests.get(season_api, headers=headers, params=params).json()

        if result['result']['list']:
            for bgm in result['result']['list']:
                print(year, season, page, bgm['season_id'])
                try:
                    save_to_db(bgm['season_id'])
                    #s = Score(bangumi_id=bgm['season_id'],cover=bgm['cover'],title=bgm['title'])
                except:
                    print(bgm['season_id']+'failed to add to DB')

            return True
        else:
            return False

    for x in year_list:
        for y in [1, 2, 3, 4]:
            z = 1
            while bgm_index(x, y, z):
                z += 1
def save_to_db(bgmid):
    params = (
        ('callback', 'seasonListCallback'),
    )
    response = requests.get(bangumi.format(bgmid), headers=headers, params=params)
    print(response.url)
    data = json.loads(response.text[19:-2])
    title = '\"{}\"'.format(data['result']['media']['title'])
    score = float(data['result']['media']['rating']['score'])
    count = int(data['result']['media']['rating']['count'])
    play_count = int(data['result']['play_count'])
    cover = '\"{}\"'.format(data['result']['cover'])
    bangumi_id = int(bgmid)
    pub_time = str('\"{}\"'.format(data['result']['pub_time'][:10]))
    brief = data['result']['brief']
    s = Score(bangumi_id=bangumi_id,score=score,count=count,brief=brief,
              play_count=play_count,pub_time=pub_time,cover=cover,title=title)
    s.save()

def export_csv(request):
    all_s = Score.objects.order_by("-score", "-count")
    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_dir = os.path.join(base_dir,'..','csv_file')
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)
    csvpath = os.path.join(base_dir,'..','csv_file','anime_score.csv')
    with open(csvpath,'w',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        #先写入columns_name
        writer.writerow(["番剧id","分数","评分人数","番剧名","番剧简介","播放次数","播放时间"])
        for s in all_s:
            single_list = []
            single_list.append(s.bangumi_id)
            single_list.append(s.score)
            single_list.append(s.count)
            single_list.append(s.title)
            single_list.append(s.brief)
            single_list.append(s.play_count)
            single_list.append(s.pub_time)
            writer.writerow(single_list)
        csvfile.close()
    with open(csvpath,encoding='utf-8') as f:
        c = f.read()
    response = HttpResponse(c)
    filename = os.path.basename(csvpath)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename={0}'.format(filename)
    return response


