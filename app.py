# from flask import Flask, render_template, request, jsonify
# import os,sys,requests, json
# from random import randint

# app = Flask(__name__)

# @app.route('/')

# def home():
#   return render_template('index.html')

# @app.route('/parse',methods=['POST', 'GET'] )

# def extract():
#   text=str(request.form.get('value1'))
#   payload = json.dumps({"sender": "Rasa","message": text})
#   headers = {'Content-type': 'application/json', 'Accept':     'text/plain'}
#   response = requests.request("POST",   url="http://localhost:5005/webhooks/rest/webhook", headers=headers, data=payload)
#   response=response.json()
#   resp=[]
#   for i in range(len(response)):
#     try:
#       resp.append(response[i]['text'])
#     except:
#       continue
#   result=resp
#   return render_template('index.html', result=result,text=text)


# if __name__ == "__main__":
#   app.run(debug=True)

from flask import Flask  
from flask import render_template

# creates a Flask application with name "app"
app = Flask(__name__)

@app.route("/")
def home_page():  
    # return render_template('index.html')
    return render_template('decidim.barcelona.html')

@app.route("/procesos")
def procesos():  
    return render_template('Procesos participativos - decidim.barcelona.html')

@app.route("/procesoGuineueta")
def procesoGuineueta():  
    return render_template('ProcesoGuineueta-decidim.barcelona.html')

@app.route("/procesoGuineueta/encuentros")
def procesoGuineueta_encuentros():  
    return render_template('EncuentrosGuineueta-decidim.barcelona.html')
    
@app.route("/procesoTallerMasriera")
def procesoTallerMasriera():  
    return render_template('ProcesoTallerMasriera-decidim.barcelona.html')

@app.route("/procesoTallerMasriera/encuentros")
def procesoTallerMasriera_encuentros():  
    return render_template('EncuentrosTallerMasriera-decidim.barcelona.html')

@app.route("/procesoTallerMasriera/propuestas")
def procesoTallerMasriera_propuestas():  
    return render_template('PropuestasTallerMasriera-decidim.barcelona.html')

@app.route("/procesoParcOreneta")
def procesoParcOreneta():  
    return render_template('ParcOreneta-decidim.barcelona.html')

@app.route("/procesoParcOreneta/encuentros")
def procesoParcOreneta_encuentros():  
    return render_template('EncuentrosParcOreneta-decidim.barcelona.html')

@app.route("/procesoAvenidaMadrid")
def procesoAvenidaMadrid():  
    return render_template('ProcesoAvenidaMadrid-decidim.barcelona.html')

@app.route("/procesoAvenidaMadrid/encuentros")
def procesoAvenidaMadrid_encuentros():  
    return render_template('EncuentrosAvenidaMadrid-decidim.barcelona.html')

# run the application
if __name__ == "__main__":  
    app.run(debug=True)