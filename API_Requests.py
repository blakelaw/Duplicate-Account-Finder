import pandas as pd
import requests
import json
import time

ACCESS_TOKEN="ENTER YOUR ACCESS TOKEN"
PUBLIC_KEY = "K3u5lgAQktVbSANC7RNrm4Y4kysWofPibusjpwNSLtzno3gSa6i8dvesg7hgsEDi"
SECRET_KEY = "ENTER YOUR SECRET KEY"
FORUM= "predictit"
THREAD="6174959359"

first_request = "https://disqus.com/api/3.0/posts/list.json"+"?"+"access_token="+ACCESS_TOKEN+"&api_key="+PUBLIC_KEY+"&api_secret="+SECRET_KEY+"forum="+FORUM+"&thread="+THREAD+"&limit="+"100"
response_cursor = requests.get(first_request)
response_info_cursor = json.loads(response_cursor.text)

responses_df = pd.DataFrame(data=response_info_cursor["response"])

initial_cursor = response_info_cursor["cursor"]["next"]

min_til_reset = 60
remaining_request = 975
total_global_API_requests = 1000 - int(remaining_request)
target_global_API_requests_rate_per_second = (remaining_request/min_til_reset/60) - 0.1
print(target_global_API_requests_rate_per_second)
start_time = time.time()

cursor = str(initial_cursor)
pull_number = 0 #the number of full cycles and DF saved, each with 900 pages

num_cursors = 20000 # 500 * 100

target_google_drive_folder = "/content/drive/My Drive/Colab Notebooks/Disqus/rnom_data/"

while True:
  print("has been running for:")
  print("--- %s seconds ---" % (time.time() - start_time))

  print("now beginning work on pull: "+str(pull_number))

  print("now beginning work on cursor:")
  print(cursor)

  counter = 0

  responses_df  = pd.DataFrame()
  while counter < num_cursors:
    print("Requesting cursor:" + str(counter) + " of " + str(num_cursors) + " | " + str(round(counter/num_cursors*100,3))+"% done this frame")
    current_request = "https://disqus.com/api/3.0/posts/list.json"+"?"+"access_token="+ACCESS_TOKEN+"&api_key="+PUBLIC_KEY+"&api_secret="+SECRET_KEY+"forum="+FORUM+"&thread="+THREAD+"&limit="+"100"+"&cursor="+cursor
    response = requests.get(current_request)
    response = json.loads(response.text)
    total_global_API_requests += 1
    """
    print("api response: ")
    print(response["code"])
    """
    #print("Checking if key exists in JSON")
    if response["code"] == int(200) or response["code"] == int(0):
      cursor = response["cursor"]["next"]
      responses_df = responses_df.append(pd.DataFrame(data=response["response"]))
      counter += 1
    elif response["code"] == int(13):
      print("error" )
      print(response["code"])
      print(response["response"])
      print("waiting 61 seconds so as not to over burden API")
      time.sleep(61)
    elif response["code"] > int(299):
      print("error > 299")
      print(response["code"])
      print(response["response"])
      print("sleeping 30 sec")
      time.sleep(30)
    else:
      print("unknown error")

    seconds_run = int((time.time() - start_time))
    print("seconds run: "+str(seconds_run))
    print("total global API requests: " + str(total_global_API_requests))
    api_request_rate_per_second = total_global_API_requests / seconds_run
    print("total global API requests per second: " + str(api_request_rate_per_second))
    while api_request_rate_per_second > target_global_API_requests_rate_per_second:
      print("requesting api calls too fast! sleeping 5 sec")
      time.sleep(5)
      seconds_run = int((time.time() - start_time))
      api_request_rate_per_second = total_global_API_requests / seconds_run
      print("seconds run: "+str(seconds_run))
      print("total global API requests: " + str(total_global_API_requests))
      print("total global API requests per second: " + str(api_request_rate_per_second))

  print("last cursor: "+str(response["cursor"]["next"]))
  print("df shape: "+str(responses_df.shape))
  print("ready to save DF")
  print("has been running for:")
  print("--- %s seconds ---" % (time.time() - start_time))

  #target_filename = str("df_pull_number_"+str(pull_number)+"_cursorEND_"+str(cursor))
  target_filename = "RNomArchive2"
  responses_df.reset_index(inplace=True, drop=True)
  print("trying to save: " + str(target_filename))
  responses_df.to_feather(target_filename)
  print("saved!")
  print("has been running for:")
  print("--- %s seconds ---" % (time.time() - start_time))

  pull_number += 1

responses_df.reset_index(inplace=True, drop=True)
responses_df.to_feather("2020_Archive_Partial")

