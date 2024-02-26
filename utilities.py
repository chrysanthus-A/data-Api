# imports
import json 
from datetime import datetime,timedelta
from dateutil import parser
from passlib.hash import pbkdf2_sha256 as Phash
import random
import pprint
import string

# variables
users_file = 'C:/Users/chrys/Documents/fervid/JS Grid/server/Users.json'
projects = 'C:/Users/chrys/Documents/fervid/JS Grid/server/projects.json'
save_loc = "C:/Users/chrys/Documents/fervid/JS Grid/mui/saved"
sessions = 'C:/Users/chrys/Documents/fervid/JS Grid/server/sessions.json'

special_chars = ['@','!','?','%','ù','$','*']
# functions

def initialize_session(user):
    session_id = get_id(user,25)
    entry = {session_id:{'user':user,'expiration':str(datetime.now()+timedelta(hours = 1))}}
    with open(sessions,'r+') as file:
        try:
            c = file.read()
            if not len(c): raise ValueError('len 0')
            c = json.loads(c)
            c[session_id] = {'user':user,'expiration':str(datetime.now()+timedelta(hours = 1))}
        except ValueError:
            c = entry
        file.truncate(0)
        file.seek(0,0)
        file.write(json.dumps(c))
    return session_id

def validate_session(id):
    with open(sessions,'r+') as file:
        try:
            c = file.read()
            if not len(c): raise ValueError('len 0')
            c = json.loads(c)
            if parser.parse(c[id]['expiration']) < datetime.now():
                return False,None
            else:
                return True,c[id]['user']
        except Exception as e :
            return False,None

def get_id(name = 'None',size = 10):
    chars = name.replace(" ","") +string.digits+string.ascii_letters
    return "".join(random.choices(chars,k = size))
def pp(jsonobj):
    pprint.pprint(jsonobj, sort_dicts=False)

def get_wsList(user):
    with open(projects,'r+') as file:
        c = json.load(file)
    return mendData(c[user])

def get_projects(user):
    with open(projects,'r+') as file:
        c = json.load(file)
        c= c[user]
    collection = [c[ws] for ws in c]
    if len(collection) > 0:
        collection = [mendData(coll)for coll in collection] 
        data = collection[0]
        for coll in collection[1:]:
            data+=coll
        return data
    else:
        return []

def get_pages(user):
    with open(projects,'r+') as file:
        c = json.load(file)
        c= c[user]
    collection = [c[ws][pj] for ws in c for pj in c[ws]]
    collection = [{entry:None} for i in collection for entry in i ]
    if len(collection) > 0:
        collection = [mendData(coll)for coll in collection] 
        data = collection[0]
        for coll in collection[1:]:
            data+=coll
        return data
    else:
        return []

def update_ws(user,ws):
    with open(users_file,'r+') as file:
        c = json.load(file)
        c[user]['workspaces'][ws] = {'ID':get_id(ws)}
        file.truncate(0)
        file.seek(0,0)
        file.write(json.dumps(c))
    with open(projects,'r+') as pfile:
        try:
            m = pfile.read()
            if not len(m): raise ValueError('len 0')
            models = json.loads(m)
            models[user][ws] = {}
        except ValueError as f:
            print(f)
            models = {user:{ws:{}}}
        pfile.truncate(0)
        pfile.seek(0,0)
        pfile.write(json.dumps(models))
    return c[user]['workspaces']
    
def AddUser(user,pwd):
    if checkCredentials(user,pwd)[0]:
            return("Username Already exists") 
    if not validate_pass(pwd):
        return('password must contain atleast 8 characters including special chanracters like @,! etc.')
    update_pass(user,pwd)
    return('Account Successfully Created, Login using the new account')


def validate_pass(pwd):

    if len(pwd)<8 :
        return False
    else:
        for x in special_chars:
            if x in pwd:
                return True
        return False     
    
def update_pass(user, pwd):
    entry = {str(user):{'pass':str(Phash.hash(pwd)),'workspaces':{}}}
    with open(users_file,"r+") as file:
        try:
            c = file.read()
            if not len(c): raise ValueError('len 0')
            c = json.loads(c)
            c[str(user)] = {'pass': str(Phash.hash(pwd)),'workspaces':{}}
        except ValueError:
            c = entry
        file.truncate(0)
        file.seek(0,0)
        file.write(json.dumps(c))


def checkCredentials(user,pwd):
    check_user,check_pass = False,False
    with open(users_file,'r') as file:
        try:
            users = json.load(file)
            if user in users.keys():
                check_user = True
                if Phash.verify(pwd,users[user]['pass']):
                        check_pass = True
        except json.decoder.JSONDecodeError:
            pass
    return check_user,check_pass

def SaveData(data,file):
    try:
        with open(f'{save_loc}{file}','w') as file:
            file.write(json.dumps(data))    
        return(True)
    except Exception:
        return (False,Exception)


def mendData(data,id = ''):
    render_tree = []
    for key, value in data.items():
        if isinstance(value, dict):
            # Recursively transform nested dictionaries
            children = mendData(value,f'{id}.{key}')
        elif isinstance(value, list):
            child = []
            for n,c in enumerate(value):
                child.append({'id':str(n), 'name':c})
            children = child
        else:
            children = [{'id':'child'+key,'name':value,'children':None}]

        # Create the RenderTree object
        id = f"{id}.{key}" if id else key
        render_tree.append({
            "id": str(id),
            "name": key,
            "children": children,
        })

    return render_tree

