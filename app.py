# import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# import library flask sqlalchemy
from flask_sqlalchemy import Model, SQLAlchemy
import os

# inisiasi object
app = Flask(__name__)
api = Api(app)
CORS(app)

# inisiasi object flask-sqlalchemy
db = SQLAlchemy(app)

# konfigurasi database
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

# membuat database model
class ModelDatabase(db.Model):
    # membuat field/kolom
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    umur = db.Column(db.Integer)
    alamat = db.Column(db.TEXT)

    # membuat method simpan data agar simpel
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

# mencreate database
db.create_all()

# inisiasi variabel kosong bertipe dict
identitas = {}

# membuat class resource
class ContohResource(Resource):
    def get(self):
        # menampilkan data dari database sqlite
        query = ModelDatabase.query.all()

        # melakukan iterasi pada model database dengan teknik list comprehension
        output = [
            {
                "id":data.id,
                "nama":data.nama,
                "umur":data.umur,
                "alamat":data.alamat
            }
            for data in query
        ]

        response = {
            "code": 200,
            "msg": "Query data sukses",
            "data": output
        }

        return response, 200

    def post(self):
        dataName = request.form["nama"]
        dataAge = request.form["umur"]
        dataAddress = request.form["alamat"]
        
        # masukkan data ke dalam database model
        model = ModelDatabase(nama=dataName, umur=dataAge, alamat=dataAddress)
        model.save()
        
        response = {
            "msg": "Data Berhasil Ditambahkan",
            "code": 200
        }
        return response, 200

    def delete(self):
        query = ModelDatabase.query.all()
        # looping
        for data in query:
            db.session.delete(data)
            db.session.commit()

        response = {
            "msg": "semua data berhasil dihapus",
            "code": 200
        }
        return response

# membuat class baru edit & hapus data
class UpdateResource(Resource):
    def put(self, id):
        # konsumsi id untuk query db
        # pilih data yang ingin di edit berdasarkan id
        query = ModelDatabase.query.get(id)

        # form untuk edit data
        editNama = request.form["nama"]
        editUmur = request.form["umur"]
        editAlamat = request.form["alamat"]

        # mereplace nilai yang ada di field
        query.nama = editNama
        query.umur = editUmur
        query.alamat = editAlamat
        db.session.commit()

        response = {
            "msg": "edit data berhasil",
            "code": 200
        }
        return response

    # delete berdasarkan id
    def delete(self, id):
        query = ModelDatabase.query.get(id)

        # panggil method untuk delete data berdasarkan id
        db.session.delete(query)
        db.session.commit()

        response = {
            "msg": "delete data berhasil",
            "code": 200
        }
        return response


# setup resource
api.add_resource(ContohResource, "/api", methods=["GET", "POST", "DELETE"])
api.add_resource(UpdateResource, "/api/<id>", methods=["PUT","DELETE"])

if __name__ == "__main__":
    app.run(debug=True)