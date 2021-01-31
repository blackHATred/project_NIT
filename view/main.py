from sanic import Sanic
from tortoise.contrib.sanic import register_tortoise

from config.configuration import host, port, DB_URL
from view.routes import all_routes


app = Sanic("Project_for_NIT")
register_tortoise(
    app,
    db_url=DB_URL,
    modules={'models': ['model.User', 'model.Msg', 'model.Upload']},
    generate_schemas=True
)


if __name__ == "__main__":
    all_routes(app=app)
    app.run(host=host,
            port=port)
