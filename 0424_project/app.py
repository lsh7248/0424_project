import os, requests
import pymysql
from datetime import datetime
from flask import Flask, render_template
from flask import request, redirect, abort, session, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
import random



app = Flask(__name__, 
            static_folder="static",
            template_folder="views")
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.secret_key = 'abcabc'

db = pymysql.connect(
    user='root',
    passwd='8427728c',
    host='localhost',
    db='0424_project',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

def get_menu(name):
    cursor = db.cursor()
    cursor.execute(f"""select b.* from tb_members a, tb_diary b where a.id = b.member_id and a.name = '{name}'""")
    menu = [f"<li><a href='/{row['id']}'>{row['title']}</a></li>"
            for row in cursor.fetchall()]
    return '\n'.join(menu)

    
@app.route("/", methods = ["GET", "POST"])
def index():    
    
    title = 'Welcome ' + session['user']['name'] if 'user' in session else 'Welcome'
    content = 'Welcome My Diary!'
    
    if 'user' in session:
        name = session['user']['name']
        menu = get_menu(session['user']['name'])
    else:
        name = ''
        menu = ''
        
    return render_template('template.html',
                           name = name,
                           title = title,
                           content = content,
                           menu = menu)

@app.route("/login", methods = ["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        cursor = db.cursor()
        cursor.execute(f"""select * from tb_members where name = '{request.form["name"]}'""")
        user = cursor.fetchone()
        
        if user is None:
            message = "<p>회원이 아닙니다.</p>"
        else:
            cursor.execute(f"""
            select id, name, profile, password from tb_members 
            where name = '{request.form['name']}' and 
                  password = SHA2('{request.form['password']}', 256)""")
            user = cursor.fetchone()
            if user is None:
                message = "<p>비밀번호를 확인해주세요</p>"
            else:
                session['user'] = user
                return redirect("/")
                
    return render_template('login.html',
                           message=message)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')



@app.route('/<id>')
def diary(id):
    cursor = db.cursor()
    cursor.execute(f"""select title, content from tb_diary
                       where id = {id}
                   """)
    diary_list = cursor.fetchone()
    title = diary_list['title']
    content = diary_list['content'] 
    
    return render_template('diary.html',
                           name = session['user']['name'],
                           title=title,
                           content=content,
                           menu=get_menu(session['user']['name']),
                           id = id,
                           img_src = get_img(title))

# 웹에서 이미지 검색 & 결과 보여주기
def get_img(word):
    url = "https://search.naver.com/search.naver"
    query = { 'where': 'image',
             'sm' : 'tab_jum',
             'query' : word
    }
    response = requests.get(url,params=query)
    soup = BeautifulSoup(response.content, "html.parser")
    tags = soup.select('img._img')
    
    
    
    return tags[random.randrange(50)]['data-source']


@app.route('/create', methods=["get", "post"])
def create():
    if request.method == "POST":
        cursor = db.cursor()
        cursor.execute(f"""insert tb_diary (title, content, created, member_id)
                           values ('{request.form['title']}', '{request.form['content']}',
                        '{datetime.now()}', '{session['user']['id']}')
                        """)
        db.commit()

        return redirect('/')
    
    return render_template('create.html',
                           name = session['user']['name'],
                           menu = get_menu(session['user']['name']))

@app.route("/delete/<id>")
def delete(id):
    cursor = db.cursor()
    cursor.execute(f"delete from tb_diary where id='{id}'")
    db.commit()
    
    return redirect("/")
                           
@app.route("/update/<id>", methods = ["GET", "POST"])
def update(id):
    cursor = db.cursor()
    cursor.execute(f"""select title, content from tb_diary
                       where id = {id}
                   """)
    diary_list = cursor.fetchone()
    title = diary_list['title']
    content = diary_list['content']
    
    if request.method == "POST":
        cursor.execute(f"""update tb_diary set
                      title = '{request.form['title']}',
                      content = '{request.form['content']}',
                      created = '{datetime.now()}'
                      where id = '{id}'""")
        return redirect("/")
    
    return render_template('update.html',
                           name = session['user']['name'],
                           title=title,
                           content=content,
                           menu=get_menu(session['user']['name']),
                           id = id)


@app.route('/crawler/google/<word>')
def crawler_google(word):
#     def download_img_from_tag(tag, filename):
#         response = requests.get(tag['data-source'])
#         with open(filename, 'wb') as f:
#             f.write(response.content)

    driver = webdriver.Chrome('chromedriver.exe')
    driver.implicitly_wait(10)
    
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%84%A4%EC%9D%B4%EB%B2%84%EC%9A%B4%EC%84%B8"
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="srch_txt"]').click()
    driver.find_element_by_css_selector('#srch_txt').send_keys(word)
    driver.find_element_by_xpath('//*[@id="fortune_birthCondition"]/div[1]/fieldset/input').click()
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     tags = soup.select("h3.r dO0Ag")
#     filenames = []
#     for i, tag in enumerate(tags):
#         # tag를 던지면 이미지를 저장하고 이미지명을 반환
#         filename = f'static/{word}{i}.jpg'
#         download_img_from_tag(tag, filename)
#         filenames.append(filename)
    
#     return render_template('crawler.html',
#                            files=filenames)

#################################
#네이버운세 selenium
#####################3
# from selenium import webdriver
# import time
# driver = webdriver.Chrome('chromedriver.exe')
# driver.implicitly_wait(3)
# url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%84%A4%EC%9D%B4%EB%B2%84%EC%9A%B4%EC%84%B8"
# driver.get(url)

# driver.find_element_by_xpath('//*[@id="srch_txt"]').click()
# driver.find_element_by_css_selector('#nx_query').click()
# time.sleep(1)
# driver.find_element_by_xpath('//*[@id="srch_txt"]').click()
# driver.find_element_by_css_selector('#srch_txt').send_keys('19801111')


app.run(port=8088)