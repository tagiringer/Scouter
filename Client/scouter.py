
from flask import Flask, render_template, redirect, url_for, request
from RatingAPI import *
#from requests import request
 
app = Flask(__name__)




@app.route("/", methods=['GET'])
def scouter():
    return(render_template('index.html'))

@app.route("/player", methods=['GET', 'POST'])
def player():
    if request.method == 'POST':
        rating = request.form['uscf']
        user_rating_dict = get_rating_profile(rating)

        player_id = user_rating_dict['id']
        player_name = user_rating_dict['name']
        player_standard = user_rating_dict['standard']
        player_quick = user_rating_dict['quick']

        return render_template('player_lookup.html', uscf_id = player_id, name = player_name, standard = player_standard, quick = player_quick, data = user_rating_dict)
    else:
        return render_template('player_lookup.html')

    



if(__name__=="__main__"):
    app.run()
