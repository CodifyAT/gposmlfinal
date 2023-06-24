from flask import Flask, render_template,jsonify,request
import pickle

app=Flask(__name__,static_folder='static')

def get_h():
    with open('/Users/atharvt14/Desktop/gposmlfinal/dataheight.pkl','rb') as h:
        model=pickle.load(h)
    return model

def get_s():
    with open('/Users/atharvt14/Desktop/gposmlfinal/datasubpopulation.pkl', 'rb') as s:
        model=pickle.load(s)
    return model

def get_y():
    with open('/Users/atharvt14/Desktop/gposmlfinal/datayield.pkl', 'rb') as y:
        model=pickle.load(y)
    return model

def strconv(a):
    leg = {'A': '1', 'C': '3', 'G': '4', 'T': '4'}
    seqq = ""
    for j in a:
        seqq += leg[j]
    return int(seqq)

@app.route('/')
def index():
    return render_template("Home.html")

@app.route('/GetData')
def getdata():
    return render_template("Datasets.html")

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        modh=get_h()
        mods=get_s()
        mody=get_y()

        genseq=request.form['gene_sequence']
        finalseq=strconv(genseq)

        prheight=modh.predict([[finalseq]])
        prheight=prheight[0]

        prsubpop=mods.predict([[finalseq]])
        prsubpop=prsubpop[0]

        pryield=mody.predict([[finalseq]])
        pryield=pryield[0]

        return jsonify({'Sequence':genseq,'Predicted_Height':prheight,'Predicted_Subpopulation':prsubpop,'Predicted_Yield':pryield})


if __name__=="__main__":
    app.run(debug=True)
