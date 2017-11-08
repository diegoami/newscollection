from . import app

@app.route('/reload')
def reload():
    app.application.reload()
    return "Models refreshed", {'Content-Type': 'text/html'}

