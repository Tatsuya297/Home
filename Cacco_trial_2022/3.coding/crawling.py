# import
import requests
import os
import shutil
import time
from bs4 import BeautifulSoup
import math
import sys
import pandas as pd

def makedir(dir): 
    if os.path.exists(dir): 
        print(f"remake, {dir}")
        shutil.rmtree(dir)  
        os.mkdir(dir)
    else: 
        print(f"make, {dir}")
        os.mkdir(dir)
dir_n = 1
makedir(f'traial_{dir_n}')
makedir(f'traial_{dir_n}/crawling_files')

#access total category page
print('access total category page')
url = 'https://blog.with2.net/category'
res = requests.get(url)
with open(f"traial_{dir_n}/crawling_files/total_category_page.html", "w", encoding='utf-8') as f: 
    f.write(res.text)
time.sleep(1)
front_url = 'https://blog.with2.net'
soup = BeautifulSoup(res.text, 'lxml')
cate_url_list = [] 
cate_lists = soup.find('ul', class_="cate tree0").find_all('li', class_="li0")
for cate_list in cate_lists: 
    cate_back_url = cate_list.find('a', class_='cate').get('href')
    cate_url = front_url+cate_back_url
    cate_url_list.append(cate_url)
print('over')

#access each ranking pages
result_list = []
result_check = []
for z, cate_url in enumerate(cate_url_list): 
    makedir(f'traial_{dir_n}/crawling_files/category_{z}')
    makedir(f'traial_{dir_n}/crawling_files/category_{z}/ranking')
    makedir(f'traial_{dir_n}/crawling_files/category_{z}/blog')

    print(f'access category{z} ranking page')
    def crow_total_ranking(url): 
        url
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        n_blog = (int(soup.find('h1').find('span', class_='count').text.
                    replace(',', '').replace('件', '').replace('(', '').replace(')', '')))
        print(f'the number of blogs in category{z} are {n_blog} .')
        
        if n_blog % 30 == 0: 
            end = math.floor(n_blog/30)-1
        else: 
            end = math.floor(n_blog/30)
        
        #check the website
        check_url = url+'/'+str(end)
        res_check = requests.get(check_url)
        res_check = requests.get(check_url)
        soup = BeautifulSoup(res_check.text, 'lxml')
        n_blog_ch = (int(soup.find('h1').find('span', class_='count').text.
                        replace(',', '').replace('件', '').replace('(', '').replace(')', '')))
        if n_blog == n_blog_ch: 
            print(f'there are no problems in category{z} ranking page.')
        else: 
            print(f'ferror, there are problems in category{z} ranking page.')
            sys.exit()
        
        #crawling
        print('1-page')
        with open(f"traial_{dir_n}/crawling_files/category_{z}/ranking/cate{z}_ranking_1.html", "w", encoding='utf-8') as f: 
            f.write(res.text)
        for i in range(1, (end+1)): 
            print(f'{i+1}-page')
            rank_url = url+'/'+str(i)
            res_rank = requests.get(rank_url)
            with open(f"traial_{dir_n}/crawling_files/category_{z}/ranking/cate{z}_ranking_{i+1}.html", "w", encoding='utf-8') as f: 
                f.write(res_rank.text)
            time.sleep(1)

        #check the website
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        n_blog_af = (int(soup.find('h1').find('span', class_='count').text.
                        replace(',', '').replace('件', '').replace('(', '').replace(')', '')))
        if n_blog == n_blog_af: 
            print('the number of blogs did not change.')
            check_url = url+'/'+str(end)
            res_check = requests.get(check_url)
            res_check = requests.get(check_url)
            soup = BeautifulSoup(res_check.text, 'lxml')
            n_blog_ch = (int(soup.find('h1').find('span', class_='count').text.
                            replace(',', '').replace('件', '').replace('(', '').replace(')', '')))
            if n_blog == n_blog_ch: 
                print('there are no problems in the website.')
                return n_blog
            else: 
                print('error, there are problems in the website.')
                sys.exit()
        else: 
            print('the number of blogs changed.')
            crow_total_ranking(cate_url)

    crow_total_ranking(cate_url)
    res = requests.get(cate_url)
    soup = BeautifulSoup(res.text, 'lxml')
    # n_blogs means the number of blogs in the website
    n_blogs = (int(soup.find('h1').find('span', class_='count').text.
                replace(',', '').replace('件', '').replace('(', '').replace(')', '')))
    if n_blogs % 30 == 0: 
        end = math.floor(n_blogs/30)-1
    else: 
        end = math.floor(n_blogs/30)
    print('over')

    #access blog information page                         
    print('access blog information page')
    error_list = []         #contains respose error 
    rank_page_list = []     #shows the number of blogs we can't get
    attri_list = []         #contains attribute error
    attri_i_list = []       #count blog-rank in attribute error
    time_list = []          #contains timeout error
    def get_blog(i, j, blog, blogs): 
        try: 
            rank = blog.find('span', class_='rankno').text
            #remove PR blog
            if rank == 'PR': 
                pass
            else: 
                rank = int(rank.replace('位', ''))
                back_url = blog.find('a', class_='info').get('href')
                blog_url = front_url+back_url
                res_blog = requests.get(blog_url)
                if str(res_blog) =='<Response [404]>': 
                    error_list.append([rank, blog_url])
                    print(f'error_blog_{rank}')
                else: 
                    soup_blog = BeautifulSoup(res_blog.text, 'lxml')
                    ID_info = soup_blog.find('li', class_='id').find('dd').text
                    ID_rank = back_url.replace('/blog/', '')
                    if ID_info != ID_rank: 
                        error_list.append([rank, blog_url])
                        print(f'error_blog_{rank}')
                    else: 
                        print(f'cate{z}_blog_{rank}')
                        with open(f"traial_{dir_n}/crawling_files/category_{z}/blog/cate{z}_blog_{rank}.html", "w", encoding='utf-8') as f: 
                            f.write(res_blog.text)
            time.sleep(1)
        except AttributeError: 
            rank = (30*(i-1)+j+1)
            if os.path.isfile(f"traial_{dir_n}/crawling_files/category_{z}/blog/cate{z}_blog_{rank}.html"): 
                pass
            else: 
                lack = 31-len(blogs)
                print(f"we couldn't get the category{z} ranking_{i} correctly.")
                rank_page_list.append([(str(i)+'-page of ranking-page'), ("can't get" +str(lack)+'blogs')])
                rank = (30*(i-1)+j+1)
                attri_list.append([rank, blog])
                attri_i_list.append(i)
                print(f'error_blog_{rank}')
        except TimeoutError: 
            rank = (30*(i-1)+j+1)
            time_list.append([rank, blog])
            print(f'error_blog_{rank}')

    front_url = 'https://blog.with2.net'
    for i in range(1, (end+2)): 
        with open(f"traial_{dir_n}/crawling_files/category_{z}/ranking/cate{z}_ranking_{i}.html", "r", encoding="utf-8") as f: 
            soup = BeautifulSoup(f, 'lxml')
            blogs = soup.find('ul', class_='rank').find_all('section', class_='item')
            for j, blog in enumerate(blogs): 
                get_blog(i, j, blog, blogs)
        print(f'{i}-page of no{z}ranking-page is over.')


    #check if there are problems in the blog infomation page.
    #if there are, retry to access the page.
    #attribute-error and time-error.
    if (len(rank_page_list) != 0): 
            print("list of ranking pages we can't get infomation")
            print(rank_page_list)
            rank_page = pd.DataFrame(rank_page_list, columns=['page num of ranking-page', 'num of lack'])
            rank_page.to_csv(f"traial_{dir_n}/crawling_files/category_{z}/rank_page_{z}.csv", encoding='utf-8')
    if (len(attri_list) == 0): 
        pass
    else: 
        print('we cannot get some pages: attri-error.')
        attri = pd.DataFrame(attri_list, columns=['rank', 'blog_html'])
        attri.to_csv(f"traial_{dir_n}/crawling_files/category_{z}/attri_list_{z}.csv", encoding='utf-8')
        print('try to get infomation again: attri')
        len_attri = len(attri_i_list)
        for i in range(0, len_attri): 
            i_attri = attri_i_list[i]
            with open(f"traial_{dir_n}/crawling_files/category_{z}/ranking/cate{z}_ranking_{i_attri}.html", "r", encoding="utf-8") as f: 
                soup = BeautifulSoup(f, 'lxml')
                blogs = soup.find('ul', class_='rank').find_all('section', class_='item')
                for j, blog in enumerate(blogs): 
                    get_blog(i_attri, j, blog, blogs)   
    if (len(time_list) == 0): 
        pass
    else: 
        print('we cannot get some pages: time-error.')
        attri = pd.DataFrame(time_list, columns=['rank', 'blog_html'])
        attri.to_csv(f"traial_{dir_n}/crawling_files/category_{z}/time_list_{z}.csv", encoding='utf-8')

    #respons error
    if (len(error_list) == 0): 
        print(f'category{z} finish')
        result_list.append(f'category{z} finish')
        result_check.append(0)
    else: 
        print('there were some errors.')
        print(error_list)
        error_df = pd.DataFrame(error_list, columns=['rank', 'blog_url'])
        error_df.to_csv(f"traial_{dir_n}/crawling_files/category_{z}/error_list_{z}.csv", encoding='utf-8', index=False)
        error_id_list = []
        error2_list = []
        print('try to get information again.')
        for j in range(0, len(error_list)): 
            rank = error_list[j][0]
            blog_url = error_list[j][1]
            res_blog = requests.get(blog_url)
            if str(res_blog) =='<Response [404]>': 
                error2_list.append([rank, blog_url])
                print(f'{rank}-page maybe be deleted. plese check.')
                with open(f"traial_{dir_n}/crawling_files/category_{z}/blog/cate{z}_blog_{rank}.html", "w", encoding='utf-8') as f: 
                    f.write(res_blog.text)
            else: 
                soup_blog = BeautifulSoup(res_blog.text, 'lxml')
                ID_info = soup_blog.find('li', class_='id').find('dd').text
                ID_rank = blog_url.replace('https://blog.with2.net/blog/', '')
                if ID_info != ID_rank: 
                    error_id_list.append([rank, blog_url])
                    print(f"{rank}-page's link is uncorrect.")
                else: 
                    print(f'blog_{rank}')
                    with open(f"traial_{dir_n}/crawling_files/category_{z}/blog/cate{z}_blog_{rank}.html", "w", encoding='utf-8') as f: 
                        f.write(res_blog.text)
            time.sleep(1)
        if len(error2_list) == 0 and len(error_id_list) == 0: 
            print(f'finish. we got all page in category{z}')
            result_list.append(f'finish. we got all page in category{z}')
            result_check.append(0)
        elif len(error2_list) != 0 and len(error_id_list) == 0: 
            print(error2_list)
            print(f'there are some delated pages in category{z}.plese check, finish')
            result_list.append(f'there are some delated pages in category{z}.plese check, finish')
            result_check.append(0)
            error2_df = pd.DataFrame(error2_list, columns=['rank', 'blog_url'])
            error2_df.to_csv(f"traial_{dir_n}/crawling_files/category_{z}/error2_list_{z}.csv", encoding='utf-8', index=False)    
        elif len(error2_list) == 0 and len(error_id_list) != 0: 
            print(f'link is not correct.end in category{z}. please retry')
            result_list.append(f'link is not correct.end in category{z}. please retry')
            result_check.append(1)
            print(error_id_list)
            error_id_df = pd.DataFrame(error_id_list, columns=['rank', 'blog_url'])
            error_id_df.to_csv(f"traial_{dir_n}/crawling_files/category_{z}/error_id_list_{z}.csv", encoding='utf-8', index=False)
        else: 
            print(f'there are some delated pages and incorrect links in category{z}')
            result_list.append(f'there are some delated pages and incorrect links in category{z}')
            result_check.append(1)
            print(error2_list)
            print(error_id_list)
            error2_df = pd.DataFrame(error2_list, columns=['rank', 'blog_url'])
            error2_df.to_csv(f"traial_{dir_n}/crawling_files/category_{z}/error3_list_{z}.csv", encoding='utf-8', index=False)  
            error_id_df = pd.DataFrame(error_id_list, columns=['rank', 'blog_url'])
            error_id_df.to_csv(f"traial_{dir_n}/crawling_files/category_{z}/error_id_list_{z}.csv", encoding='utf-8', index=False)

#total_result
print(result_list)
if 1 in result_check: 
    print('there are some problems')
else: 
    print('crawling complete')