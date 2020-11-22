from flask import Flask, render_template, request, jsonify, redirect, flash
import sys
import scrapper

app = Flask(__name__)
@app.errorhandler(404)
def not_found(error):
  resp = jsonify( { 
    u'status': 404, 
    u'message': u'Resource not found' 
    })
  resp.status_code = 404
  return resp

@app.route('/',methods=['GET'])
def search():
    return render_template('search.html')

@app.route("/experts",methods=['GET','POST'])
def experts():
  hashtag = "#" + request.form['hashtag']
  threshold = 10
  location = ""
  language = ""
  users, tweets = scrapper.get_users_and_tweets(hashtag)
  top_influencers, top_tweets = scrapper.get_top_influencers(hashtag, threshold, users, tweets)
  return render_template('index.html',hashtag=hashtag, top_influencers=top_influencers, top_tweets=top_tweets)


if __name__ == "__main__":
  app.run(debug=True)
