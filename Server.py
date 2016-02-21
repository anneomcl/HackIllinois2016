__author__ = 'RR'
from flask import Flask, render_template, request, json
import requests
import json as JSON
import urllib.parse
from decimal import Decimal
from visualization import map_balanced


app= Flask(__name__)

masterAccessToken=-1
masterDataPasser=[]


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')




@app.route('/cropImages')
def imageCaller():
    global masterDataPasser
    jsonpasser=masterDataPasser
    print(map_balanced(jsonpasser))
    return JSON.dumps(map_balanced(jsonpasser))


@app.route('/sendBounds')
def cluCaller():
    global masterDataPasser
    # here we want to get the value of the key (i.e. ?key=value)

    neValue=urllib.parse.unquote(request.args.get('NE'))
    swValue=urllib.parse.unquote(request.args.get('SW'))
    # print(neValue)
    # print(swValue)
    r=cluGetter(neValue, swValue)
    masterDataPasser=r
    print('testerPrint   ', r)
    return JSON.dumps(r)

#protobuffer

def cluGetter(ne, sw):
    ne=ne.replace('(', '').replace(')', '')
    sw=sw.replace('(', '').replace(')', '')
    neVals=ne.split(',')
    swVals=sw.split(',')
    neVals[0]=Decimal(neVals[0])
    neVals[1]=Decimal(neVals[1])
    swVals[0]=Decimal(swVals[0])
    swVals[1]=Decimal(swVals[1])

    print(masterAccessToken)
    url='https://hackillinois.climate.com/api/clus'

    params={'ne_lon': neVals[1],
    'ne_lat': neVals[0],
    'sw_lon': swVals[1],
    'sw_lat': swVals[0]}


    headers={'Authorization' : 'Bearer 08c89249-89bf-4cc3-9c4a-966ea63d695c'}

    r = requests.get(url=url,
                      params=params,
                      headers=headers)

    rFeatures=r.json()
    # try:
    #     with open("static/cods.json", 'w') as f:
    #         JSON.dump(rFeatures, f)
    # except:
    #     pass
    try:
        print(r.json()['features'][0]['geometry']['coordinates'])
    except:
        pass
    return rFeatures



@app.route('/croptimize')
def croptimizePage():
    global masterAccessToken
    oAuthReturnCode=request.args.get('code')
    url='https://climate.com/api/oauth/token'
    params={'grant_type': 'authorization_code',
    'redirect_uri':'http://127.0.0.1:5000/croptimize',
    'code':oAuthReturnCode}
    headers={'Authorization' : 'Basic ZHAxZm1zMDk5bHUzNzQ6aGJuYTlyZGQ2aTdwdWZjbmQwOW9wdXZwaGE='}
    r = requests.post(url=url,
                      params=params,
                      headers=headers)

    # masterAccessToken=json.loads(r.text)['access_token']
    print(json.loads(r.text))

    print(oAuthReturnCode)
   #print(request.args.get('code'))
    return render_template('croptimizePage.html')



@app.route('/signUp',methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
 # validate the received values
    if _name and _email and _password:
        print(_name, _email, _password)
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
