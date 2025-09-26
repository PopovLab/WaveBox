from typing import Annotated, Callable, Coroutine
from fastapi.responses import HTMLResponse, RedirectResponse
import marimo
from fastapi import FastAPI, Form, Request, Response


# Create a marimo asgi app
server = (
    marimo.create_asgi_app()
    .with_app(path="", root="./pages/index.py")
    .with_app(path="/viewer", root="./pages/viewer.py")
    .with_app(path="/settings", root="./pages/settings.py")
    .with_app(path="/about", root="./pages/about.py")
)

# Create a FastAPI app
app = FastAPI()

#app.add_middleware(auth_middleware)
#app.add_route("/login", my_login_route, methods=["POST"])

app.mount("/", server.build())

# Run the server
if __name__ == "__main__":
    import uvicorn

    #uvicorn.run(app, host="localhost", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=9000)