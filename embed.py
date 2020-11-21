import requests

def normalize_tweet_content(code):
    code = code.replace("\\\\", "")
    code = code.replace("u003C", "<")
    code = code.replace("u003E", ">")
    return code

def get_html_content(json_content):
    start = json_content.index('html":"<blockquote') + 7
    pre_n = end = json_content.index('</blockquote>') + 13
    end = json_content.index('</script>') + 9
    return json_content[start:pre_n] + json_content[pre_n+1:end]

def get_tweet_html(tweet_id):
    url = ("https://publish.twitter.com/oembed?"
        "url=https://twitter.com/Interior/status/{}".format(tweet_id))
    r = requests.get(url, allow_redirects=True)
    json_content = normalize_tweet_content(str(r.content))
    return get_html_content(json_content)
