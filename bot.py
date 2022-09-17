import os, asyncio, discord, json, datetime, requests
from inviter import Inviter
from discord.ext import commands
import git
from git import Repo
from requests.exceptions import ConnectTimeout

class gitwrapper(object):
    """docstring for gitwrapper."""

    def __init__(self):
        self.isup = False
        self.repo_path = "data"
        try:
            if requests.get("https://crow.port0.org/git", timeout=10).status_code == 200:
                self.isup = True
            else:
                print("git repository is down, starting in invite only mode")
        except ConnectTimeout:
            print("git repository is unreachable, starting in invite only mode")
        self.initgit()

    def print_repository(self, repo):
        print('Repo description: {}'.format(repo.description))
        print('Repo active branch is {}'.format(repo.active_branch))
        for remote in repo.remotes:
            print('Remote named "{}" with URL "{}"'.format(remote, remote.url))
        print('Last commit for repo is {}.'.format(str(repo.head.commit.hexsha)))

    def print_commit(self, commit):
        print('----')
        print(str(commit.hexsha))
        print("\"{}\" by {} ({})".format(commit.summary,
                                         commit.author.name,
                                         commit.author.email))
        print(str(commit.authored_datetime))
        print(str("count: {} and size: {}".format(commit.count(),
                                                  commit.size)))

    def initgit(self):
        if self.isup:
            if not os.path.isdir(self.repo_path): Repo.clone_from("https://crow.port0.org/git/comradecrow/OCC-join.git", self.repo_path)

            self.repo = Repo(self.repo_path)

            from git import Actor
            author = Actor("comradecrow", "comradecrow@vivaldi.net")

            self.origin = self.repo.remote()
            assert self.origin.exists()
            self.origin.pull()

            self.index = self.repo.index
            assert len(list(self.index.iter_blobs())) == len([o for o in self.repo.head.commit.tree.traverse() if o.type == 'blob'])

            if not self.repo.bare:
                print('Repo at {} successfully loaded.'.format(self.repo_path))
                self.print_repository(self.repo)
                # create list of commits then print some of them to stdout
                commits = list(self.repo.iter_commits('master'))[:5]
                for commit in commits:
                    self.print_commit(commit)
                    pass
            else:
                print('Could not load repository at {} :('.format(self.repo_path))

            data={};
            if not os.path.isfile("data/users.json"):
                with open("data/users.json", "x") as f:
                    f.write("{}")

            with open("data/users.json", "r", encoding='utf-8') as f:
                data = json.load(f)

    def make_commit(self):
        if self.isup:
            print({str(ctx.author): githubusrnme})
            e = datetime.datetime.now()
            assert self.origin.exists()
            self.origin.pull()
            data.update({str(ctx.author): githubusrnme})
            with open('data/users.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.index.add(['users.json'])
            self.index.commit(F"autocommit {e.strftime('%Y-%m-%d %H-%M-%S')}", author=author)
            self.origin.push()

if os.name == "nt":
    from dotenv import load_dotenv
    load_dotenv()
TOKEN = os.getenv('TOKEN')
username = os.getenv('user')
apikey = os.getenv('apikey')
I = Inviter(username, apikey)

G = gitwrapper()

description = '''Jhonathan M. Binns'''
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():
    print('BOT Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for guild in bot.guilds:
        print('\n\n'+
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')
    game = discord.Game("Terraria")
    await bot.change_presence(status=discord.Status.online, activity=game)

async def invite(username, id):
    x = I.send_invite_to(username)
    user = bot.get_user(id)
#     ———————————No switches?———————————
# ⠀⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗⢷⢽⢽⢽⣮⡷⡽⣜⣜⢮⢺⣜⢷⢽⢝⡽⣝
# ⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇
# ⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏⠀
# ⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁⠀⠀
# ⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂⠀⠀⠀⠀
# ⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# —————————————————————————————
    if x == -1: msg = "Something went wrong, ask @Comrade Crow#3095 or @JonTheLeprechaun#1793 for help"
    elif x == 2: msg = "You were already invited! You can click this link to access your invitation: https://github.com/Computer-Science-Club-OCC/Computer-Science-Club-OCC.github.io/invitations"
    else: msg = "You have been invited to the Computer Science Club Github repository!  You can click this link to access your invitation: https://github.com/Computer-Science-Club-OCC/Computer-Science-Club-OCC.github.io/invitations"
    await user.send(msg)

@bot.command()
async def join(ctx, *, githubusrnme):
    await invite(githubusrnme, ctx.author.id)
    await ctx.send('Sent an invite to: {} for {}'.format(githubusrnme, str(ctx.author)))
    await make_commit()

bot.run(TOKEN)
