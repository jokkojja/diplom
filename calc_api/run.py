from flask import Flask, request, jsonify
import subprocess
from config import CALCULATOR_PATH, PROG_NAME_CPP, PROG_NAME_EXE
import os

app = Flask(__name__)

@app.route('/calc', methods=['POST'])
def calc():
    try:
        content = request.json
    except Exception:
        return app.make_response(('Failure: invalid JSON!\n', 500))
    
    subprocess.run([f"g++ -o ../{os.path.join(CALCULATOR_PATH, PROG_NAME_EXE)} ../{os.path.join(CALCULATOR_PATH, PROG_NAME_CPP)}"], shell=True)
    try:
        cmd = f'../{os.path.join(CALCULATOR_PATH, PROG_NAME_EXE)} '
        for i in content.values():
            cmd += str(i) + ' '
        subprocess.run([cmd], shell=True)
        print(cmd)
        return app.make_response(('Started process!\n', 200))
    except Exception:
        return app.make_response(('Failure. Problem with starting proocess!\n', 500))
    

if __name__ == '__main__':
    app.run(debug=True, port=8051)
