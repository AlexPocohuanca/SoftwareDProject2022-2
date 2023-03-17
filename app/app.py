'''Main project'''

import socket
import bcrypt
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import pandas as pd
import numpy as np



#create object FLask
app = Flask(__name__)

# mysql database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'save'

mysql = MySQL(app)

#key secret - msj flask
app.secret_key='mysecretkey'

### encrypted
semilla = bcrypt.gensalt()

HOST = 'localhost'
PORT = 50008

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((HOST, PORT))


############################################################################################

def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message)


@app.route('/')
def main():
    if 'user' in session:
        return redirect(url_for('dashboardSD'))   
    else:
        return render_template('pages-login.html')
    #return render_template('pages-login.html')


@app.route('/login', methods=["GET","POST"])    
def login():
    if request.method == "GET":
        if 'user' in session:
            return redirect(url_for('dashboardSD'))   
        else:
            return redirect(url_for('main'))
    else:
        username = request.form['usernameL']
        password = request.form['passwwordL']
        password_encode = password.encode("utf-8")

        cur = mysql.connection.cursor()  # run cursor
        #Query to login#
        sQuery = "SELECT names, email,account,company,position,username, password, country, id FROM login WHERE username = %s "
        cur.execute(sQuery,[username])

        usuario = cur.fetchone() # get data
        cur.close() #close query
    #verify data 
    if (usuario != None ) : 
        password_encriptado_encode = usuario[6].encode() #***

        if (bcrypt.checkpw(password_encode,password_encriptado_encode)):
            cur = mysql.connection.cursor()  # run cursor
            #Query to login#
            sQuery = "SELECT empresa FROM empresas WHERE id = %s "
            cur.execute(sQuery,[usuario[3]])
            usuario=usuario+cur.fetchone() # get data
            cur.close() #close query

            session['user'] = usuario[5] #*****
            session['name'] = usuario[0]
            session['email'] =usuario[1] 
            session['pos'] = usuario[4]
            session['account'] =usuario[2] 
            session['company'] = usuario[3]
            session['country'] = usuario[7]
            session['id'] = usuario[8]
            session['companyname'] = usuario[9]
            
            return redirect(url_for('dashboardSD'))   
        else: 
            flash('Password incorrect')
            return redirect(url_for('main'))
    else :  
        flash("El usuario no existe")
        return redirect(url_for('main'))     
############################################################################################

@app.route('/register', methods =["GET","POST"])
def register():

    if (request.method =="GET"):
        if 'user' in session: 
            return render_template('index.html') 
        else:

            cur = mysql.connection.cursor()  # run cursor
            sQuery = f"select * from empresas"
            cur.execute(sQuery)
            empresas = cur.fetchall() # get data
            cur.close() #close query
            return render_template('pages-register.html',empresas=empresas)
    else:
        names = request.form['nameR']
        email = request.form['emailR']
        account = request.form['rol']
        company = request.form['companyR']
        
        position = request.form['positionR']
        username = request.form['usernameR']
        password = request.form['passwordR']
        country= request.form['countryR']


        password_encode = password.encode("utf-8")
        password_encriptado = bcrypt.hashpw(password_encode, semilla)
        #Prepare Query 
        sQuery = "INSERT into login (names, email,account,company,position,username, password, country) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

        cur = mysql.connection.cursor()

        cur.execute(sQuery,(names, email,account,company,position,username, password_encriptado, country))
        mysql.connection.commit()

        ##Login session 
        ##session['user'] = username
        ##session['name'] = names
        ##session['email'] = email
        ##session['user'] = username
        ##session['pos'] = position
        ##session['account'] = account
        ##session['company'] = company
        ##session['country'] = country
        session.clear()
        return redirect(url_for('login'))



##############################################################################################

##### ##### ##### #####   ####  #####  ###  #   # #####
#     #   # #       #     #   # #   #   #   #   # #
##### #   # ####    #     #   # #####   #   #   # ####
    # #   # #       #     #   # # #     #    # #  #
##### ##### #       #     ####  #  ##  ###    #   #####

##############################################################################################


@app.route('/dashboardSD', methods =["GET","POST"])
def dashboardSD():

   

    cur = mysql.connection.cursor()  # run cursor
    sQuery = f"SELECT C.id, C.nombre,R.cnt FROM conductores as C INNER JOIN dispositivos as D ON C.id=D.conductor INNER JOIN (SELECT ID_dispositivo, COUNT(ID_dispositivo) as cnt FROM incidentes group by ID_dispositivo)as R ON R.ID_dispositivo=D.id where C.empresa= %s order by R.cnt desc limit 3;"
    cur.execute(sQuery,str(session['company']))
    peligros = cur.fetchall() # get data
    sQuery = f"SELECT R.cnt FROM dispositivos as D INNER JOIN (SELECT ID_dispositivo, COUNT(ID_dispositivo) as cnt FROM incidentes group by ID_dispositivo)as R ON R.ID_dispositivo=D.id where D.empresa=%s;"
    cur.execute(sQuery,str(session['company']))
    lista_incidentes = cur.fetchall() # get data
    sQuery = f"select dispositivos.id,dispositivos.conductor from dispositivos where empresa=%s;"
    cur.execute(sQuery,str(session['company']))
    lista_dispositivos = cur.fetchall() # get data
    cur.close() #close query


    tasa_prevencion = 85
    aceptacion_usuario = 85
    incidentes_total = sum([pair[0] for pair in lista_incidentes])


    dispositivos_activos = len( lista_dispositivos)
    return render_template('dashboardSD.html', peligros=peligros, tasa_prevencion=tasa_prevencion,aceptacion_usuario=aceptacion_usuario,incidentes_total=incidentes_total,dispositivos_activos=dispositivos_activos)

@app.route('/conductoresSD', methods =["GET","POST"])
def conductoresSD():

    cur = mysql.connection.cursor()  # run cursor
    #Query to fetch all drivers#
    sQuery = "SELECT C.id, C.nombre, C.email, C.empresa, C.activo, D.id as idDisp, R.cnt FROM conductores as C INNER JOIN dispositivos as D ON C.id=D.conductor INNER JOIN (SELECT ID_dispositivo, COUNT(ID_dispositivo) as cnt FROM incidentes group by ID_dispositivo)as R ON R.ID_dispositivo=D.id where C.empresa=%s ;"
    cur.execute(sQuery, str(session['company']))
    conductoresreg = cur.fetchall() # get data
    sQuery = "SELECT C.id, C.nombre, C.email, C.empresa, C.activo FROM conductores as C where C.empresa=%s ;"
    cur.execute(sQuery, str(session['company']))
    conductorestot = cur.fetchall() # get data
    cur.close() #close query
    return render_template('conductoresSD.html', conductoresreg=conductoresreg,conductorestot=conductorestot)


@app.route('/tablasSD', methods = ["GET","POST"])
def tablasSD():
    cur = mysql.connection.cursor()  # run cursor
    #Query to fetch all incidents#
    sQuery = " select incidentes.id,incidentes.ID_dispositivo,incidentes.tipo_incidente,incidentes.max_vel from dispositivos INNER JOIN incidentes ON dispositivos.id=incidentes.ID_dispositivo where empresa= %s; "
    cur.execute(sQuery,str(session['company']))
    incidentes = cur.fetchall() # get data
    cur.close() # close query

    return render_template('tablasSD.html', incidentes = incidentes)

@app.route('/formularioSD', methods =["GET","POST"])
def formularioSD():
    return render_template('formularioSD.html')

@app.route('/registerdriver', methods =["GET","POST"])
def registerdriver():

    if (request.method =="POST"):
        names = request.form['nameR']
        email = request.form['emailR']
        company = session['company']
        active = request.form['isActive']

        #Prepare Query 
        sQuery = "INSERT into conductores (nombre, email,empresa,activo) VALUES (%s,%s,%s,%s)"

        cur = mysql.connection.cursor()

        cur.execute(sQuery,(names, email,company,active))
        mysql.connection.commit()

        flash("Conductor añadido a la base de datos")
        return redirect(url_for('formularioSD'))    

@app.route('/changecompany', methods =["POST"])
def changecompany():

    if (request.method =="POST"):
        company = request.form['companyR']
        session['company'] = company
        if company=='1':
            session['companyname'] = 'Chama'
        elif company=='2':
            session['companyname'] = 'Movil'
        elif company=='3':
            session['companyname'] = 'Acvdo'
        else:
            session['companyname'] = 'Empresa'
        flash("Empresa cambiada a: "+ session['companyname'])
        return redirect(url_for('general'))    



@app.route('/graficosSD', methods =["GET","POST"])
def graficosSD():


#select tipo_incidente,AVG(I.max_vel) as prom from dispositivos as D INNER JOIN incidentes as I ON I.ID_dispositivo=D.id WHERE empresa=1 group by tipo_incidente;


    cur = mysql.connection.cursor()  # run cursor
    sQuery = f"SELECT C.nombre,R.cnt FROM conductores as C INNER JOIN dispositivos as D ON C.id=D.conductor INNER JOIN (SELECT ID_dispositivo, COUNT(ID_dispositivo) as cnt FROM incidentes group by ID_dispositivo)as R ON R.ID_dispositivo=D.id where C.empresa= %s order by R.cnt desc;"
    cur.execute(sQuery,str(session['company']))
    peligros = cur.fetchall() # get data
    
    sQuery = f" SELECT tipo_incidente, COUNT(R.tipo_incidente) FROM dispositivos as D INNER JOIN incidentes as R ON R.ID_dispositivo=D.id where empresa=%s group by D.empresa,R.tipo_incidente;"
    cur.execute(sQuery,str(session['company']))
    cuentatipos = cur.fetchall() # get data

    sQuery = f" select tipo_incidente,AVG(I.max_vel) as prom from dispositivos as D INNER JOIN incidentes as I ON I.ID_dispositivo=D.id WHERE empresa=%s group by tipo_incidente;"
    cur.execute(sQuery,str(session['company']))
    promediovel = cur.fetchall() # get data

    sQuery = f" SELECT C.nombre,R.tipo_incidente,cntfinal FROM conductores as C INNER JOIN dispositivos as D on C.id=D.conductor INNER JOIN (SELECT ID_dispositivo,tipo_incidente, COUNT(tipo_incidente) as cntfinal FROM incidentes group by ID_dispositivo, tipo_incidente) as R on R.ID_dispositivo=D.id INNER JOIN (SELECT C1.nombre,R1.cnt FROM conductores as C1 INNER JOIN dispositivos as D1 ON C1.id=D1.conductor INNER JOIN (SELECT ID_dispositivo, COUNT(ID_dispositivo) as cnt FROM incidentes group by ID_dispositivo)as R1 ON R1.ID_dispositivo=D1.id where C1.empresa=%s order by R1.cnt desc limit 1) as AUX ON C.nombre=AUX.nombre where C.empresa=%s;"
    cur.execute(sQuery,(str(session['company']),str(session['company'])))
    maspeligroso = cur.fetchall() # get data

    cur.close() #close query
    return render_template('graficosSD.html',peligros=peligros,cuentatipos=cuentatipos,promediovel=promediovel,maspeligroso=maspeligroso)

@app.route('/UISD', methods =["GET","POST"])
def UISD():
    return render_template('UISD.html')

























@app.route('/index')
def index():

    if 'user' in session:

        """
        #     session['data'] = [3, 90, 4, 5, 6, 7, 8]
        #     return render_template('index.html')
        # else:
        #     return redirect(url_for('main'))
        if 'user' in session:
            cur = mysql.connection.cursor()
            # Query = f'SELECT names, date from emotions where usuario_id={session["id"]}' 
            # cur.execute(Query)
            # rows= cur.fetchall()
            cur.close()
            # df = pd.DataFrame([[ij for ij in i] for i in rows])
            # df.rename(columns={0: 'Name', 1:'Date'}, inplace =True)
            # print('-'*80)

            # df.groupby('Name')['C:onfiability'].apply(lambda group_series:group_series.tolist()).reset_index()
            df['Day'] = df['Date'].dt.date
            df =df.groupby(['Day', 'Name'], as_index=False).agg('count')
            df.rename(columns={'Date': 'value'}, inplace =True)
            df.sort_values(by=['Day'], inplace=True)
            # df = fill_df(df)

            # happy=df.loc[df['Name']=='HAPPY']
            # if not happy.empty:
            #     session['happyvalues']= happy['value']
            # sad=df.loc[df['Name']=='SAD']
            # if not sad.empty:
            #     session['sadvalues']= sad['value']
            # angry=df.loc[df['Name']=='ANGRY']
            # if not angry.empty:
            #     session['angryvalues']= angry['value']
            # confuse=df.loc[df['Name']=='CONFUSED ']
            # if not confuse.empty:
            #     session['confusevalues']= confuse['value']
            # disgus=df.loc[df['Name']=='DISGUSTED']
            # if not disgus.empty:
            #     session['disgusvalues']= disgus['value']

            # sup=df.loc[df['Name']=='SURPRISED']
            # if not sup.empty:
            #     session['supvalues']= sup['value']

            # calm=df.loc[df['Name']=='CALM']
            # if not calm.empty:
            #     # session['x-axis'] =  ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
            #     session['calmvalues']= calm['value'].to_list()
            #     data = calm['value'].to_list()
            #     print(data)
            #     # session['x-axis'] = list(range(len(data)))
            #     # session['x-axis'] = [0, 1]
            #     # session['x-axis']= calm['Day'].astype(str).to_list()
            #     # session['x-axis']  = ['01/01/21 12:20', '02/02/21 14:00']
            #     date_list  = ['12/11/22 12:20', '11/11/22 14:00']
            #     # session['x-axis'] =  ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z"]

            emotions = ['CALM', 'CONFUSED', 'SAD']
            for emotion in emotions:
                emotiondf=df.loc[df['Name']== emotion]
                if not emotiondf.empty:
                    # session['x-axis'] =  ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
                    session[f'{emotion.lower()}values'] = emotiondf['value'].to_list()
                    data = emotiondf['value'].to_list()
                    date_list  = ['12/11/22 12:20', '11/11/22 14:00']
                    # session['x-axis'] =  ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z"]
            # fear=df.loc[df['Name']=='FEAR']
            # if not fear.empty:
            #     session['fearvalues']= fear['value']
            """

        return render_template('index.html', dlist=date_list)
    else:
        return redirect(url_for('main'))




@app.route('/uploadVideo', methods=['POST'])
def upload_video():
    '''Handler when the user press submit button in the forms'''
    dir_save_path = 'videos'
    if request.method == 'POST':
        print('request form:\n', request.form)
        uploaded_file = request.files['file']
        curso = request.args.get("curso")
        if uploaded_file.filename != '':
            path_to_save = dir_save_path + '/' + uploaded_file.filename
            uploaded_file.save(path_to_save)
            print(f'saved succesfull in {path_to_save}')
            # send_message(b'connected')
            send_message(str.encode(f'{uploaded_file.filename};{session["id"]}; {curso}'))
            print(f'sending: {uploaded_file.filename}')
    return redirect('/forms')

@app.route('/uploadCsvAttendance', methods=['POST'])
# rn it is basically a copy of upload_video; update so that it posts data directly to the db
def upload_csv_attendance():
    dir_save_path = 'attendance_records'
    if request.method == 'POST':
        print('request form:\n', request.form)
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            path_to_save = dir_save_path + '/' + uploaded_file.filename
            uploaded_file.save(path_to_save)
            print(f'saved succesful in {path_to_save}')
            # send_message(b'connected')
            send_message(str.encode(f'{uploaded_file.filename};{session["id"]}'))
            print(f'sending: {uploaded_file.filename}')
    return redirect('/forms')

@app.route('/uploadCsvGrades', methods=['POST'])
# rn it is basically a copy of upload_video; update so that it posts data directly to the db
def upload_csv_grades():
    dir_save_path = 'grades_records'
    if request.method == 'POST':
        print('request form:\n', request.form)
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            path_to_save = dir_save_path + '/' + uploaded_file.filename
            uploaded_file.save(path_to_save)
            print(f'saved succesful in {path_to_save}')
            # send_message(b'connected')
            send_message(str.encode(f'{uploaded_file.filename};{session["id"]}'))
            print(f'sending: {uploaded_file.filename}')
    return redirect('/forms')


@app.route('/exit')
def flask_exit():
    session.clear()
    return redirect(url_for('main'))

@app.route('/forms')
def about():
    if 'user' in session:
        return render_template('forms-elements.html')
    else :
        return redirect(url_for('main'))

@app.route('/component')
def component():
    if 'user' in session:   
        return render_template('components-progress.html')
    else :
        return redirect(url_for('main'))
    

@app.route('/accordion')
def accordion():
    if 'user' in session:   
        return render_template('components-accordion.html')
    else :
        return redirect(url_for('main'))
    

@app.route('/echarts')
def echarts():
    if 'user' in session:   
        return render_template('charts-echarts.html')
    else :
        return redirect(url_for('main'))
    

@app.route('/chartjs')
def chartjs():
    if 'user' in session:   
        return render_template('charts-chartjs.html')
    else :
        return redirect(url_for('main'))
    
@app.route('/apex')
def apex():
    if 'user' in session:   
        return render_template('charts-apexcharts.html')
    else :
        return redirect(url_for('main'))

@app.route('/contact')
def contact():
    if 'user' in session:   
        return render_template('pages-contact.html')
    else :
        return redirect(url_for('main'))
    

@app.route('/profile')
def profile():
    if 'user' in session:   
        return render_template('users-profile.html')
    else :
        return redirect(url_for('main'))
    

@app.route('/tabledata')
def tabledata():
    if 'user' in session and session['account'] == 'Administrator':
        cur = mysql.connection.cursor()  
        Query = f'SELECT * from video' 
        cur.execute(Query)
        data = cur.fetchall()
        return render_template('tables-data.html', video=data)   
    else :
        return redirect(url_for('denegado'))

    
@app.route('/general')
def general():
    if 'user' in session and session['account'] == 'admin': 
        cur = mysql.connection.cursor()  # run cursor
        sQuery = f"SELECT C.nombre,R.cnt FROM conductores as C INNER JOIN dispositivos as D ON C.id=D.conductor INNER JOIN (SELECT ID_dispositivo, COUNT(ID_dispositivo) as cnt FROM incidentes group by ID_dispositivo)as R ON R.ID_dispositivo=D.id order by R.cnt desc;"
        cur.execute(sQuery)
        peligros = cur.fetchall() # get data
        
        sQuery = f" SELECT tipo_incidente, COUNT(R.tipo_incidente) FROM dispositivos as D INNER JOIN incidentes as R ON R.ID_dispositivo=D.id group by R.tipo_incidente;"
        cur.execute(sQuery)
        cuentatipos = cur.fetchall() # get data

        sQuery = f" select tipo_incidente,AVG(I.max_vel) as prom from dispositivos as D INNER JOIN incidentes as I ON I.ID_dispositivo=D.id group by tipo_incidente;"
        cur.execute(sQuery)
        promediovel = cur.fetchall() # get data

        sQuery = f" SELECT C.nombre,R.tipo_incidente,cntfinal FROM conductores as C INNER JOIN dispositivos as D on C.id=D.conductor INNER JOIN (SELECT ID_dispositivo,tipo_incidente, COUNT(tipo_incidente) as cntfinal FROM incidentes group by ID_dispositivo, tipo_incidente) as R on R.ID_dispositivo=D.id INNER JOIN (SELECT C1.nombre,R1.cnt FROM conductores as C1 INNER JOIN dispositivos as D1 ON C1.id=D1.conductor INNER JOIN (SELECT ID_dispositivo, COUNT(ID_dispositivo) as cnt FROM incidentes group by ID_dispositivo)as R1 ON R1.ID_dispositivo=D1.id order by R1.cnt desc limit 1) as AUX ON C.nombre=AUX.nombre;"
        cur.execute(sQuery)
        maspeligroso = cur.fetchall() # get data

        cur.close() #close query
        return render_template('tables-general.html', peligros=peligros,cuentatipos=cuentatipos,promediovel=promediovel,maspeligroso=maspeligroso)
    else :
        return redirect(url_for('denegado'))

@app.route('/usuarios')
def usuarios():
    if 'user' in session and session['account'] == 'Administrator': 
        cur = mysql.connection.cursor()  
        Query = f'SELECT * from login' 
        cur.execute(Query)
        data = cur.fetchall()
        return render_template('usuarios.html', login=data)
    else :
        return redirect(url_for('denegado'))

@app.route('/alumnos')
def alumnos():
    if 'user' in session and session['account'] == 'Administrator': 
        cur = mysql.connection.cursor()  
        Query = f'SELECT * from alumnos' 
        cur.execute(Query)
        data = cur.fetchall()

        # geting the emotion table
        #         cur = mysql.connection.cursor()
        # Query = f'SELECT names, date from emotions where usuario_id={session["id"]}' 
        # cur.execute(Query)
        # rows= cur.fetchall()
        # cur.close()
        # df = pd.DataFrame([[ij for ij in i] for i in rows])
        # df.rename(columns={0: 'Name', 1:'Date'}, inplace =True)
        # print('-'*80)

        # df['Day'] = df['Date'].dt.date
        # df =df.groupby(['Day', 'Name'], as_index=False).agg('count')
        # df.rename(columns={'Date': 'value'}, inplace =True)
        # df.sort_values(by=['Day'], inplace=True)

        # emotions = ['CALM', 'CONFUSED', 'SAD']
        # for emotion in emotions:
        #     emotiondf=df.loc[df['Name']== emotion]
        #     if not emotiondf.empty:
        #         session[f'{emotion.lower()}values'] = emotiondf['value'].to_list()
        #         data = emotiondf['value'].to_list()
        #         date_list  = ['12/11/22 12:20', '11/11/22 14:00']

        return render_template('alumnos.html', login=data, dlist=date_list)
    else :
        return redirect(url_for('denegado'))
    
@app.route('/error')
def error():
    return render_template('pages-error-404.html')

@app.route('/denegado')
def denegado():
    return render_template('notadmin.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
