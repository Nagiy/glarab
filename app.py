from flask import Flask, redirect, url_for
import channel

app = Flask(__name__)


@app.route('/')
def api_root():
    return 'Welcome'


@app.route('/channels')
def api_channels():
    return 'List of ' + url_for('api_channels')


@app.route('/channels/<channelid>')
def api_channel(channelid):
    url = channel.getGLArabURL(channelid)
    return redirect(url, code=302)


if __name__ == '__main__':
    app.run()
