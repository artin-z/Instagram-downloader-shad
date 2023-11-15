from httpx import AsyncClient
from bs4 import BeautifulSoup
import asyncio

class Instagram_dl(object):
	def __init__(self):
		self.network = AsyncClient()
	
	async def getInformationByUrl(self, url: str):
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Accept': '*/*',
			'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; fa; 21091116AG Build/evergreen-user 12 SP1A.210812.016 V13.0.5.0.SGBMIXM) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.0.0 Mobile Safari/537.36',
			'Referer': 'https://saveig.app/en'
		}
		try:
			response = await self.network.post(
				url="https://v3.saveig.app/api/ajaxSearch",
				headers=headers,
				data={
					"q": url,
					"t": "media",
					"lang": "en"
				}
			)
			if response.status_code == 200:
				result = response.json().get("data", None)
				if isinstance(result, str):
					soup = BeautifulSoup(result, "html.parser")
					#for item in soup.find_all("ul", class_="download-box"):
					return dict(
							images = soup.find_all("img"),
							videos = soup.find_all("a")
						)
				else:
					return None
			else:
				return None
		except:
			return None
	
	async def getUrl(self, url: str):
		result = await self.getInformationByUrl(url)
		if isinstance(result, dict):
			images = []
			for image in result.get("images"):
				images.append(image["src"])
			
			videos = []
			for video in result.get("videos"):
				link = video["href"]
				if "https://download.ig" in link:
					videos.append(link)
			
			return dict(
				images = images,
				videos = videos
			)
		else:
			return None