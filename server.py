import flask,json
from flask_cors import CORS
from flask import jsonify,request,session,make_response
from datetime import datetime,timedelta
import utilities as ut
import os
import logging



app = flask.Flask('data-handler')
CORS(app, supports_credentials=True,origins=[r'http://localhost:5173/*'])
logging.getLogger('flask_cors').level = logging.DEBUG
app.config["SESSION_PERMANENT"] = True
app.config['SESSION_TYPE'] = 'memcache'
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.secret_key = "mysecret"
# Session(app)
# Session.session_lifetime = timedelta(minutes=1)

# functions
def get_cred(request):
    data = json.loads(request.data)
    user = data['user']
    pwd = data['pwd'] 
    # token = data['auth'] 
    return user,pwd

@app.route('/login',methods=['post','get'])
def login():
    user,pwd = get_cred(request)
    if all(ut.checkCredentials(user,pwd)):
        token= ut.initialize_session(user)
        response = make_response({'auth':'Login Authorized','code':200,'status':'Authorization Sucessfull', 'auth_token':token})
        return response #code 200 reserved for successfull auth

    return jsonify({'auth':'Check Username and Password','code':400,'status':'Credentials not Authorised'})
    

@app.route('/newuser',methods=['post','get'])
def createuser():
    user,pwd = get_cred(request) 
    user_status = ut.AddUser(user,pwd)
    response = jsonify({'auth' :user_status,'status':'200 OK'})
    return response
    
@app.route('/save',methods=['post','Get'])
def save():
    data = json.loads(request.data)
    filename = '/' + str(data['file'])
    content = data['data']
    status = ut.SaveData(content,filename)

@app.route('/time',methods=['Get'])
def gettime():
    time = str(datetime.now())
    time = time.split('.')[0]
    date,time = time.split(' ')
    response = jsonify({'date':date,'time':time})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/workspaces/tree',methods=['Get','POST'])
def WS():
    def get_D():
        auth = request.headers['auth']
        valid_session,user=ut.validate_session(auth)
        if valid_session:
                response = jsonify(ut.get_wsList(user))
                return response 
        return jsonify({'response':'Bad Request','code':401})
        
    def addWS():
        auth = request.headers['auth']
        valid_session,user = ut.validate_session(auth)
        data = json.loads(request.data)
        ws_name = data['name']
        if valid_session:
                data = ut.update_ws(user,ws_name)
                return jsonify(ut.mendData(data))
        return jsonify({'response':'Bad Request','code':401})
        
    if request.method == 'GET':
        return get_D()
    elif request.method == 'POST':
        return addWS()
    
@app.route('/pages/tree',methods=['Get','POST'])
def PG():
    def get_D():
        auth = request.headers['auth']
        valid_session,user=ut.validate_session(auth)
        if valid_session:
                response = jsonify(ut.get_pages(user))
                return response 
        return jsonify({'response':'Bad Request','code':401})
    return get_D()
# TODO: implement logic for adding pages to projects

@app.route('/projects/tree',methods=['Get','POST'])
def PJ():
    def get_D():
        auth = request.headers['auth']
        valid_session,user=ut.validate_session(auth)
        if valid_session:
                response = jsonify(ut.get_projects(user))
                return response 
        return jsonify({'response':'Bad Request','code':401})
    return get_D()
# TODO: rouute for adding projects

app.run()