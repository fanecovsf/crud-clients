from waitress import serve
from main import app, THREAD_ATT

if __name__ == '__main__':
    THREAD_ATT.start()
    serve(app, host='0.0.0.0', port=3000)
