import pandas as pd
import aiohttp
import json

async def getLeetStats(username):
    url = f"https://leetcode-stats-api.herokuapp.com/{username}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            json_data = json.loads(data)
            return convert_to_dataframe(json_data=json_data)
            

def convert_to_dataframe(json_data):
    df = pd.DataFrame({
        "Category": ["Total Solved", "Total Questions", "Easy Solved", "Total Easy",
                     "Medium Solved", "Total Medium", "Hard Solved", "Total Hard",
                     "Acceptance Rate", "Ranking", "Contribution Points", "Reputation"],
        "Value": [json_data["totalSolved"], json_data["totalQuestions"],
                  json_data["easySolved"], json_data["totalEasy"],
                  json_data["mediumSolved"], json_data["totalMedium"],
                  json_data["hardSolved"], json_data["totalHard"],
                  json_data["acceptanceRate"], json_data["ranking"],
                  json_data["contributionPoints"], json_data["reputation"]]
    })

    return df