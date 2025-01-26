import discord
from pinata_python.pinning import Pinning
import os
from dotenv import load_dotenv
from transaction import Transaction
global cid

load_dotenv()
# Update the file location to the location of project (to access images folder)
os.chdir(r"/path/to/project")

def get_mint_number():
    if os.path.exists("MINT_COUNTER_FILE.txt"):
        with open("MINT_COUNTER_FILE.txt", 'r') as f:
            return int(f.read().strip())
    return 1

def increment_mint_number():
    mint_number = get_mint_number()
    with open("MINT_COUNTER_FILE.txt", 'w') as f:
        f.write(str(mint_number + 1))
    return mint_number

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

pinata_api_key = 'a449087e51ae803cf3aa'
pinata_api_secret = os.getenv("PINATA_SCT")

pinata = Pinning(PINATA_API_KEY=pinata_api_key,
                 PINATA_API_SECRET=pinata_api_secret)


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.attachments:
    for attachment in message.attachments:
      if attachment.content_type.startswith('image/'):
        global IMAGE_CID
        try:
          await attachment.save(f"./images/{attachment.filename}")
          await message.channel.send(
              f"Image saved successfully!")
          your_filepath = f'./images/{attachment.filename}'

          response = pinata.pin_file_to_ipfs(your_filepath)
          cid = response['IpfsHash']
          global image_cid
          image_cid = f"https://ipfs.io/ipfs/{cid}"

          increment_mint_number()
          new_token = get_mint_number()

          metadata = {
            "name": f"#{new_token}",
            "description": "This is an NFT minted via Discord Bot.",
            "image": image_cid,
            "attributes": [
                {
                    "trait_type": "Minted By",
                    "value": "User"
                }
            ]
          }
          responseMeta = pinata.pin_json_to_ipfs(metadata)
          meta_cid = responseMeta['IpfsHash']

          #await message.channel.send("Successfully pinned file to IPFS.")
          with open('name.txt', 'w') as f:
            f.write(your_filepath)
          await message.channel.send("Your image is ready to be minted!")
          await message.channel.send("Be paitent. As this process will take 1-2 minutes.")

          tx_receipt , tx_hash = Transaction(f"https://gateway.pinata.cloud/ipfs/{meta_cid}")

          await message.channel.send("NFT minted successfully!")

          await message.channel.send(f"transaction link: https://sepolia.etherscan.io/tx/0x{tx_hash}")
          await message.channel.send(f"nft link: https://testnets.opensea.io/assets/sepolia/0xb5bfee21bb057ddcf435707d7f99fe2185d952ad/{new_token -1}")

        except Exception as e:
          await message.channel.send(f"{e} \n If you face timeout problem visit this link below after few minutes \n https://testnets.opensea.io/assets/sepolia/0xb5bfee21bb057ddcf435707d7f99fe2185d952ad/{new_token -1}")
        break


client.run(os.getenv("BOT_TOKEN"))
