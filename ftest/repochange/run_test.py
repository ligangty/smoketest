import requests
import json
import os

basepath = os.path.dirname(os.path.realpath(__file__))

def collect_repos():
  repos = {}
  for base, dirs, files in os.walk(os.path.join(basepath, "repodef")):
    for fi in files:
      with open(os.path.join(base, fi), 'r') as f:
        repo_data = json.load(f)
        repo_key = repo_data["key"]
        repos[repo_key] = repo_data
  return repos

"""
Preparation in indy side, will do these:
  1. Create 3 test repos, including each of hosted,remote and group
  2. Update each repo several times (Not done yet)
  3. Delete the 3 test repos (Not done yet)
"""
def prepare(repos):
  for key in repos:
    repo_data = repos[key]    
    (repo_name, repo_type, package_type) = (repo_data["name"], repo_data["type"], repo_data["packageType"])
    url = 'http://localhost:8080/api/admin/stores/%s/%s/%s' % (package_type, repo_type, repo_name)
    headers = {'Content-type': 'application/json'}
    jsonstring = json.dumps(repo_data)
    print("Start creating %s" % key)
    r = requests.put(url,headers=headers, data=jsonstring)
    if(r.status_code==200):
      print('%s created successfully' % key)
      continue
    print('%s creation failed, Error: %s' % (key, r.reason))
        
"""
Verify summary stats function, do these:
  1. Access rest api and get data back
  2. Verify if there are 6 entries(3 initial repo changes, and 3 from prepared test repo change)
  3. Verify if the count for different status of each test repo is correct.
  4. Verify if the total count of each test repo is correct.
"""
def verifyStats():
  url = 'http://localhost:8082/api/rest/history/stores/summary/stats'
  headers = {'Content-type': 'application/json'}
  r = requests.get(url,headers=headers)
  if(r.status_code==200):
    data = r.json()
    # 2.Verify if 6 entries in stats
    entry_count = 6
    assert len(data)==entry_count, "Stats should contains %s entries" % entry_count

    # 2. Verify if 3 entries for test repos are there
    (test_remote, test_hosted, test_group)=(None, None, None)    
    for r in data:
      if (r["storeKey"]=="maven:hosted:htest"):
        test_hosted=r["storeKey"]
      if (r["storeKey"]=="maven:remote:rtest"):
        test_remote=r["storeKey"]
      if (r["storeKey"]=="maven:group:gtest"):
        test_group=r["storeKey"]
    (r_exist, h_exist, g_exist)=(test_remote is not None, test_hosted is not None, test_group is not None)
    assert r_exist and h_exist and g_exist, "Some repo not contained. Remote: %s, Hosted: %s, Group: %s" % (r_exist, h_exist, g_exist)
  else:
    print('Stats validation failed. Error: %s' % r.reason)

"""
Verify change summary entrypoint for store. Do following:
  1. Access summary by store rest endpoint for one or more stores.
  2. Verify if the summary entries count is correct for the specified store.
"""
def verifySummaries(repos):
  for key in repos:
    repo_data = repos[key]
    (repo_name, repo_type, package_type) = (repo_data["name"], repo_data["type"], repo_data["packageType"])
    url = 'http://localhost:8082/api/rest/history/stores/summary/by-store/%s/%s/%s' % (package_type, repo_type, repo_name)
    headers = {'Content-type': 'application/json'}
    jsonstring = json.dumps(repo_data)
    r = requests.get(url,headers=headers)
    if(r.status_code==200):
      data = r.json()       
      #TODO: verify if summary entries count is correct
      continue
    else:
      print('Validation failed for %s, Error: %s' % (key, r.reason))


"""
Verify if single change event is correct. Do following:
  1. Access single change event by event id rest endpoint.
  2. Verify if the returned change event contains enough information.
"""
def verifyChangeEvent(eventId):
  url = 'http://localhost:8082/api/rest/history/stores/change/%s' % (eventId)
  headers = {'Content-type': 'application/json'}
  r = requests.get(url,headers=headers)
  if(r.status_code==200):
    data = r.json()       
    #TODO: verify if change event data contains enough information
  else:
    print('Validation failed for event %s, Error: %s' % (eventId, r.reason))


repos = collect_repos()

# prepare(repos)
verifyStats()

