# Lazy-NFT-Minter

A Discord bot that automatically converts every image it receives into an NFT. This bot simplifies the NFT creation process by handling everything from receiving an image to minting it as an NFT on the Sepolia testnet.

---

## **How It Works**

1. **Receive Image**:

   - The bot listens for image uploads in Discord channels it has access to.
   - Once an image is received, it is saved locally.

2. **Pin to IPFS**:

   - The image is pinned to Pinata, and a CID (Content Identifier) is obtained.

3. **Generate Metadata**:

   - The image CID is used to create metadata in JSON format.
   - This metadata is also pinned to Pinata, and its CID is obtained.

4. **Mint NFT**:

   - The metadata CID is passed to a smart contract deployed on the Sepolia testnet.
   - The smart contract mints the NFT using the metadata CID.

---

## **Project Details**

### **Smart Contract**

- The smart contract used for minting is already deployed on the Sepolia testnet.
- **Contract Address**: [0xb5bfee21bb057ddcf435707d7f99fe2185d952ad](https://sepolia.etherscan.io/address/0xb5bfee21bb057ddcf435707d7f99fe2185d952ad)
- A copy of the contract code is included in the project as `LazyMinter.sol`.

### **NFT Collection**

- **OpenSea Testnet Collection**: [Minter](https://testnets.opensea.io/collection/minter-33)

---

## **Setup and Installation**

### **Prerequisites**

1. Python 3.8+
2. Discord Developer Account
3. Pinata API Key

### **Environment Variables**

Create a `.env` file in the project directory and include the following:

```env
PINATA_API_KEY=your-pinata-api-key
PINATA_SECRET_KEY=your-pinata-api-secret
WALLET_ADDRESS=your-ethereum-wallet-address
WALLET_PRIVATE_KEY=your-ethereum-wallet-private-key
BOT_TOKEN=your-discord-bot-token
```

### **Installation**

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/Lazy-NFT-Minter.git
   cd Lazy-NFT-Minter
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the bot:

   ```bash
   python main.py
   ```

---

## **Usage**

1. Add the bot to your Discord server using the following link:
   [Invite Link](https://discord.com/oauth2/authorize?client_id=1324682806718107721)

2. Send an image in a channel where the bot is active.

   - The bot will save the image, pin it to IPFS, and mint it as an NFT.

3. View the minted NFT on OpenSea Testnet under the [Minter Collection](https://testnets.opensea.io/collection/minter-33).

---

## **Files and Structure**

```
Lazy-NFT-Minter/
├── main.py                # Main bot script
├── transaction.py         # Handles blockchain transactions
├── abi.txt                # Contract ABI for interactions
├── MINT_COUNTER_FILE.txt  # Tracks minting count
├── requirements.txt       # All the modules used in the project
├── .env                   # Environment variables (excluded from the repository)
├── LazyMinter.sol         # Smart contract source code
└── images/                # Directory to store uploaded images
```
