from flask import Flask, render_template, request, jsonify
import requests
import json
app = Flask(__name__)

@app.route('/')
def index():
   try:
      response = requests.get("http://172.18.0.3:5000/films")
      data = response.json()
      movies = []
      for movie_data in data:
         movie = {
            'id': movie_data.get('id'),
            'titre': movie_data.get('titre'),
            'realisateur': movie_data.get('realisateur'), 
            'annee': movie_data.get('annee'),
            'genre': movie_data.get('genre'),
            'description': movie_data.get('description'),
            'image': movie_data.get('url_image'),  
         }
         movies.append(movie)
      return render_template("index.html", movies=movies)
   except requests.RequestException as e:
      return f"Erreur de connexion à l'API TMDb : {str(e)}"
   
@app.route('/form')
def aff():
   return render_template("form.html")


@app.route('/traitement_fomulaire', methods = ['POST'])
def traitement_formulaire():
   image = request.files['image']
   donnees_formulaire = {
      'titre': request.form['titre'],
      'realisateur': request.form['realisateur'],
      'annee': request.form['annee'],
      'genre': request.form['genre'],
      'description': request.form['description']
   }
   files = {'image': image}
   response = requests.post("http://172.18.0.3:5000/films", data=donnees_formulaire, files=files)

   if response.status_code == 200:
      return render_template("popup_enregistrement.html")
   else:
      return "Erreur"+ response.text

@app.route('/supprimer_film/<film_id>', methods = ['DELETE'])
def supprimer_film(film_id):
    api_url = f"http://172.18.0.3:5000/films/{film_id}"  # Remplacez par l'URL réelle de votre API
    response = requests.delete(api_url)

    if response.status_code == 200:
        return jsonify({"message": "Film supprimé avec succès!"}), 200
    else:
        return jsonify({"message": "Erreur lors de la suppression du film", "error": response.text}), response.status_code

@app.route('/traitement_modification/<idFilm>', methods=['POST'])
def traitement_modification(idFilm):
   image = request.files['image']
   # Récupérer les données du formulaire
   nouvelle_donnee = {
        'titre': request.form['titre'],
        'realisateur': request.form['realisateur'],
        'annee': request.form['annee'],
        'genre': request.form['genre'],
        'description': request.form['description']
   }
   filesnew = {'image': image}
    # Envoyer une requête PATCH ou PUT à l'API pour mettre à jour le film
   api_url = f"http://172.18.0.3:5000/films/{idFilm}"
   response = requests.put(api_url, data=nouvelle_donnee, files=filesnew)

   if response.status_code == 200:
      return "Film modifié avec succès"
   else:
      return "Erreur lors de la modification du film"

@app.route('/recherche', methods=["POST"])
def recherche_films():
    terme_recherche = request.form.get('terme_recherche')

    if terme_recherche:
        api_url = f"http://172.17.0.3:5000/films/recherche?terme={terme_recherche}"
        response = requests.get(api_url)

        if response.status_code == 200:
            films = response.json()
            return render_template("search.html", films=films)
        else:
            return "Erreur lors de la recherche"

    return "Terme de recherche vide"

if __name__ == '__main__':
    app.run(debug=True)
        




   




