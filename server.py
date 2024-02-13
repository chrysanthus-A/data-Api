import flask,json
from flask_cors import CORS
from flask import jsonify,request
from datetime import datetime

save_loc = "C:/Users/chrys/Documents/fervid/JS Grid/mui/saved"
app = flask.Flask('data-handler')
CORS(app)
app.config['DEBUG'] = True

@app.route('/save',methods=['post','Get'])
def save():
    data = request.data
    data = json.loads(data)
    filename = '/' + str(data['file'])
    content = data['data']
    with open(f'{save_loc}{filename}','w') as file:
        file.write(json.dumps(content))
    return ('request ok' )

@app.route('/time',methods=['Get'])
def gettime():
    time = str(datetime.now())
    time = time.split('.')[0]
    date,time = time.split(' ')
    print(time)
    print(date)
    response = jsonify({'date':date,'time':time})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    



app.run()