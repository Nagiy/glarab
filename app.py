from flask import Flask, redirect, url_for
import channel

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/init/<code>')
def api_init(code):
    return channel.initDevice(code)

@app.route('/channels')
def api_channels():
    return 'List of ' + url_for('api_channels')

@app.route('/channels/<channelid>')
def api_channel(channelid):
    url = channel.getStreamingURL(channelid)
    return url
    #return redirect(url, code=302)

def setup_app(app):
   # All your initialization code
   channel.initDevice()

setup_app(app)

if __name__ == '__main__':
    app.run()
