from shared.application.services.commands.command import Command


class AuthUser(Command):

    def __call__(self, auth, request, username: str, password: str):
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
