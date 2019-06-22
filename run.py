from app import app
import sys

server = app.server
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug=True
    else:
        debug=False
    app.run_server(debug=debug)

    