

#import
from bs4 import BeautifulSoup
import math
import pandas as pd
import os
import shutil
import re

# make directory
def makedir(dir): 
    if os.path.exists(dir): 
        print(f"remake, {dir}")
        shutil.rmtree(dir)  
        os.mkdir(dir)
    else: 
        print(f"make, {dir}")
        os.mkdir(dir)

#select dir_number 
dir_n = 1
makedir(f'traial_{dir_n}/data')


#total_category_page
print('start total_category_page')
def getinfo(a_cate): 
    name = a_cate.find('a', class_='cate').get('title')
    patarn = "\(.+?\)"
    regular = re.findall(patarn, name)
    if len(regular) != 0: 
        name = name.replace(regular[-1], '')
    else: 
        name = name.replace(regular, '')
    return name

total_list = []
d_cate = {}
cate_name_list = []
d_name = {}
with open(f"traial_{dir_n}/crawling_files/total_category_page.html", "r", encoding='utf-8') as f: 
    soup = BeautifulSoup(f, 'lxml')
    ###category
    cate_lists = soup.find('ul', class_="cate tree0").find_all('li', class_="li0")
    n_cate = len(cate_lists)
    for y, cate_list in enumerate(cate_lists): 
        cate_name = getinfo(cate_list)
        d_name['カテゴリ名'] = cate_name
        d_name['カテゴリ番号'] = y
        cate_name_list.append(d_name)
        d_name = {}
        
        ###subcategory
        subcate_lists = cate_list.find_all('li', class_="li1")
        for subcate_list in subcate_lists: 
            subcate_name = getinfo(subcate_list)
            sub2cate_lists = []
            sub2cate_lists = subcate_list.find_all('li', class_= 'li2')
            d_cate['カテゴリ'] = cate_name
            d_cate['タイトル'] = subcate_name
            d_cate['サブカテゴリ'] = subcate_name
            total_list.append(d_cate)
            d_cate = {}
            if sub2cate_lists == []: 
                pass
            else: 
                
                ###sub2category
                for sub2cate_list in sub2cate_lists: 
                    sub2cate_name = getinfo(sub2cate_list)
                    
                    sub3cate_lists = []
                    sub3cate_lists = sub2cate_list.find_all('li', class_= 'li3')
                    d_cate['カテゴリ'] = cate_name
                    d_cate['タイトル'] = sub2cate_name
                    d_cate['サブカテゴリ'] = subcate_name
                    d_cate['サブ2カテゴリ'] = sub2cate_name
                    total_list.append(d_cate)
                    d_cate = {}
                    if sub3cate_lists == []: 
                        pass
                    else: 
                        ###sub3category
                        for sub3cate_list in sub3cate_lists: 
                            sub3cate_name = getinfo(sub3cate_list)
                            sub3cate_name = sub3cate_name.replace('++', '+ +')
                            d_cate['カテゴリ'] = cate_name
                            d_cate['タイトル'] = sub3cate_name
                            d_cate['サブカテゴリ'] = subcate_name
                            d_cate['サブ2カテゴリ'] = sub2cate_name
                            d_cate['サブ3カテゴリ'] = sub3cate_name
                            total_list.append(d_cate)
                            d_cate = {}
df_cate = pd.DataFrame(total_list)
df_cate = df_cate[[ 'タイトル', 'カテゴリ', 'サブカテゴリ', 'サブ2カテゴリ', 'サブ3カテゴリ']]
df_cate.to_csv(f'traial_{dir_n}/data/category_list.csv', encoding='CP932', index=False)
df_name = pd.DataFrame(cate_name_list)
df_name = df_name[['カテゴリ名', 'カテゴリ番号']]
df_name.to_csv(f'traial_{dir_n}/data/category_name_list.csv', encoding='CP932', index=False)
print('over total_category_page')

check_list = []
problem_list = []
for z in range(0, n_cate): 
    #each_ranking_page
    print(f'start cate{z}_ranking_page')
    ranking_list = []
    d_rank = {}
    #get infomation from 1st page.
    with open(f"traial_{dir_n}/crawling_files/category_{z}/ranking/cate{z}_ranking_1.html", "r", encoding='utf-8') as f: 
            soup = BeautifulSoup(f, 'lxml')
            n_blog = (int(soup.find('h1').find('span', class_='count').text.
                            replace(',', '').replace('件', '').replace('(', '').replace(')', '')))
            if n_blog % 30 == 0: 
                end = math.floor(n_blog/30)-1
            else: 
                end = math.floor(n_blog/30)
    # crawling ranking page
    for i in range(1, (end+2)): 
        with open(f"traial_{dir_n}/crawling_files/category_{z}/ranking/cate{z}_ranking_{i}.html", "r", encoding='utf-8') as f: 
            soup = BeautifulSoup(f, 'lxml')
            rankings = soup.find('ul', class_='rank').find_all('section', class_='item')
            for ranking in rankings: 
                d_rank = {}
                rank = ranking.find('span', class_='rankno').text
                if rank == 'PR': 
                    pass
                else: 
                    name = ranking.find('a', class_='ttl').text
                    rank = int(rank.replace('位', ''))
                    update = ranking.find('li', class_='time')
                    if str(type(update)) == "<class 'NoneType'>": 
                        pass
                    else: 
                        update = update.text
                    ID = ranking.find('a', class_='info').text.replace('ID:', '')
                    IN_OUT = ranking.find('div', class_='rank-info').find_all('span')
                    week_in = IN_OUT[0].text.replace('週間IN:', '')
                    week_out = IN_OUT[1].text.replace('週間OUT:', '')
                    mon_in = IN_OUT[2].text.replace('月間IN:', '')
                    d_rank = {'ブログ名': name, '順位': rank, 'ID': ID, '週間IN': week_in, '週間OUT': week_out, '月間IN': mon_in, '更新日時': update}
                    ranking_list.append(d_rank)
        print(f"cate{z}_ranking_{i}: over")
    df_rank = pd.DataFrame(ranking_list)
    with open(f'traial_{dir_n}/data/ranking_list_{z}.csv', mode="w", encoding="cp932", errors="ignore", newline=None) as f: 
        df_rank.to_csv(f, index=False)
    print(f'over cate{z}_ranking_page')


    #blog_infomation_page
    print(f'start cate{z} blog_infomation_page')
    blog_list = []          #use to make DataFrame of blogs
    error_list = []         #hold blog number when Attribute-Error happen
    deleted_list = []       #hold blog number when it's deleted page.
    file_not_list = []      #hold blog number when page wasn't find
    def get_blog_info(i): 
        try: 
            with open(f"traial_{dir_n}/crawling_files/category_{z}/blog/cate{z}_blog_{i}.html", "r", encoding='utf-8') as f: 
                soup = BeautifulSoup(f, 'lxml')
                d_blog = {}
                cate = []
                try: 
                    ID = soup.find('li', class_='id').find('dd').text
                    categories = soup.find('ul', class_='cate').find_all('li')
                    for category in categories: 
                        _cate = category.find('a').text.replace('++', '+ +')
                        cate.append(_cate)
                    d_blog['カテゴリ'] = cate
                    intr = soup.find('li', class_='desc').find('dd').text
                    d_blog = {'ID': ID, 'カテゴリ': cate, '紹介文': intr}
                    blog_list.append(d_blog)
                    print(f"cate{z}_blog_{i}: over")
                except AttributeError: 
                    if (os.path.isfile(f"traial_{dir_n}/crawling_files/category_{z}/error2_list_{z}.csv")): 
                        error2_df = pd.read_csv(f"traial_{dir_n}/crawling_files/category_{z}/error2_list_{z}.csv") 
                        length = len(error2_df)
                        for j in range(0, length): 
                            if int(error2_df['rank'][j]) == i: 
                                ID = (soup.find('section', class_='error').find('h1').text
                                    .replace("指定された登録IDが見つかりませんでした。(ID: ", "").replace(')', ''))
                                if df_rank['ID'][i-1] == ID: 
                                    print(f'blog_{i} is deleted.')
                                    blog_list.append(d_blog)
                                    deleted_list.append(i)
                                else: 
                                    print(f'blog_{i} : could not get')
                                    error_list.append(f'blog_{i}')
                    else: 
                        print(f'cate{z}_blog_{i} : could not get')
                        error_list.append(f'blog_{i}')
        except FileNotFoundError as E: 
            file_not_list.append((i))
            
    for i in range(1, n_blog+1): 
        get_blog_info(i)
    df_blog = pd.DataFrame(blog_list)
    #output of ranking_page
    with open(f'traial_{dir_n}/data/blog_list_{z}.csv', mode="w", encoding="cp932", errors="ignore", newline=None) as f: 
        df_blog.to_csv(f, index=False)      
    print(f'over cate{z} blog_infomation_page')


    ##chech the Correctness
    print(f'check the correctness cate{z}')
    check_id = []
    check_rank = []
    if len(df_rank) == len(df_blog)==n_blog: 
        for i in range(0, len(df_rank)): 
            if df_rank['ID'][i] == df_blog['ID'][i]: 
                pass
            elif i+1 in deleted_list: 
                pass 
            else: 
                check_id.append(str(i+1)+'th-page')
            if df_rank['順位'][i] == i+1: 
                pass
            else: 
                check_rank.append(str(i+1)+'th-page')
        if len(check_id)==0 and len(check_rank)==0: 
            if len(deleted_list) == 0: 
                print(f'len of ranking-page cate{z}: ', len(df_rank))
                print(f'len of blog-info-page cate{z}: ', len(df_blog))
                print(f'number of blogs cate{z}: ', n_blog)
                print(f'All right cate{z}')
                check_list.append(0)
                
            else: 
                print(f'len of ranking-page cate{z}: ', len(df_rank))
                print(f'len of blog-info-page cate{z}: ', len(df_blog))
                print(f'number of blogs cate{z}: ', n_blog)
                print(f'All right, we cannot get some page because the page is deleted cate{z}')
                print(f'the pages follow cate{z}: ')
                print(deleted_list)
                check_list.append(0)
        else: 
            print(check_id)
            print(check_rank)
            print(f'have problem. cate{z}')
            check_list.append(1)
            problem_list.append(f'cate{z}')
    else: 
        print(f"Don't match the lenght cate{z}")
        print(f'len of ranking-page:  cate{z}', len(df_rank))
        print(f'len of blog-info-page cate{z}: ', len(df_blog))
        print(f'number of blogs cate{z}: ', n_blog)
        print(error_list)
        print(deleted_list)
        print(file_not_list)
        check_list.append(1)
        problem_list.append(f"cate{z} Don't match the lenght")

#check all correctness
if 1 in check_list: 
    print('there are some problems')
else: 
    print('scraping complete')

