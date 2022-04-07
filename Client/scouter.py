
from flask import Flask, render_template, redirect, url_for, request
from RatingAPI import *
#from requests import request
 
app = Flask(__name__)




@app.route("/", methods=['GET'])
def scouter():
    graph_tournaments()

    return(render_template('index.html'))

@app.route("/player_search", methods=['GET', 'POST'])
def player_search():
    if request.method == 'POST':
        firstname = request.form['fname']
        lastname = request.form['lname']

        modified_player_string = '{},{}'.format(lastname, firstname)

        get_member_results(modified_player_string)

        #print(firstname, lastname)
        return(render_template('player_search.html'))

    else:
        return(render_template('player_search.html'))

@app.route("/player", methods=['GET', 'POST'])
def player():
    if request.method == 'POST':
        selected_id = request.form['uscf']
        user_rating_dict = get_rating_profile(selected_id)

        user_tournament_dict = get_tournament_history(selected_id)
        
        for t in user_tournament_dict:
            del user_tournament_dict[t]['BeforeStandardRating']
            del user_tournament_dict[t]['BeforeQuickRating']


        
        

        player_id = user_rating_dict['id']
        player_name = user_rating_dict['name']
        player_standard = user_rating_dict['standard']
        player_quick = user_rating_dict['quick']

        return render_template('player_lookup.html', uscf_id = player_id, name = player_name, standard = player_standard, quick = player_quick, tournament_data = user_tournament_dict)
    else:
        return render_template('player_lookup.html')

    



if(__name__=="__main__"):
    app.run()
