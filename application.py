from app import application


"""
This is the entry point for the application container (asgi/wsgi)
in the app. It can be coupled with asgi or other relevant gateway
interface for proper production setup. Currently, it is
using nothing but is only a design provision.
"""
application()
