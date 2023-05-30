import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

# Path ke file konfigurasi Firebase Admin SDK yang Anda dapatkan dari Firebase Console
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
collection_ref = db.collection('post')

timestamp = datetime.datetime.now()

data = {
    'text':  str(input("masukan kata-kata: ")),
    'timestamp': timestamp.isoformat()
}

collection_ref.add(data)

print('Data berhasil dikirim')