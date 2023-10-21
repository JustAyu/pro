import time
import asyncio
from EngineX12 import app
from saved_members import localDB
from pyrogram import filters
from pyrogram.errors import FloodWait, UserPrivacyRestricted
from pyrogram.enums import UserStatus
from config import OWNER_ID

offline = []
online = []
inactive = []



@app.on_message(filters.command("load") & filters.user(OWNER_ID))
async def load(client, message):
	online_babes = ["userstatus.recently", "userstatus.online"]
	offline_babes = ["userstatus.long_ago", "userstatus.last_month"]
	week = ["userstatus.last_week"]
	try:
		async for member in app.get_chat_members(scrape_from):
			user = await app.get_users(member)
			if (str(user.status)).lower() in offline_babes:
				offline.append(member.user.id)
			elif (str(user.status)).lower() in week:
				inactive.append(member.user.id)
			else:
				online.append(member.user.id)
		scraping_report = await message.reply_text(f"<b>{len(online_members)}</b> Online Members and {len(offline_loaded)} Members loaded ✅")
	except Exception as exc:
		return await message.reply_text(f"<b>ERROR ⚠️</b>:\n\n{exc}")

@app.on_message(filters.command("save") & filters.user(OWNER_ID))
async def savetofile(client, message):
	if len(offline) > 10:
		offf = open("offline.text" "w")
		offf.write(f"{offline}")
		offf.close()

	if len(online) > 10:
		offf = open("online.text" "w")
		offf.write(f"{online}")
		offf.close()

	if len(inactive) > 10:
		offf = open("inactive.text" "w")
		offf.write(f"{inactive}")
		offf.close()