import re, ipdb, asyncio
from urllib import parse
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.sessions import CookieMiddleware, SessionMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import parse_cookie
from knox.auth import TokenAuthentication

User = get_user_model()

def extract_chat_segment(url):
    """
    Extract the segment between /ws/chat/ and the next / from a given URL.

    :param url: The URL string to be parsed
    :return: The extracted segment or None if not found
    """
    # Regex pattern to capture the segment between /ws/chat/ and the next /
    pattern = r"/ws/chat/(.+?)/"

    # Search for the pattern in the URL
    match = re.search(pattern, url)

    # If a match is found, return the captured segment
    if match:
        return match.group(1)

    # If no match is found, return None
    return None

async def get_user(token, username):
    try:
        knox_auth = await TokenAuthentication()
        user, auth_token = await knox_auth.authenticate_credentials(token.encode('utf-8'))
        chats = await User.objects.filter(chat_name=username)
        if not chats:
            return AnonymousUser()
        chat = chats.first()
        return user, chat
    except Exception:
        return AnonymousUser()
'''
class AuthKnoxMiddleware(AuthMiddleware):
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """
    async def __call__(self, scope, receive, send):
        if "headers" not in scope:
            raise ValueError(
                "CookieMiddleware was passed a scope that did not have a headers key "
                + "(make sure it is only passed HTTP or WebSocket connections)"
            )
        for name, value in scope.get("headers", []):
            if name == b"cookie":
                cookies = parse_cookie(value.decode("latin1"))
                break
        else:
            cookies = {}
        query_string = scope.get("query_string", None)
        if query_string:
            query_params = parse.parse_qs(query_string.decode("utf-8"))
            token = query_params.get("token", [None])[0]
            cookies = {"access": token}
        else:
            cookies = {}
        access = cookies.get("access")
        if access:
            path = scope.get("path")
            if not path:
                return self.inner(scope, receive, send)
            username = extract_chat_segment(path)
            if not username:
                return self.inner(scope, receive, send)
            __ = get_user(access, username)
            if isinstance(__, AnonymousUser):
                return self.inner(scope, receive, send)
            user, chat = __
            if not user:
                return self.inner(scope, receive, send)
            scope["user"] = user
            scope["chat"] = chat
        return self.inner(scope, receive, send)
'''

class AuthKnoxMiddleware(BaseMiddleware):
    """
    Middleware which populates scope["user"] from a Django session.
    Requires SessionMiddleware to function.
    """
    def populate_scope(self, scope):
        # Make sure we have a session
        print("\npopulate_scope\n")
        if "session" not in scope:
            raise ValueError(
                "AuthMiddleware cannot find session in scope. "
                "SessionMiddleware must be above it."
            )
        # Add it to the scope if it's not there already
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def resolve_scope(self, scope):
        print("\resolve_scope\n")
        scope["user"]._wrapped = await get_user(scope)

    async def __call__(self, scope, receive, send):
        print("\__call__\n")
        scope = dict(scope)
        # Scope injection/mutation per this middleware's needs.
        self.populate_scope(scope)
        # Grab the finalized/resolved scope
        await self.resolve_scope(scope)

        return await super().__call__(scope, receive, send)


def QueryAuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(AuthKnoxMiddleware(inner)))