'''本函数是对金蝶数据库中的送货单表头和表体进行查询，得到分列的数据进行汇总后返回。'''

# 连接sql server的库
import pyodbc

#pandas库进行数据分析
import pandas as pd


# 设置连接参数

server = '192.168.0.234'
database = 'AIS20191210135722'
username = 'sa'
password = 'Jhs16888'
DSN= 'seord'

# seordNumber= (input('请输入单号进行查询：')).upper()

# 构建连接字符串
connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};trustServerCertificate=yes'

# 连接到数据库
conn = pyodbc.connect(connection_string)
    


# 查询送货单表头数据
def query_SEord(params):

# 使用try防止异常
    try:

        # 创建游标
        cursor = conn.cursor()
        # 查询语句
        
        sql1= f"SELECT FInterID, FBillNo, FTranType, FSalType, FCustID FROM AIS20191210135722.dbo.SEOutStock WHERE FBILLNO = ?"
        print()
        # 执行查询或其他数据库操作
        cursor.execute(sql1, params)
        rows = cursor.fetchall()
        # print(rows)
        data=[]
        # 打印结果
        for row in rows:
            data.append(row)

        # 返回查询结果
    
        cursor = conn.cursor()
        # 查询语句
        
        sql2= f"SELECT FEntrySelfS0257, FEntrySelfS0240,FEntrySelfS0258,FEntrySelfS0248,FEntrySelfS0239,FEntrySelfS0244, FEntrySelfS0263 FROM AIS20191210135722.dbo.SEOutStockEntry WHERE FInterID = ?"

        # 执行查询或其他数据库操作
        cursor.execute(sql2, data[0][0])
        rows1 = cursor.fetchall()
        # 使用
        data1=[[j for j in i] for i in rows1]


        # 关闭连接
        # print(data)
        columns=['物料名称','整支规格','料号','批号','订单号','数量','备注']
        dfs= pd.DataFrame(data1,columns=columns)


        # 使用numpy把decimal格式的数字精度控制在2位。
        dfs['数量']= dfs['数量'].apply(float).round(2)
        # 使用JOIN对合并的备注进行拼接处理得到要求的字符串
        dfs['备注']= dfs['备注'].apply(lambda x: ('*'.join(x.split('*')[-3::2]).replace('M','')+ ' '))
        # print(dfs['备注'])

        #对结果进行分类汇总
        dfs= dfs.groupby('整支规格').agg({'物料名称':'first','料号':'first','批号':'first','订单号':'first','数量':'sum','备注':'sum'})
        
        #新建index名称是ID
        dfs.reset_index(drop=False,inplace=True)
        dfs.index.name= 'ID'

        #返回数据
        return dfs
    except Exception as e:
        print(f'出现错误：{e}')
        return e


# try:

#     reseponse= query_SEord(conn,(seordNumber,))

#     reseponse.to_html('result.html')
# except Exception as e:
#     print(f'出现错误：{e}')

# finally:
    conn.close()