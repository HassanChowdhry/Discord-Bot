import pandas as pd
import aiohttp
import json

async def getLeetStats(username):
    url = f"https://leetcode-stats-api.herokuapp.com/{username}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    json_data = json.loads(data)
                    return convert_to_dataframe(json_data=json_data)
                else:
                    print(f"Error: {response.status} - {response.reason}")
                    return None  # or raise an exception if appropriate
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # or raise an exception if appropriate
            

def convert_to_dataframe(json_data):
    try:
        df = pd.DataFrame({
            "Category": ["Total Solved", "Easy Solved", "Medium Solved", "Hard Solved",
                         "Acceptance Rate", "Ranking", "Contribution Points", "Reputation"],
            "Value": [json_data["totalSolved"], json_data["easySolved"],
                      json_data["mediumSolved"], json_data["hardSolved"],
                      json_data["acceptanceRate"], json_data["ranking"],
                      json_data["contributionPoints"], json_data["reputation"]]
        })

        # some cases zero only was returned
        if df["Value"].sum() == 0:
            return None 
        
        return df
    except KeyError as ke:
        print(f"KeyError: {ke} - Check if the expected keys are present in the JSON data.")
        return None
    except Exception as e:
        print(f"An error occurred during DataFrame creation: {e}")
        return None  

async def compareUsers(username1, username2):
    df_user1 = await getLeetStats(username1)
    df_user2 = await getLeetStats(username2)

    if df_user1 is None or df_user2 is None:
        # add proper handling later
        return None

    # new df for comparison
    df_comparison = pd.DataFrame({
        "Category": df_user1["Category"],
        f"{username1}": df_user1["Value"],
        f"{username2}": df_user2["Value"]
    })

    # Winner column based on the comparison
    df_comparison["Winner"] = df_comparison.apply(lambda row: determine_winner(row, username1, username2), axis=1)

    return df_comparison

def determine_winner(row, username1, username2):
    category = row["Category"]
    value1 = row[username1]
    value2 = row[username2]

    if category == "Ranking":
        return username1 if value1 < value2 else username2
    else:
        return username1 if value1 > value2 else username2