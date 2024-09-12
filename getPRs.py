import requests

# GET method
resp = requests.get("https://api.github.com/repos/kubernetes/kubernetes/pulls")

# .json() -> convert JSON to Dictionary
# .status_code -> HTTP status

# output = json.loads(response.text)
# convert josn data to Dictionary

complete_detail = resp.json()  # print(complete_detail[0])

# Print list of users who made PRs
for i in range(len(complete_detail)):
    print(complete_detail[i]["user"]["login"])


#No of PRs User has opened
