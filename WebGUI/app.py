from quart import Quart

app = Quart(__name__)

@app.route("/")
async def hello():
    return "Hello!"

@app.route("/<name>")
async def name(name):
    return f"Hello {name}"



app.run(port=80, debug=True)