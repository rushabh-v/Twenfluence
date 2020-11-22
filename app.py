from flask import Flask, render_template, request, jsonify, redirect, flash
import sys
import scrapper
import plot


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
    hashtag = request.form['hashtag']
    if hashtag and hashtag[0] != "#":
        hashtag  = "#" + hashtag
    threshold = 10
    users, tweets = scrapper.get_users_and_tweets(hashtag)
    top_influencers, top_tweets = scrapper.get_top_influencers(hashtag, threshold, users, tweets)
    figure = plot.get_graph(top_influencers)
  
    row_template = "<tr> \
                        <td> {0} </td> \
                        <td> {1} </td> \
                        <td> {2} </td> \
                        <td> {3} </td> \
                        <td> {4} </td> \
                        <td> {5} </td> \
                        <td> {6} </td> \
                    </tr>"

    users_html = ""
    data = top_influencers["data"]
    for i, user in enumerate(data):
        linked_profile = '<a href="https://twitter.com/{0}"> {0} </a>'.format(user["username"])
        users_html += row_template.format(i+1,
                                        linked_profile,
                                        user["n_followers"],
                                        user["n_tweets"],
                                        user["total_retweets"],
                                        user["total_likes"],
                                        int(user["user_score"])
                                        )

    top_tweets_html = []
    for tweet in top_tweets:
        top_tweets_html.append(tweet["html"])
    f = open("./templates/index.html")
    text = f.read()
    text = text.replace("Top tweets", ''.join(top_tweets_html))
    text = text.replace("TI table", users_html)
    text = text.replace("_hashtag_", hashtag)

    return text

if __name__ == "__main__":
    app.run(debug=True)
