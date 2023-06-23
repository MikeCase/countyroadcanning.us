from website import app

if app.config['ENV'] == 'prod':
    app.run(host='0.0.0.0')
else:
    app.run() 