import sys
import urllib2
import json
from StringIO import StringIO
import base64
import getpass

#==== globals =======
username = ""
password = ""
dst_url = ""
server = "api.github.com"
issues_filename = ""
milestones_filename = ""
labels_filename = ""
#==== end of globals ===

def set_filenames(string):
	#issues
	global issues_filename
	issues_filename = "%s_issues.json" % string
	
	#milestones
	global milestones_filename
	milestones_filename = "%s_milestones.json" % string
	
	#labels
	global labels_filename
	labels_filename = "%s_labels.json" % string

def get_milestones():
	f = open(milestones_filename)
	result = f.read()
	milestones = json.load(StringIO(result))
	f.close()
	return milestones

def get_labels():
	f = open(labels_filename)
	result = f.read()
	labels = json.load(StringIO(result))
	f.close()
	return labels

def get_issues():
	f = open(issues_filename)
	result = f.read()
	issues = json.load(StringIO(result))
	f.close()
	return issues

def get_comments_on_issue(issue):
	if issue.has_key("comments") \
	  and issue["comments"] is not None \
	  and issue["comments"] != 0:
		response = urllib2.urlopen("%s/comments" % issue["url"])
		result = response.read()
		comments = json.load(StringIO(result))
		return comments
	else :
		return []

def import_milestones(milestones):
	for source in milestones:
		dest = json.dumps({
			"title": source["title"],
			"state": "open",
			"description": source["description"],
			"due_on": source["due_on"]})

		req = urllib2.Request("%s/milestones" % dst_url, dest)
		req.add_header("Authorization", "Basic " + base64.urlsafe_b64encode("%s:%s" % (username, password)))
		req.add_header("Content-Type", "application/json")
		req.add_header("Accept", "application/json")
		
		try:
			res = urllib2.urlopen(req)
			data = res.read()
			res_milestone = json.load(StringIO(data))
			print "Successfully created milestone %s" % res_milestone["title"]
		except urllib2.HTTPError as e:
			print "Could not create milestone %s" % source["title"]
			print e.read()

def import_labels(labels):
	for source in labels:
		dest = json.dumps({
			"name": source["name"],
			"color": source["color"]
		})

		req = urllib2.Request("%s/labels" % dst_url, dest)
		req.add_header("Authorization", "Basic " + base64.urlsafe_b64encode("%s:%s" % (username, password)))
		req.add_header("Content-Type", "application/json")
		req.add_header("Accept", "application/json")
		
		try:
			res = urllib2.urlopen(req)
			data = res.read()
			res_label = json.load(StringIO(data))
			print "Successfully created label %s" % res_label["name"]
		except urllib2.HTTPError as e:
			print "Could not create label %s" % source["name"]
			print e.read()
		

def get_milestones_from_repo(url):
	response = urllib2.urlopen("%s/milestones?state=open" % url)
	result = response.read()
	milestones = json.load(StringIO(result))
	return milestones
		
def get_labels_from_repo(url):
	response = urllib2.urlopen("%s/labels" % url)
	result = response.read()
	labels = json.load(StringIO(result))
	return labels

def import_issues(issues, dst_milestones, dst_labels):

	for source in issues:
		
		labels = []
		if source.has_key("labels"):
			for src_label in source["labels"]:
				name = src_label["name"]
				for dst_label in dst_labels:
					if dst_label["name"] == name:
						labels.append(name)
						break
	

		milestone = None
		if source.has_key("milestone") and source["milestone"] is not None:
			title = source["milestone"]["title"]
			for dst_milestone in dst_milestones:
				if dst_milestone["title"] == title:
					milestone = dst_milestone["number"]
					break

		assignee = None

		if source.has_key("assignee") and source["assignee"] is not None:
			assignee = source["assignee"]["login"]

		body = None
		if source.has_key("body") and source["body"] is not None:
			body = source["body"]

		dest = json.dumps({
			"title": source["title"],
		    "body": body,
		    "assignee": assignee,
		    "milestone": milestone,
		    "labels": labels
		})

		comments = get_comments_on_issue(source)
		#todo: insert logic on comments if needed
		req = urllib2.Request("%s/issues" % dst_url, dest)
		req.add_header("Authorization", "Basic " + base64.urlsafe_b64encode("%s:%s" % (username, password)))
		req.add_header("Content-Type", "application/json")
		req.add_header("Accept", "application/json")
		res = urllib2.urlopen(req)

		data = res.read()
		res_issue = json.load(StringIO(data))
		print "Successfully created issue %s" % res_issue["title"]

def main():
	
	#get the partial file name from the first argument
	partial = sys.argv[1]
	set_filenames(partial)
	
	#get the username from the second arg
	global username
	username = sys.argv[2]
	
	#get the destination repository from the third arg
	dst_repo = sys.argv[3]
	
	#set the global destination url
	global dst_url
	dst_url = "https://%s/repos/%s" % (server, dst_repo)
	
	#prompt for password
	global password
	password = getpass.getpass()
	
	#Need to get labels and milestones files from github api
	
    #get milestones and labels to import
	milestones = get_milestones()
	labels = get_labels()
	
	#import milestones and labels
	import_milestones(milestones)
	import_labels(labels)
		
	#get imported milestones and labels
	milestones = get_milestones_from_repo(dst_url)
	labels = get_labels_from_repo(dst_url)

	#process issues
	issues = get_issues()
	import_issues(issues, milestones, labels)


if __name__ == '__main__':
	main()