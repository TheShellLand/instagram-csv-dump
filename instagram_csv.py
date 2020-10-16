import json
import os
from dateutil.parser import parse


class User:
    def __init__(self, user):
        self.user = user
        self.followed = ''
        self.blocked = ''

    def __str__(self):
        return f'{self.user}'

    def __eq__(self, other):
        return self.user == other.user


class InstagramConnections:
    """connections.json"""

    def __init__(self, folder: str, file: str = 'connections.json'):
        self._folder = folder
        self._filename = file
        self._file = os.path.join(folder, file)
        self._json = json.loads(open(self._file, 'r').read()) or ''

        self._blocked_users = self._json['blocked_users'] or {}
        self._followers = self._json['followers'] or {}

        self.users = []
        self.users.extend([User(x) for x in self._blocked_users.keys() if User(x) not in self.users])
        self.users.extend([User(x) for x in self._followers.keys() if User(x) not in self.users])

        count = 0
        for user in self.users:
            count += 1
            print(f'{count}/{len(self.users)} ({count / len(self.users) * 100:.0f}%) {user}')

            for blocked in self._blocked_users.keys():
                if user == User(blocked):
                    user.blocked = self._blocked_users.get(blocked)

            for follower in self._followers.keys():
                if user == User(follower):
                    user.followed = self._followers.get(follower)

    def __str__(self):
        return f'followers: {len(self._followers)}, blocked_users: {len(self._blocked_users)}'

    def __eq__(self, other):
        return self.users == other.users

    def csv(self):
        """
        account, started_following, date_blocked
        """
        header = f'account, started_following, date_blocked\n'
        filename = f'{os.path.splitext(self._filename)[0]}.csv'
        with open(filename, 'w') as f:
            f.write(header)

            for user in self.users:
                line = f'{user.user}, {user.followed}, {user.blocked}\n'
                f.write(line)

        print(f'Wrote {filename} ({os.stat(filename).st_size / 1024:.2f} Kb)')


class InstagramAccount:
    """each folder is an account"""

    def __init__(self, account: str):
        self._folder = account

        self.account = account
        self.connections = InstagramConnections(self._folder)

    def __str__(self):
        return f'{self.account}'

    def __eq__(self, other):
        self.account == other.account

    def export_connections(self):
        self.connections.csv()


def main():
    accounts = [InstagramAccount(x) for x in os.listdir() if os.path.isdir(x) and x[0] != '.']
    export = [x.export_connections() for x in accounts]
    print()


if __name__ == "__main__":
    main()
