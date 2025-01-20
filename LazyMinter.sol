// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity ^0.8.22;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {ERC721Enumerable} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import {ERC721Pausable} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Pausable.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract Minter is ERC721, ERC721Enumerable, ERC721Pausable, Ownable, ERC721URIStorage {
    uint256 private _nextTokenId;

    uint256 public MaxSupply = 2000;
    string public baseURI;
    bool public publicMintOpen = true;
    bool public allowlistMintOpen = true;
    mapping(address => bool) public allowlist;

    constructor(address initialOwner) ERC721("Minter", "MT") Ownable(initialOwner) {}

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    function editMintWindow(bool _publicMintOpen, bool _allowlistMintOpen) external onlyOwner {
        publicMintOpen = _publicMintOpen;
        allowlistMintOpen = _allowlistMintOpen;
    }

    function allowListMint(string memory _tokenURI) public payable {
        require(allowlistMintOpen, "Allow list mint is closed!");
        require(allowlist[msg.sender], "Not in Allow List");
        require(msg.value == 0.0001 ether, "Not enough balance");
        internalMint(_tokenURI);
    }

    function publicMint(string memory _tokenURI) public payable {
        require(publicMintOpen, "Public Mint is closed");
        require(msg.value == 0.01 ether, "Not enough balance");
        internalMint(_tokenURI);
    }

    function setBaseURI(string memory _newBaseURI) public onlyOwner {
        baseURI = _newBaseURI;
    }

    function internalMint(string memory _tokenURI) internal {
        require(totalSupply() < MaxSupply, "We sold Oout!");
        uint256 tokenId = _nextTokenId++;
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, _tokenURI);
    }

    function tokenURI(uint256 tokenId) public view virtual override(ERC721, ERC721URIStorage) returns (string memory) {
        string memory _tokenURI = super.tokenURI(tokenId);
        string memory base = _baseURI();

        // If there is no base URI, return the token URI.
        if (bytes(base).length == 0) {
            return _tokenURI;
        }

        // If there is a base URI, concatenate it with the token URI.
        return string(abi.encodePacked(base, _tokenURI));
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return baseURI;
    }

    // The following functions are overrides required by Solidity.
    function allowlisteditor(address[] calldata addresses) public onlyOwner {
        for (uint i = 0; i < addresses.length; i++) {
            allowlist[addresses[i]] = true;
        }
    }

    function withdraw(address _addr) external {
        uint balance = address(this).balance;
        payable(_addr).transfer(balance);
    }

    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721, ERC721Enumerable, ERC721Pausable)
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }

    function _increaseBalance(address account, uint128 value)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._increaseBalance(account, value);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}