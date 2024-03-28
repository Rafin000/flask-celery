# from celery import Celery

from project import create_app , ext_celery, socketio

app = create_app()

celery = ext_celery.celery
# celery = Celery(
#     __name__,  
#     broker = "redis://127.0.0.1:6379/0",
#     backend= "redis://127.0.0.1:6379/0"
# )

@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == '__main__':
    socketio.run(
        app,
        debug=True,
        allow_unsafe_werkzeug=True, 
        use_reloader=True,
        host='0.0.0.0',
    )
# @celery.task
# def divide(x,y):
#     import time
#     time.sleep(5)
#     return x/y


