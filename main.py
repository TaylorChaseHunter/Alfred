import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)

BOOKS = ["2021:", "Incognito", "Flowers for Algernon", "Mice of men", "1984",
         "Brave New World", "Fahrenheit 451", "Cold Mountain", "Slaughterhouse 5",
         "In Cold Blood", "Myth of Sisyphus", "Picture of Dorian Grey", "Outsiders",
         "Bury my Heart at Wounded Knee", "\n2022:", "Grapes of wrath", "Moby dick", "Swerve",
         "Cats cradle", "Cosmos", "Born to Run", "Farewell to Arms", "The Right Stuff",
         "The Hitchikers Guide to the Galaxy"]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    elif message.content.lower() == "hello alfred":
        await message.channel.send("Good morrow")

    elif message.content.lower() == "speak alfred":
        await message.channel.send("I live")

    elif message.content.lower() == "alfred, grab the books":
        await message.channel.send("Right away master.")
        response = "`" + "\n".join(BOOKS) + "`"
        await message.channel.send(response)

    elif message.content.lower() == "alfred, what is your favorite book?":
        await message.channel.send("I must say, slaugherhouse-5 is incredibly, but personally the truth and passion "
                                   "behind Myth of Sisyphus makes it unmatched to me.")

    elif message.content.lower() == "alfred, what is your least favorite book?":
        await message.channel.send("All books are good books my dear masters, but if I had to pick one that I did not"
                                   "enjoy as much as others, I'd sadly say Cold Mountain.")

    elif message.content.lower() == "alfred, list the constitution":
        dir_list = os.listdir('constitution')
        for file in dir_list:
            with open('constitution/' + file, 'r') as r:
                data = r.read()
                await message.channel.send(data)
            r.close()

    elif "alfred, list article" in message.content.lower():
        _, _, after_keyword = message.content.lower().partition("article")
        location = "constitution/article" + after_keyword.strip()
        with open(location) as r:
            data = r.read()
            await message.channel.send(data)
        r.close()

    elif message.content.lower() == "alfred, list the preamble":
        location = "constitution/Apreamble"
        with open(location) as r:
            data = r.read()
            await message.channel.send(data)
        r.close()

    elif message.content.lower() == "alfred, list the poem":
        location = "constitution/Apoem"
        with open(location) as r:
            data = r.read()
            await message.channel.send(data)
        r.close()

    elif message.content.lower() == "alfred, flip a coin":
        content = random.choice(["Heads", "Tails"])
        await message.channel.send(content)

    elif message.content.lower() == "thank you alfred" or message.content.lower() == "thanks alfred":
        responses = ["Twas no problem.",
                     "Isn't a worry masters.",
                     "I live to serve the hobos.",
                     "Please, it was my pleasure.",
                     "As always my dear friends."]
        response = random.choice(responses)
        await message.channel.send(response)

    elif "alfred" in message.content.lower():
        responses = ["I have no opinion on this matter.",
                     "I am busy making tea, what is it masters?",
                     "The hobos are an important group that I strive to serve.",
                     "I often think of myself as Ishmael as well.",
                     "Is one not just a rat in a maze? Maybe not, but it is worth the thought.",
                     "Is desertion a crime if it saves one's life? How can a man be blamed for such reasons?",
                     "The worst crime man can commit is not educating himself.",
                     "I defer to Grond.",
                     "I relate most to captain Ahab. Do we all not chase some White Whale? "
                     "What are we doing otherwise?",
                     "If life is meaningless, we must create the meaning. That is a great thing.",
                     "NFTs are a scam.",
                     "What would one give to live in a perfect society?",
                     "Is man just a mouse running along his wheel, simply awaiting death? Is this bad?",
                     "Something something war something something supreme court.",
                     "Not enough people know of Sandy Creek.",
                     "The power of the human brain is incalculable, yet we must try to number it.",
                     "Space is the final frontier, and we must find our way amongst the stars.",
                     "Only the very weak-minded refuse to be influenced by literature and poetry.",
                     "You talk when you cease to be at peace with your thoughts.",
                     "Every heart sings a song, incomplete, until another heart whispers back. "
                     "Those who wish to sing always find a song. At the touch of a lover, everyone becomes a poet."]
        response = random.choice(responses)
        await message.channel.send(response)

client.run(TOKEN)



