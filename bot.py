import os, asyncio, discord, json, datetime
from inviter import Inviter
from discord.ext import commands
import git
from git import Repo

def print_repository(repo):
    print('Repo description: {}'.format(repo.description))
    print('Repo active branch is {}'.format(repo.active_branch))
    for remote in repo.remotes:
        print('Remote named "{}" with URL "{}"'.format(remote, remote.url))
    print('Last commit for repo is {}.'.format(str(repo.head.commit.hexsha)))

def print_commit(commit):
    print('----')
    print(str(commit.hexsha))
    print("\"{}\" by {} ({})".format(commit.summary,
                                     commit.author.name,
                                     commit.author.email))
    print(str(commit.authored_datetime))
    print(str("count: {} and size: {}".format(commit.count(),
                                              commit.size)))

repo_path = "data"

if not os.path.isdir(repo_path): Repo.clone_from("https://crow.port0.org/git/comradecrow/OCC-join.git", repo_path)

repo = Repo(repo_path)

from git import Actor
author = Actor("comradecrow", "comradecrow@vivaldi.net")

origin = repo.remote()
assert origin.exists()
origin.pull()

index = repo.index
assert len(list(index.iter_blobs())) == len([o for o in repo.head.commit.tree.traverse() if o.type == 'blob'])

if not repo.bare:
    print('Repo at {} successfully loaded.'.format(repo_path))
    print_repository(repo)
    # create list of commits then print some of them to stdout
    commits = list(repo.iter_commits('master'))[:5]
    for commit in commits:
        print_commit(commit)
        pass
else:
    print('Could not load repository at {} :('.format(repo_path))

data={};
if not os.path.isfile("data/users.json"):
    with open("data/users.json", "x") as f:
        f.write("{}")

with open("data/users.json", "r", encoding='utf-8') as f:
    data = json.load(f)

if os.name == "nt":
    from dotenv import load_dotenv
    load_dotenv()
TOKEN = os.getenv('TOKEN')
username = os.getenv('user')
apikey = os.getenv('apikey')
I = Inviter(username, apikey)

description = '''Jhonathan M. Binns'''
intents = discord.Intents.default()
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
    I.send_invite_to(username)
    user = bot.get_user(id)
    await user.send("You have been invited to the Computer Science Club Github repository!  You can click this link to access your invitation: https://github.com/Computer-Science-Club-OCC/Computer-Science-Club-OCC.github.io/invitations")

@bot.command()
async def join(ctx, *, githubusrnme):
    print({str(ctx.author): githubusrnme})
    e = datetime.datetime.now()
    assert origin.exists()
    origin.pull()
    data.update({str(ctx.author): githubusrnme})
    with open('data/users.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    index.add(['users.json'])
    index.commit(F"autocommit {e.strftime('%Y-%m-%d %H-%M-%S')}", author=author)
    origin.push()
    invite(githubusrnme, ctx.author.id)
    await ctx.send('Sent an invite to: {} for {}'.format(githubusrnme, str(ctx.author)))

bot.run(TOKEN)
