# Itest-answer
# itest答案显示
#### 为什么说是itest答案显示呢，因为只能显示答案，不能自动答题。
******
## 用法
#### 1，安装python环境。
#### 2，打开浏览器开始一项考试。
#### 3，编辑`Itest.py`的第21行如下，将172.16.64.208换成你们学校itest主机的ip。（gliet/guet的可以不用换）
```
HOST = '172.16.64.208'
```
#### 4，运行`python Itest.py`运行程序，输入学号姓名即可使用。
******

## 这里有适用于gliet/guet的打包好的exe程序。[点击下载](https://github.com/chainsx/Itest-answer/releases/download/1.0/itest.exe)

### 如何获取学校itest主机的ip(以guet为例)
```
nslookup itest.guet.edu.cn
服务器:  openwrt.lan
Address:  192.168.31.1

非权威应答:
名称:    wrdproxy.guet.edu.cn
Address:  172.16.64.208
Aliases:  itest.guet.edu.cn
```
## 作者: Hanxven_Marvels 20200707 编辑修改请注明
