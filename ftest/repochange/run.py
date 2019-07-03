import requests
import json
import os

basepath = os.path.dirname(os.path.realpath(__file__))

def prepare():
  for base, dirs, files in os.walk(os.path.join(basepath, "repodef")):
    for fi in files:
      with open(os.path.join(base, fi), 'r') as f:
        repo_data = json.load(f)
        repo_key = repo_data["key"]
        repo_name = repo_data["name"]
        repo_type = repo_data["type"]
        package_type = repo_data["packageType"]
        url = 'http://localhost:8080/api/admin/stores/%s/%s/%s' % (package_type, repo_type, repo_name)
        headers = {'Content-type': 'application/json'}
        jsonstring = json.dumps(repo_data)
        print("Start creating %s" % repo_key)
        r = requests.put(url,headers=headers, data=jsonstring)
        if(r.status_code==200):
          print('%s created successfully' % repo_key)
          continue
        print('%s creation failed, Error: %s' % (repo_key, r.reason))
        

def verifyStats():
  url = 'http://localhost:8082/api/rest/history/stores/summary/stats'
  headers = {'Content-type': 'application/json'}
  r = requests.get(url,headers=headers)
  if(r.status_code==200):
    data = r.json()
    entry_count = 6
    assert len(data)==entry_count, "Stats should contains %s entries" % entry_count
    remote_contain=False
    hosted_contain=False
    group_contain=False
    for r in data:
      if (r["storeKey"]=="maven:hosted:htest"):
        hosted_contain=True
      if (r["storeKey"]=="maven:remote:rtest"):
        remote_contain=True
      if (r["storeKey"]=="maven:group:gtest"):
        group_contain=True
    assert remote_contain and hosted_contain and group_contain, "Some repo not contained. Remote: %s, Hosted: %s, Group: %s" % (remote_contain, hosted_contain, group_contain)
  else:
    print('Stats validation failed. Error: %s' % r.reason)

def verifySummaries():
  for base, dirs, files in os.walk(os.path.join(basepath, "repodef")):
    for fi in files:
      with open(os.path.join(base, fi), 'r') as f:
        repo_data = json.load(f)
        repo_key = repo_data["key"]
        repo_name = repo_data["name"]
        repo_type = repo_data["type"]
        package_type = repo_data["packageType"]
        url = 'http://localhost:8082/api/rest/history/stores/summary/by-store/%s/%s/%s' % (package_type, repo_type, repo_name)
        headers = {'Content-type': 'application/json'}
        jsonstring = json.dumps(repo_data)
        r = requests.get(url,headers=headers)
        if(r.status_code==200):
          data = r.json()          
          continue
        print('Validation failed for %s, Error: %s' % (repo_key, r.reason))
        
        

# prepare()
verifyStats()

