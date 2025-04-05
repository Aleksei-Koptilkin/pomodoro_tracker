from handlers.endpoint_tasks import router as task_router
from handlers.ping import router as ping_router
from handlers.endpoint_user import router as user_router
from handlers.endpoint_auth import router as auth_router


routers = [task_router, ping_router, user_router, auth_router]