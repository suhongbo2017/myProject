from flask import Flask ,render_template,request
from flask_bootstrap import Bootstrap5
import server_connect
import pandas as pd

app= Flask(__name__)

bootstrap= Bootstrap5(app)


@app.route('/',methods=['get','post'])
def index_page():
    try:
        data= request.form.get("inputEntry")
        # print(data)
        if data:

            data= data.upper()
            seoutId= data
            data= data.split('/')
            print("格式化输入单号：",data)
            datas= pd.DataFrame()
            for ds in data:
                df= server_connect.query_SEord(ds)
                datas= pd.concat([datas,df])
            print('合并后的内容',datas)
            # for i,d in datas.iterrows():
            #     print(d['物料名称'])
            return render_template('index.html',table= datas.iterrows(),data= seoutId)            
        else:
            datas= '查询出错，请输入查询'
            print(datas)            
            return render_template('index.html')
    except Exception as e:
        print(f'{e}')       
        return render_template('index.html')
@app.route('/print_page')
def print_page():
    return render_template('formTable.html')
if __name__ == '__main__':
    app.run(debug=True)