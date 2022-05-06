import requests

url = "https://twinword-emotion-analysis-v1.p.rapidapi.com/analyze/"

querystring = {"text":"On the last night, with my trunk packed and my car sold to the grocer, I went over and looked at that huge incoherent failure of a house once more. On the white steps an obscene word, scrawled by some boy with a piece of brick, stood out clearly in the moonlight, and I erased it, drawing my shoe raspingly along the stone. Then I wandered down to the beach and sprawled out on the sand."}

headers = {
	"X-RapidAPI-Host": "twinword-emotion-analysis-v1.p.rapidapi.com",
	"X-RapidAPI-Key": "cff2be9e3amsha4efae17b30618ap1771fejsn8f8582860b97"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)