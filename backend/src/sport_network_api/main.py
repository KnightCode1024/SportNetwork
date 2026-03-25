from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()
    return app


app = create_app()


@app.get("/ping")
def ping():
    return {"message": "pong"}
