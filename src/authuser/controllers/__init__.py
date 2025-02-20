from fastapi import APIRouter
import importlib

router = APIRouter()

routers_list = [
    "authuser.controllers.auth.router",
    "authuser.controllers.users.router"
]

for path in routers_list:
    module_path, attribute_name = path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    subrouter = getattr(module, attribute_name)
    print(f"ADDED CONTROLLER {router}")
    router.include_router(subrouter)