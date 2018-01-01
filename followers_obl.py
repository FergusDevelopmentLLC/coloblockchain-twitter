from twitter import *
import json
import urllib2
from pprint import pprint

import private as private

def containsTerm(string):

    for term in terms:
        if(term.lower() + ' ' in string.lower()):
            return True

    for term in terms:
        if('#' + term.lower() + ' ' in string.lower()):
            return True

    return False


def clean(value):
    return value.replace('|','').replace('\n','').replace('\r','').rstrip('\r\n')


twitter = Twitter(
    auth=OAuth(
        private.twitterAuth['token'],
        private.twitterAuth['token_secret'],
        private.twitterAuth['consumer_key'],
        private.twitterAuth['consumer_secret']
        )
    )

terms = ['Altcoin','Angel','App','ApplicationDevelopment','Bitcoin','Bitfinex','Blockchain','BlockchainSecurity','Boulder','BTC','Build','Builder','BuildTheFuture','Business','ChangeTheWorld','Code','Coinbase','Collaboration','CollaborationBetweenCreativeMinds','Colorado','ColoradoSprings','Community','ComputerProgramming','Consensus','ContractDevelopment','Create','Crypto','Crypto101','CryptoCurrency','CryptoGovenance','CryptoKitties','CryptoMiner','CryptoMining','CryptoTrader','CryptoTrading','DAPP','Decentralization','DecentralizedSystems','Demonetization','Denver','Dev','Developer','DigitalCurrency','Disrupt','Engineer','Enthusiast','Entrepreneur','ETH','ETHCommons','ETHDenver','Ethereum','ETHGlobal','ExchangeVolume','Fintech','FortCollins','Free','FreeForHackers','FrontRange','Funds','Future','FutureTech','GameChanger','Geek','GoEthereum','Hack','Hackathon','Hacker','HardwareWallet','HyperLedger','ICO','Internet','InternetOfThings','Investments','Investor','Javascript','KnowledgeSharing','Leader','Litecoin','Maker','Micropayments','Mining','Moonshot','Nerd','NewTechnology','NodeJs','Open','OpenSource','Programmer','Programming','Protocol','Python','RubyOnRails','SmartContracts','SoftwareDevelopment','Solidity','Startup','StartupBusinesses','Superdao','Team','Tech','Technology','Thought','token','Tokenize','Tokens','Tools','Trader','VirtualCurrency','Wallet','Web3','WomenInBlockchain','WomenInTech','WomensNetworking']

screen_names = [
# 'rabbyte'
# 'weareopolis'
# 'owocki'
# 'SashainDenver',
# 'MarkBeylin'
# 'hannahparsons'
#'DanielDougherty'
# 'michaelgreen06'
# 'coditch'
# 'RhysLindmark'
# 'cooperkernan'
'davecraige'
]

coloblockchain = twitter.followers.ids(screen_name = 'coloblockchain')

def isFollowedByCBC(user_id):
    if(user_id in coloblockchain["ids"]):
        return True
    return False

output = "<html><head><link href='tablesort.css' rel='stylesheet'><script src='tablesort.js'></script><script src='tablesort.number.js'></script></head><style>table, th, td { border: 1px solid black; border-collapse:collapse; font-family:'Arial, Helvetica, sans-serif' }</style><body><script async src='https://platform.twitter.com/widgets.js' charset='utf-8'></script><table id='data'><tr><th data-sort-method='none'>twitter</th><th>Source</th><th>Name</th><th>url</th><th>location</th><th>followers_count</th><th>friends_count</th><th>lists_count</th><th>description</th></tr>"
delim = "</td><td>"

for screen_name in screen_names:

    query = twitter.followers.ids(screen_name = screen_name)

    print "found %d followers" % (len(query["ids"]))

    for n in range(0, len(query["ids"]), 100):
    	ids = query["ids"][n:n+100]
    	subquery = twitter.users.lookup(user_id = ids)
    	for u in subquery:
            #line = '<tr><td>' + screen_name + delim + clean(u["name"]) + delim + 'https://twitter.com/' + clean(u["screen_name"]) + delim + clean(u["location"]) + delim + str(u["followers_count"]) + delim + str(u["friends_count"]) + delim + str(u["listed_count"]) + delim + clean(u["description"]) + delim + str(containsTerm(u["description"])) + '</td></tr>' + '\n'
            link = '<a href=\'https://twitter.com/' + clean(u["screen_name"]) + '?ref_src=twsrc%5Etfw\' class=\'twitter-follow-button\' data-show-count=\'false\'>Follow @' + clean(u["screen_name"]) + '</a>'
            line = '<tr><td>' + link + delim + screen_name + delim + clean(u["name"]) + delim + 'https://twitter.com/' + clean(u["screen_name"]) + delim + clean(u["location"]) + delim + str(u["followers_count"]) + delim + str(u["friends_count"]) + delim + str(u["listed_count"]) + delim + clean(u["description"]) + '</td></tr>' + '\n'
            print line
            if(containsTerm(u["description"]) and isFollowedByCBC(u["id"]) == False and int(u["followers_count"]) > 999):
                output = output + line


output = output + "</table></body>"
output = output + "<script>new Tablesort(document.getElementById('data'));</script>"
output = output + "</html>"
o = "output/" + screen_names[0] + ".html"
f = open(o,"w")
f.write(str(output.encode('utf-8')))
f.close
