from flask import Flask, render_template, request, flash, session, redirect, url_for, json, Response, jsonify
from MhDatabses import MhDatabases
from functools import wraps
import numpy
import sys
from imp import reload
from flask_cors import CORS
app = Flask(__name__)
app.secret_key = 'test'

@app.route('/')
def hello_world():
    return render_template("echarts.html")

def login_required(func):
    @wraps(func) # 修饰内层函数，防止当前装饰器去修改被装饰函数的属性
    def inner(*args, **kwargs):
        # 从session获取用户信息，如果有，则用户已登录，否则没有登录
        user_id = session.get('user_id')
        print("session user_id:", user_id)
        if not user_id:
            return redirect('login')
        return func(*args, **kwargs)
    return inner

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 返回登录界面
    if request.method == 'GET':
        return render_template("login.html")
    else:
        # 获取用户名和密码
        name = request.form.get("username")
        pwd = request.form.get("password")
        session['user_id'] = name
        print("username:", name)
        print("password:", pwd)

        #设置内置管理员账户密码
        names = ["tyd", "wm", "wyh", "tlx", "wt"]
        pwds = ["tyd123", "wm123", "wyh123", "tlx123", "wt123"]

        # 验证是否是管理员账户密码，如果是，就登录进主界面，否则返回登录界面
        y = 0
        for i in names:
            if i == name and pwd == pwds[names.index(i)]:
                y = 1
                break
        if y == 1:
            return render_template("index.html")
        else:
            tip="登录失败"
            return render_template("login.html",tip=tip)

@app.route('/billList', methods=['GET', 'POST'])
@login_required
def billList():
    # 连接数据库
    db=MhDatabases()
    if request.method == 'GET':
        # 从数据库中返回最近十条交易记录并返回
        result = db.executeQuery("select * from pcr")
        return render_template("billList.html",result=result)
    else:
        # 获取商品ID或者名称
        option=request.values.get("searchoption")
        product = request.form.get("product")
        print(option)
        print(product)


        if option == "请输入商品的ID" :
            # 根据商品ID从数据库获取交易信息，如果不存在返回“无此交易记录”
            result = db.executeQuery("select * from pcr where gid=%s",[product])
            if len(result)==0:
                result="无此交易记录"
        else:
            # 根据商品名称从数据库获取交易信息，如果不存在返回“无此交易记录”
            result = db.executeQuery("select * from pcr where name=%s",[product])
            if len(result) == 0:
                result="无此交易记录"
        return render_template("billList.html",result=result)

@app.route('/product', methods=['GET', 'POST'])
@login_required
def product():
    # 连接数据库
    db = MhDatabases()
    if request.method == 'GET':
        # 从数据库中返回最近十条商品信息并返回
        result = db.executeQuery("select * from goods")
        return render_template("product.html",result=result)
    else:
        # 获取商品ID
        proID=request.form.get("proID")
        print("proID",proID)
        pid=request.form.get("pid")
        print("pid",pid)
        #获取操作类型
        btntype = request.form.get("btntype")
        print("btntype", btntype)
        if proID:
            # 从数据库获取商品信息并返回
            result = db.executeQuery("select * from goods where gid=%s",[product])
            return render_template("product.html",result=result)
        if pid and btntype=="pread":
            # 从数据库获取商品信息，返回商品查看界面
            result = db.executeQuery("select * from goods where gid=%s",[pid])
            return render_template("productView.html",result=result)
        if pid and btntype=="pupdate":
            # 返回商品修改界面
            return redirect(url_for('productUpdate',pid=pid))

@app.route('/productAdd', methods=['GET', 'POST'])
@login_required
def productAdd():
    # 连接数据库
    db = MhDatabases()
    if request.method == 'GET':
        return render_template("productAdd.html")
    else:
        # 获取要添加的商品信息
        product=[]
        product.append(request.form.get("productId"))
        product.append(request.form.get("productName"))
        product.append(request.form.get("type"))
        product.append(int(request.form.get("number")))
        product.append(float(request.form.get("price")))
        product.append(request.form.get("dateofproduce"))
        product.append(request.form.get("dateofbad"))
        print(product)

        # 查询数据库中是否已存在该商品，如果不存在则向数据库添加商品信息
        result1 = db.executeQuery("select * from goods where gid=%s", [product[0]])
        result2 = db.executeQuery("select * from goods where name=%s",[product[1]])
        if len(result1[0]) == 0 and len(result2[0]) == 0:
            result = db.executeUpdate("insert into goods values(%s,%s,null,%s,%s,%s,%s,%s,null)",product)
        else:
            result = 0
        return render_template("productAdd.html",data=result)

@app.route('/productUpdate/?<string:pid>', methods=['GET', 'POST'])
@login_required
def productUpdate(pid):
    # 连接数据库
    db = MhDatabases()
    if request.method == 'GET':
        # 从数据库获取商品信息并返回
        result = db.executeQuery("select * from goods where gid=%s",[pid])
        return render_template("productUpdate.html",result=result)
    else:
        # 获取商品可修改的信息
        product = []
        pid=request.form.get("productId")
        product.append(request.form.get("type"))
        product.append(int(request.form.get("number")))
        product.append(float(request.form.get("price")))
        print(product)

        # 在数据库中修改商品信息
        db.executeUpdate("update goods set sort=%s where gid=%s",[product[0],pid])
        db.executeUpdate("update goods set number=%s where gid=%s", [product[1], pid])
        db.executeUpdate("update goods set uprice=%s where gid=%s", [product[2], pid])
        return redirect(url_for('product'))

@app.route('/userlogin',methods=['GET','POST'])
def score():
    # 连接数据库
    db=MhDatabases()

    # 获取微信小程序端传来的ID和password
    id = str(json.loads(request.values.get("id")))
    password=str(json.loads(request.values.get("password")))
    print("id",id)
    print("password",password)

    # 根据ID在数据库中查询用户数据
    result=db.executeQuery("select * from user where phone=%s",[id])
    print(result)

    if len(result)!=0:
        if result[0][1]==password:
        # 如果匹配返回登录成功
            res='登录成功'
            return json.dumps(res)
    else:
        # 如果不匹配返回账号或密码错误
        res='账号或密码错误'
        return json.dumps(res)

@app.route('/userregister',methods=['GET','POST'])
def score():
    # 连接数据库
    db=MhDatabases()

    # 获取微信小程序端传来的ID和password
    id = str(json.loads(request.values.get("id")))
    password=str(json.loads(request.values.get("password")))
    name = str(json.loads(request.values.get("name")))
    sex = str(json.loads(request.values.get("sex")))
    print("name",name," sex",sex," id",id," password",password)

    # 根据ID在数据库中查询用户数据
    result1 = db.executeQuery("select * from goods where gid=%s", [id])
    if len(result1[0]) == 0:
        result = db.executeUpdate("insert into goods values(%s,%s,%s,%s,)", [id,password,sex,name])
    else:
        result = 0
    if result==1:
        res="注册成功"
    else:
        res="注册失败，手机号已注册"
    return json.dumps(res)


@app.route('/allorders',methods=['GET','POST'])
def allorders():
    # 连接数据库
    db=MhDatabases()

    # 获取微信小程序端传来的ID
    id = str(json.loads(request.values.get("id")))
    print("id",id)

    # 根据ID在数据库中查询用户数据和表段名称
    result=db.executeQuery("select * from pcr where buyerid=%s",[id])
    column= db.executeQuery("select column_name from information_schema.COLUMNS where table_name=%s order by ordinal_position", ['pcr'])
    print(result)
    # print (column)

    # 返回查询到的结果:
    # 如果有订单，按时间整合发送给微信小程序端
    if len(result[0])!=0:
        time=result[0][5]
        total=[]
        total2=[]
        timess=[]
        timess.append(time)
        for i in range(0,len(result)):
            n=i+1
            if n<len(result):
                if result[i][5]==time and result[n][5]==time:
                    a={}
                    for j in range(0,len(result[i])):
                        a[column[j][0]]=result[i][j]
                    total.append(a)
                if result[i][5]==time and result[n][5]!=time:
                    time=result[n][5]
                    timess.append(time)
                    a = {}
                    for j in range(0,len(result[i])):
                        a[column[j][0]] = result[i][j]
                    total.append(a)
                    total2.append(total)
                    total=[]
            else:
                a = {}
                for j in range(0,len(result[i])):
                    a[column[j][0]] = result[i][j]
                total.append(a)
                total2.append(total)
        res=[]

        for i in range(0,len(total2)):
            order={"times":total2[i],"timess":timess[i]}
            res.append(order)
        print(res)
        return json.dumps(res)
    # 如果没有订单，返回暂无订单
    else:
        res="暂无订单"
        return json.dumps(res)



@app.route('/allorders',methods=['GET','POST'])
def allorders():
    # 连接数据库
    db=MhDatabases()

    # 获取微信小程序端传来的ID
    id = str(json.loads(request.values.get("id")))
    print("id",id)

    # 根据ID在数据库中查询用户数据和表段名称
    result=db.executeQuery("select * from pcr where buyerid=%s",[id])
    column= db.executeQuery("select column_name from information_schema.COLUMNS where table_name=%s order by ordinal_position", ['pcr'])
    print(result)
    # print (column)

    # 返回查询到的结果:
    # 如果有订单，按时间整合发送给微信小程序端
    if len(result[0])!=0:
        time=result[0][5]
        total=[]
        total2=[]
        timess=[]
        timess.append(time)
        for i in range(0,len(result)):
            n=i+1
            if n<len(result):
                if result[i][5]==time and result[n][5]==time:
                    a={}
                    for j in range(0,len(result[i])):
                        a[column[j][0]]=result[i][j]
                    total.append(a)
                if result[i][5]==time and result[n][5]!=time:
                    time=result[n][5]
                    timess.append(time)
                    a = {}
                    for j in range(0,len(result[i])):
                        a[column[j][0]] = result[i][j]
                    total.append(a)
                    total2.append(total)
                    total=[]
            else:
                a = {}
                for j in range(0,len(result[i])):
                    a[column[j][0]] = result[i][j]
                total.append(a)
                total2.append(total)
        res=[]

        for i in range(0,len(total2)):
            order={"times":total2[i],"timess":timess[i]}
            res.append(order)
        print(res)
        return json.dumps(res)
    # 如果没有订单，返回暂无订单
    else:
        res="暂无订单"
        return json.dumps(res)



@app.route("/showEcharts")
def showEcharts():
    #从数据库中查询数据---生成Json格式
    helper = MhDatabases()
    result=helper.executeQuery("select name,sum(total) from pcr group by name ",[])
    print(result)
    list =[]
    for i in result:
        dict ={}
        dict["name"]=i[0]   #上衣
        dict["total"]=i[1]  #966
        list.append(dict)
    res = {"result":list}
    content = json.dumps(res)
    return content

@app.route("/showEchart")
def showEchart():
    return  render_template("echarts.html")

if __name__ == '__main__':
    # CORS(app,supports_credentials=True)
    app.run(ssl_context='adhoc')
