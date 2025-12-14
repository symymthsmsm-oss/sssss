from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio, random

# ضع هنا StringSession الخاص بك
string_session = "1BVtsOIIBu5lpiEEL2sV3n_3AMaSlBQz6y9tUVOIlaal7AODoNZl6xzeLkNYMCMlMa1ogt7HkQW7VPq5c0cunvyKxqal2glm89RTNVx7pz027z1b-9YbtZ_UGREnyWWgN2lawjlh4-FcfHnxAn2qEZyJKCeh9iyuRnheE7R3IerSrURKw-ZO6iPjvrjpj2F-73IdBUU34hrYQkEH22F_LTBLFinC0mBgLLDaghK4Pasawecz3MoY4JPa9Sb2c7og51K8G5qoDEjiPjk1s-EQ93V9YWv4Jy16rZHbucssA0au9DinUdIpAWM_j65lv_Focxk4Rrk9XsHktHk0JFf7ppYGXoq8RpKw="

api_id = 32819440
api_hash = "b522a1acd090143144662c95f3e7b927"

client = TelegramClient(StringSession(string_session), api_id, api_hash)

messages_list = [
    "يا ابن المنيوكه ياديوث لحجي يا ابن الشرموطه يعني كس ام امك",
"تعال كس ام امك يعني تعال  يا ابن الشرموطه",
"يا ابن المومسه يا ابن القحبه يا ابن الشرموطه يا مديث كس ام امك",
"يا ابن الشرموطه يا ابن المتريثه يا ابن المعرسه",
"يا ابن الشرموطه ي ورع القحبه",
"يا ابن المعرسه",
"كس ام امك يا ابن المنيوكه كس اختك يا ابن العاهره عق يا ابن القحبه",
"كس اختك يا لحجي يا واطي يا ابن الشرموطه",
"يا ابن المعرسه يا ابن الشرموطه يا ابن الشرموطه يا ابن الشرموطه يا ابن المعرسه",
"يا ابن الضايعه يا اخو المنيوكه ي ابن الزق",
"يا ابن الحرام ي مسكين ي ابن الزنا",
"ي ابن المتريثه",
"يا مسكين يا ابن العاهره",
"يا ابن المعرسه كس ام امك",
"عزيزي العميل يرجى تزويدنا بتفاصيل طيز امك🧕🏿⭕️",]
last_messages = {}
active_loops = {}
reply_speed = 0.01

start_word = "كس امك"
stop_word = "يا ورع القحبه"
kill_word = "كس اختك"
allowed_controller_ids = [463233975,6533022249, 7509073453]

@client.on(events.NewMessage)
async def handler(event):
    global reply_speed
    try:
        sender = await event.get_sender()
        if not sender: return
        message = (event.raw_text or "").strip().lower()

        if sender.id in allowed_controller_ids:
            if message == kill_word:
                last_messages.clear()
                for task in active_loops.values():
                    if not task.done(): task.cancel()
                active_loops.clear()
                return

            if message.startswith("تغيير سرعة"):
                try:
                    new_speed = float(message.replace("تغيير سرعة","").strip())
                    reply_speed = max(0.001,new_speed)
                    await event.reply(f" تم تغيير السرعة إلى {reply_speed}")
                except:
                    await event.reply("❌ مثال: تغيير سرعة 0.01")
                return

            if message == start_word:
                reply_to = await event.get_reply_message()
                if not reply_to: return
                user = await reply_to.get_sender()
                if not user: return
                last_messages[user.id] = reply_to
                if user.id not in active_loops or active_loops[user.id].done():
                    active_loops[user.id] = asyncio.create_task(reply_loop(user.id))
                return

            if message == stop_word:
                reply_to = await event.get_reply_message()
                if not reply_to: return
                user = await reply_to.get_sender()
                if not user: return
                last_messages.pop(user.id,None)
                return

        if sender.id in last_messages:
            last_messages[sender.id] = event
    except:
        pass

async def reply_loop(user_id):
    try:
        sent_messages = set()
        while user_id in last_messages:
            event = last_messages[user_id]
            available = [m for m in messages_list if m not in sent_messages]
            if not available:
                sent_messages.clear()
                available = messages_list
            response = random.choice(available)
            sent_messages.add(response)
            try:
                await event.reply(response)
            except: pass
            await asyncio.sleep(reply_speed)
    except asyncio.CancelledError: pass
    except: pass

with client:
    client.run_until_disconnected()