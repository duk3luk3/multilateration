from flask import Flask, request, render_template

import gps
import data
import solve

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/mean", methods=['POST'])
def lat_mean():
    d = request.get_json()
    records = data.load_records_obj(d)

    mean = gps.get_mean_latlong([r.receiverCoord for r in records])
    import pprint
    return pprint.pformat(mean)

@app.route("/solve", methods=['POST'])
def multilaterate():
    d = request.get_json()
    records = data.load_records_obj(d)

    solve_gps, solution = solve.solve_gps(records)

    return dict(
            input=records,
            solution=solve_gps
            )

if __name__ == "__main__":
    app.run(debug=True)
