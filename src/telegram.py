import requests
from dotenv import dotenv_values


def send_message(message : str) -> dict:
	config = dotenv_values(".env")
	bot_token, chat_id = config["BOT_TOKEN"], config["CHAT_ID"]
	data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
	url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
	response = requests.post(url, data=data)

	return response.json()


def send_photo(image_path : str, bot_token : str, chat_id : str, image_caption="") -> dict:
    data = {"chat_id": chat_id, "caption": image_caption}
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    with open(image_path, "rb") as image_file:
        ret = requests.post(url, data=data, files={"photo": image_file})
		
    return ret.json()
