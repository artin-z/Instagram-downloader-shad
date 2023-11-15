from shadpy import Client, Message, handlers, models
from asyncio import run, create_task
from instagram import Instagram_dl
import httpx
insta, httpx = (
	Instagram_dl(),
	httpx.AsyncClient()
)

async def private_handler(client: Client, message: Message):
	if isinstance(message.raw_text, str):
		text: str = message.raw_text
		object_guid = message.object_guid
		message_id = message.message_id
		
		if text.startswith("/d"):
			replace_text = text.strip().replace("/d ", "")
			if "instagra" in replace_text:
				msg = await message.reply("درحال دریافت اطلاعات . . .")
				response = await insta.getUrl(replace_text.replace("instagra", "instagram"))
				if isinstance(response, dict):
					print(response)
					await client.edit_message(
						object_guid=object_guid,
						message_id=msg.message_update.message_id,
						text="درحال دریافت و ارسال فایل . . ."
					)
					
					for image in response.get("images"):
						download = await httpx.get(image)
						await client.send_file(
							object_guid=object_guid,
							file=download.read(),
							file_name="insta.jpg",
							reply_to_message_id=message_id
						)
					
					for video in response.get("videos"):
						print(video)
						download = await httpx.get(video)
						await client.send_file(
							object_guid=object_guid,
							file=download.read(),
							file_name="insta.mp4",
							reply_to_message_id=message_id
						)
					
					await client.send_message(object_guid, "تمامی فایل های یافت شده به شما ارسال گردید.")
				else:
					await message.reply("خطا!")
			else:
				await message.reply("آدرس اینترنتی نامعتبر!")
	
async def main():
	async with Client(session="shadpy") as client:
		@client.on(handlers.MessageUpdates(models.is_private()))
		async def updates(message: Message):
			create_task(private_handler(client, message))
		await client.run_until_disconnected()

run(main())