from twitter import *
import json
import urllib2
from pprint import pprint

import private as private

terms = ['Altcoin','Angel','App','ApplicationDevelopment','Bitcoin','Bitfinex','Blockchain','BlockchainSecurity','Boulder','BTC','Build','Builder','BuildTheFuture','Business','ChangeTheWorld','Code','Coinbase','Collaboration','CollaborationBetweenCreativeMinds','Colorado','ColoradoSprings','Community','ComputerProgramming','Consensus','ContractDevelopment','Create','Crypto','Crypto101','CryptoCurrency','CryptoGovenance','CryptoKitties','CryptoMiner','CryptoMining','CryptoTrader','CryptoTrading','DAPP','Decentralization','DecentralizedSystems','Demonetization','Denver','Dev','Developer','DigitalCurrency','Disrupt','Engineer','Enthusiast','Entrepreneur','ETH','ETHCommons','ETHDenver','Ethereum','ETHGlobal','ExchangeVolume','Fintech','FortCollins','Free','FreeForHackers','FrontRange','Funds','Future','FutureTech','GameChanger','Geek','GoEthereum','Hack','Hackathon','Hacker','HardwareWallet','HyperLedger','ICO','Internet','InternetOfThings','Investments','Investor','Javascript','KnowledgeSharing','Leader','Litecoin','Maker','Micropayments','Mining','Moonshot','Nerd','NewTechnology','NodeJs','Open','OpenSource','Programmer','Programming','Protocol','Python','RubyOnRails','SmartContracts','SoftwareDevelopment','Solidity','Startup','StartupBusinesses','Superdao','Team','Tech','Technology','Thought','token','Tokenize','Tokens','Tools','Trader','VirtualCurrency','Wallet','Web3','WomenInBlockchain','WomenInTech','WomensNetworking']

def containsTerm(string):
    for term in terms:
        if(term.lower() in string.lower()):
            return True
    return False

twitter = Twitter(
    auth=OAuth(
        private.twitterAuth['token'],
        private.twitterAuth['token_secret'],
        private.twitterAuth['consumer_key'],
        private.twitterAuth['consumer_secret']
        )
    )



username = 'coloblockchain'

query = twitter.friends.ids(screen_name = username)

print "found %d friends" % (len(query["ids"]))

for n in range(0, len(query["ids"]), 100):
	ids = query["ids"][n:n+100]

	subquery = twitter.users.lookup(user_id = ids)

	for u in subquery:
		print "%s~%s~%s~%s~%s~%s~%s~%s" % (u["name"],'https://twitter.com/' + u["screen_name"], u["location"], u["followers_count"], u["friends_count"], u["listed_count"], u["description"], containsTerm(u["description"]))
