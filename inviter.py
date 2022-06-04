import requests, json, time, os

class GithubWrapper(object):
    """docstring for GithubWrapper."""

    def __init__(self, username, apikey):
        import requests, time
        self.s = requests.Session()
        self.s.headers.update( {"Accept":"application/vnd.github.v3+json"} )
        print((username, apikey))
        self.s.auth = (username, apikey)
    def fetch_collaborators(self):
        # x = self.s.get("https://httpbin.org/get")
        x = self.s.get("https://api.github.com/repos/Computer-Science-Club-OCC/Computer-Science-Club-OCC.github.io/collaborators")
        return x.json()
    def get_colab_list(self):
        resp = [];
        for i in self.fetch_collaborators():
            resp.append(i["login"])
        return resp;
    def add_collab(self, username, permission="push"):
        # x = self.s.put("https://httpbin.org/put", params={"permission":"push"})
        x = self.s.put(F"https://api.github.com/repos/Computer-Science-Club-OCC/Computer-Science-Club-OCC.github.io/collaborators/{username}", params={"permission":permission})
        time.sleep(5)
        return x

class Inviter(GithubWrapper):
    """Invites. people to the github"""

    def __init__(self, username, apikey):
        super().__init__(username, apikey)
    def get_json(self, url = "https://crow.port0.org/git/comradecrow/OCC-join/raw/branch/master/users.json"):
        x = requests.get(url)
        return x.json()

    def dump_json(self, data, filename = "dump.json"):
        with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, separators=(',', ': '))

    def send_invites(self):
        resp = self.get_colab_list()
        users = self.get_json()
        for i in users:
            if users[i] not in resp:
                print(users[i])
                x = self.s.put("https://httpbin.org/put", params={"permission":"push"})
                # x = self.add_collab(users[i])
                print(x)
                print(x.json())

    def send_invite_to(self, user):
        if user not in self.get_colab_list():
            print(user)
            # x = self.add_collab(user)
            x = self.s.put("https://httpbin.org/put", params={"permission":"push"})
            print(x)
            print(x.json())




if __name__ == "__main__":
    if os.name == "nt":
        from dotenv import load_dotenv
        load_dotenv()
    TOKEN = os.getenv('TOKEN')
    username = os.getenv('user')
    apikey = os.getenv('apikey')
    I = Inviter(username, apikey)
    print(I.get_json())
    I.send_invites()
    I.dump_json(I.fetch_collaborators())