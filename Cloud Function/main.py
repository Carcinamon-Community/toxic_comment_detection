import firebase_admin
from firebase_admin import credentials, firestore
import requests
from flask import Flask

app = Flask(__name__)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


@app.route("/", methods=["GET","POST"])
def index():
    def get_latest_firestore_data(collection_name, field_name):
        db = firestore.client()

        collection_ref = db.collection(collection_name)
        query = collection_ref.order_by(field_name, direction=firestore.Query.DESCENDING).limit(1)

        docs = query.get()

        last_doc = docs[0]

        global doc_ref
        doc_ref = db.collection(collection_name).document(last_doc.id)

        firestore_data = last_doc.to_dict()

        return firestore_data


    try:
        collection_name = 'post'
        field_name = 'timestamp'
        
        latest_data = get_latest_firestore_data(collection_name, field_name)

        text = latest_data.get('text')

        resp = requests.post("https://getprediction-ccobiytmvq-et.a.run.app", data={'sentence': text})

        json_response = resp.json()
        prediction = json_response.get('prediction')

        print(json_response)
        #print('Hasil prediksi:', prediction)

        if prediction > 0.5: #treshold untuk dianggap sebagai kalimat/paragraf toxic
            doc_ref.delete()
            print("dokumen di hapus karena toxic")

    except requests.exceptions.JSONDecodeError as e:
        print("Terjadi kesalahan dalam memparsing respons JSON:", str(e))

    return "OK"

if __name__ == "__main__":
    app.run(debug=True)