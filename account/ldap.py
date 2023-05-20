from django.contrib.auth.backends import RemoteUserBackend

class MyRemoteUserBackend(RemoteUserBackend):
    def clean_username(self, username):
        """
        Perform any cleaning on the "username" prior to using it to get or
        create the user object.  Return the cleaned username.

        By default, return the username unchanged.
        """
        if '\\' in username:
            return username.split('\\')[1]
        return username