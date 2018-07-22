from quart import Quart

app = Quart(__name__)


@app.route('/')
async def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
