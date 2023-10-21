import time
import asyncio
from EngineX12 import app
from saved_members import localDB
from pyrogram import filters
from pyrogram.errors import FloodWait, UserPrivacyRestricted
from pyrogram.enums import UserStatus
from config import OWNER_ID

#----------------------------Importing---------------------------------#

offline_loaded = []
online_members = []
current_members = []

member_file = None

#--------------------------Local_Database------------------------------#



# Temprory Users Loaded To Temprory Memory
@app.on_message(filters.command("load") & filters.user(OWNER_ID))
async def load(client, message):
	if len(message.command) < 2:
		return await message.reply_text("You Forgotten To Give Scraping Group's Username. Try Again!")
	try:
		scrape_from = message.text.split(" ", maxsplit=1)[1]
	except IndexError:
		return await message.reply_text("Please Give Only Group's Username!")
	
	# Scrape report!
	scraping_report = await message.reply_text(f"Scraping <b>{scrape_from}</b> 🔄")
	
	online_babes = ["userstatus.recently", "userstatus.online"]
	offline_babes = ["userstatus.long_ago", "userstatus.last_month", "userstatus.last_week"]

	# Trying To Scrape
	try:
		async for member in app.get_chat_members(scrape_from):
			user = await app.get_users(member)
			if (str(user.status)).lower() in offline_babes:
				offline_loaded.append(member.user.id)
			else:
				online_members.append(member.user.id)
		scraping_report = await message.reply_text(f"<b>{len(online_members)}</b> Online Members and {len(offline_loaded)} Members loaded ✅")
	except Exception as exc:
		return await message.reply_text(f"<b>ERROR ⚠️</b>:\n\n{exc}")



"""# Scan members from/if a database file already exists
@app.on_message(filters.command("point") & filters.user(OWNER_ID))
async def scan(client, message):
	global member_file
	if "on" in message.text:
		try:
			member_file = True
			await message.reply_text(f"Members Pointed To LocalDB! ✅")
	else:
		try:
			member_file = True
			await message.reply_text(f"Members Pointing Off! ✅")
	except ModuleNotFoundError as ayush:
		return message.reply_text("You Have No User Database!\n\nBuy From @Life_Codes")
		print("VIP File Not Found!")"""





# Add members
@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def add(client, message):
	if "online" in message.text:
		if len(online_members) > 5:
			add_me = online_members
		else:
			add_me = localDB.online
	elif "inactive" in message.text:
		if len(offline_loaded) > 5:
			add_me = offline_loaded
		else:
			add_me = localDB.inactive
	else:
		if len(offline_loaded) > 5:
			add_me = offline_loaded
		else:
			add_me = localDB.offline
	
	if len(add_me) > 0:
		return await message.reply_text(f"please load members first or check the script's database!")
	else:
		await message.reply_text(f"{len(add_me)} members loaded ✅")

	already_present = []
	try:
		async for member in app.get_chat_members(message.chat.id):
			already_present.append(member.user.id)
		report = await message.reply_text(f"This group is scanned just for avoiding already added members ✅")
	except Exception as exc:
		return await message.reply_text(f"<b>ERROR ⚠️</b>:\n\n{exc}")
	added = 0
	try:
		for tgt in add_me:
			if tgt not in already_present:
				try:
					user = await app.get_users(tgt)
					await app.add_chat_members(message.chat.id, user.id)
					addedd += 1
					print(f"{added} Member Added!-----------✅")
				except FloodWait as ayush:
					await message.reply_text(f"Flood Error => {e.value} seconds! Paused For {e.value}")
					time.sleep(int(e.value))
				except Exception as err:
					continue
			else:
				print(f"{tgt} Already")
				continue
		await message.reply_text(f"Member Adding Completed ✅")
	except Exception as loml:
		print(loml)
		return await message.reply_text(f"<b>ERROR ⚠️</b>:\n\n{loml}")