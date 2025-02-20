from fastapi import FastAPI
import importlib


app = FastAPI()

routers_list = [
    "authuser.controllers.router",
    "accounts.controllers.router",
    "transactions.controllers.router",
]

for path in routers_list:
    module_path, attribute_name = path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    router = getattr(module, attribute_name)
    print(f"ADDED ROUTER {router}")
    app.include_router(router)