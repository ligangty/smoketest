import requests
import json
import os

basepath = os.path.dirname(os.path.realpath(__file__))

def ok(text):
  return '\033[92m'+text+'\033[0m'

def fail(text):
  return '\033[91m'+text+'\033[0m'

def http_ok(status_code):
  return status_code>=200 and status_code<300

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
  2. Update each repo 1 time for description(Not done yet)
  3. Delete the 3 test repos
"""
def prepare(repos):
  for key in repos:
    repo_data = repos[key]    
    prepareCreate(repo_data)
    prepareUpdate(repo_data)
    prepareDelete(repo_data)

def prepareCreate(repo_data):
  (repo_key, repo_name, repo_type, package_type) = (repo_data["key"], repo_data["name"], repo_data["type"], repo_data["packageType"])
  url = 'http://localhost:8080/api/admin/stores/%s/%s/%s' % (package_type, repo_type, repo_name)
  headers = {'Content-type': 'application/json'}
  jsonstring = json.dumps(repo_data)
  print("Start creating %s" % repo_key)
  r = requests.put(url,headers=headers, data=jsonstring)
  assert http_ok(r.status_code), fail('%s creation failed. Status: %s, Error: %s' % (repo_key, r.status_code, r.reason))
  print('%s created successfully' % repo_key)

def prepareUpdate(repo_data):
  (repo_key, repo_name, repo_type, package_type) = (repo_data["key"], repo_data["name"], repo_data["type"], repo_data["packageType"])
  if(repo_data["description"] is None):
    repo_data["description"] = repo_key + " Updated"
  else:
    repo_data["description"] = repo_data["description"] + " Updated"
  url = 'http://localhost:8080/api/admin/stores/%s/%s/%s' % (package_type, repo_type, repo_name)
  headers = {'Content-type': 'application/json'}
  jsonstring = json.dumps(repo_data)
  print("Start updating %s" % repo_key)
  r = requests.put(url,headers=headers, data=jsonstring)
  assert http_ok(r.status_code), fail('%s updating failed. Status: %s, Error: %s' % (repo_key, r.status_code, r.reason))
  print('%s updated successfully' % repo_key)

def prepareDelete(repo_data):
  (repo_key, repo_name, repo_type, package_type) = (repo_data["key"], repo_data["name"], repo_data["type"], repo_data["packageType"])
  url = 'http://localhost:8080/api/admin/stores/%s/%s/%s' % (package_type, repo_type, repo_name)
  print("Start deleting %s" % repo_key)
  r = requests.delete(url)
  assert http_ok(r.status_code), fail('%s deleting failed. Status: %s, Error: %s' % (repo_key, r.status_code, r.reason))
  print('%s created successfully' % repo_key)

        
"""
Verify summary stats function, do these:
  1. Access rest api and get data back
  2. Verify if there are 3 entries
  3. Verify if the count for different status of each test repo is correct.
  4. Verify if the total count of each test repo is correct.
"""
def verifyStats():
  url = 'http://localhost:8082/api/rest/history/stores/summary/stats'
  headers = {'Content-type': 'application/json'}
  r = requests.get(url,headers=headers)
  assert http_ok(r.status_code), fail('Stats validation failed. Error: %s' % r.reason)
  print(ok("Summary stats REST api access validation passed!"))
  
  data = r.json()
  # 2.Verify if 3 entries in stats
  EXPECTED_ENTRY_COUNT = 3
  assert len(data)==EXPECTED_ENTRY_COUNT, "Stats should contains %s entries but %s entries" % (EXPECTED_ENTRY_COUNT, len(data))
  print(ok("Summary stats total entries count validation passed!"))

  # 2. Verify if 3 entries for test repos are there
  (test_remote, test_hosted, test_group)=(None, None, None)    
  for r in data:
    if (r["storeKey"]=="maven:hosted:htest"):
      test_hosted=r      
    if (r["storeKey"]=="maven:remote:rtest"):
      test_remote=r
    if (r["storeKey"]=="maven:group:gtest"):
      test_group=r
  (r_exist, h_exist, g_exist)=(test_remote is not None, test_hosted is not None, test_group is not None)
  assert r_exist and h_exist and g_exist, fail("Some repo not contained. Remote: %s, Hosted: %s, Group: %s" % (r_exist, h_exist, g_exist))
  print(ok("Summary stats each entry containing validation passed!"))

  # 3,4 verify count
  verifyCount(test_hosted)
  verifyCount(test_remote)
  verifyCount(test_group)

def verifyCount(repo_sum_stats):
  key = repo_sum_stats["storeKey"]
  (EXPECT_CREATED,EXPECT_UPDATED,EXPECT_DELETED)=(1,1,1)
  (creates, updates, deletes) = (repo_sum_stats["creates"], repo_sum_stats["updates"], repo_sum_stats["deletes"])
  assert creates == EXPECT_CREATED, fail("%s summary stats create count not correct, expect: %s, actual: %s" % (key, EXPECT_CREATED, creates))
  assert updates == EXPECT_UPDATED, fail("%s summary stats update count not correct, expect: %s, actual: %s" % (key, EXPECT_UPDATED, updates))
  assert deletes == EXPECT_DELETED, fail("%s summary stats delete count not correct, expect: %s, actual: %s" % (key, EXPECT_DELETED, deletes))
  TOTAL_COUNT = EXPECT_CREATED+EXPECT_UPDATED+EXPECT_DELETED
  total = creates+updates+deletes
  assert total == TOTAL_COUNT, fail("%s summary stats total count not correct, expect: %s, actual: %s" % (key, TOTAL_COUNT, total))
  print(ok("Repo summary stats validation for %s passed!" % key))

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
    if(http_ok(r.status_code)):
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
  if(http_ok(r.status_code)):
    data = r.json()       
    #TODO: verify if change event data contains enough information
  else:
    print('Validation failed for event %s, Error: %s' % (eventId, r.reason))


repos = collect_repos()

prepare(repos)
verifyStats()

