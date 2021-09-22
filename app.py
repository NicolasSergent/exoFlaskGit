#  Importer flask
from flask import Flask, json, jsonify, abort, request
from flask.helpers import make_response, url_for
#  import pour mysql_flask
from flask_mysqldb import MySQL
from datetime import datetime
app = Flask(__name__)

# appel de mysql pour l'utiliser
mysql = MySQL(app)
#  configuration à la connection msql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'sakila'

#fonction qui me sert à avoir tout les acteurs
@app.route('/actor', methods=['GET'])
def get_actor():
    try:
        cur= mysql.connection.cursor()
        cur.execute("SELECT * FROM actor")
        reponse = cur.fetchall()
        cur.close()
        actors=[]
        for actor in reponse:
            actor = make_actor(actor)
            actors.append(actor)
        return jsonify([make_public_actor(actor) for actor in actors])
    except Exception as e:
        print(e)
        abort(404)

#fonction qui me permet de rechercher un acteur par id
@app.route('/actor/<int:actor_id>', methods=['GET'])
def get_actor_by_id(actor_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM actor WHERE actor_id= %s",str(actor_id))
        reponse = cur.fetchone()
        cur.close()
        return jsonify(make_public_actor(make_actor(reponse)))
    except Exception as e:
        print(e)
        abort(404)
 #fonction qui me permet de supprimer un acteur
@app.route('/actor/<int:actor_id>', methods=['DELETE'])
def delete_actor(id_actor):
    actor=get_actor_by_id(id_actor)
    try:
        cur= mysql.connection.cursor()
        cur.execute("DELETE FROM actor WHERE actor_id=%s",str(id_actor),)
        mysql.connection.commit()
        cur.close()
        return actor
    except Exception as e:
        print(e)
        return jsonify({'is': False}) 

#fonction  qui me permet d'afficher un acteur 
@app.route('/actor', methods=['POST'])
def create_actor():
    if not request.json and not "actor_id" in request.json:
        abort(400)
    try:
        # creer les champs de ma nouvelle acteur
        first_name  = request.json['first_name']
        last_name  = request.json['last_name']
        #last_update=request.json['last_update']
        # creer ma connection et envoyer à ma bdd
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO actor(first_name, last_name, last_update) VALUES(%s,%s,%s)",(str(first_name), str(last_name),datetime.utcnow()))
        mysql.connection.commit()
        cur.close()
        return jsonify({'is':True})
    except Exception as e:
        print(e)
        return jsonify({'is':False})

#fonction qui me permet de recuperer un acteur dans une liste
def make_public_actor(actor):
    public_actor={}
    for argument in actor:
            public_actor[argument]=actor[argument]
    return public_actor


def make_actor(tache_bdd):
    # print(tache_bdd)
    list_tache= list(tache_bdd)
    # print(list_tache)
    new_tache={}
    new_tache['actor_id']=str(list_tache[0])
    new_tache['first_name']=str(list_tache[1])
    new_tache['last_name']=str(list_tache[2])
    new_tache['last_update']=str(list_tache[3])
    # print(new_tache)
    return new_tache

if __name__ == '__main__':
    app.run(debug=True)

