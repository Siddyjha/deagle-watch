import requests
import os
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
BAN_BASE_URL = "http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?"
VANITY_BASE_URL = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?"
USER_INFO_BASE_URL = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?"
ID_START_INDEX = 36


class Service:

	@staticmethod
	def isValidAccount(steam_id):
		
		try: 
			steam_id = int(steam_id)
			url = USER_INFO_BASE_URL + f"key={STEAM_API_KEY}&steamids={steam_id}"
			response = requests.get(url)

			if response.status_code != 200:
				return False, None

			if not response.json()["response"]["players"]:
				return False, None

			return True, response.json().get("response").get("players")[0].get("steamid")

		except:
			vanity_url = steam_id
			url = VANITY_BASE_URL + f"key={STEAM_API_KEY}&vanityurl={vanity_url}"

			response = requests.get(url)

			if response.status_code != 200:
				return False, None

			if response.json()["response"]["success"] != 1:
				return False, None

			return True, response.json().get("response").get("steamid")

	@staticmethod
	def checkBan(steam_id):
		ban_flag = False
		
		# get profile details from steam api
		url = BAN_BASE_URL + f"key={STEAM_API_KEY}&steamids={steam_id}"
		response = requests.get(url)
		response = response.json()
		response = response.get("players")[0]
		
		# possible bans
		community_ban = response.get("CommunityBanned")
		vac_ban = response.get("VACBanned")
		game_ban = response.get("NumberOfGameBans")
		economy_ban = response.get("EconomyBan")

		if community_ban == True or vac_ban == True or game_ban > 0 or economy_ban != 'none':
			ban_flag = True
			response_string = """This account has been banned!
			VAC: {}
			Game Ban: {} 
			Community Ban: {} 
			Economy Ban: {}
			ID:  https://steamcommunity.com/profiles/{}
			""".format(vac_ban, game_ban, community_ban, economy_ban, steam_id)

		else:
			response_string = "No ban detected"
		
		return ban_flag, response_string

	@staticmethod
	def checkAllBans(repository):
		collection = repository.collection
		accounts = collection.find()
		ban_list = ""

		for account in accounts:
			steam_id = account["steam_id"]
			ban_flag, response = Service.checkBan(steam_id)

			if ban_flag:
				repository.removeOne(steam_id)
				ban_list += "\n" + response

		return ban_list

