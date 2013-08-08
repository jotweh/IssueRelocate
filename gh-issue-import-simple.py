import urllib2
import json
from StringIO import StringIO
import base64
import getpass

# copy one issue from one repo to another
#==== configurations ======
username = raw_input("username: ")
password = getpass.getpass()
src_repo = raw_input("Source repository (format: user/src_repo): ")
issuenumber = raw_input("Enter Issue Number to import from %s:" % src_repo)
dst_repo = raw_input("Destination repository (format: user/dst_repo): ")
#==== end of configurations ===

server = "api.github.com"
src_url = "https://%s/repos/%s" % (server, src_repo)
dst_url = "https://%s/repos/%s" % (server, dst_repo)

## helper function for secure requests
def request(logging_context, url, body=None):
	if body:
		print "Request[%s]: %s w/ body=%s" % (logging_context, url, body)
	else :
		print "Request[%s]: %s" % (logging_context, url)
	req = urllib2.Request(url, body)
	req.add_header("Authorization", "Basic " + base64.urlsafe_b64encode("%s:%s" % (username, password)))
	req.add_header("Content-Type", "application/json")
	req.add_header("Accept", "application/json")
	return urllib2.urlopen(req)

def get_issue(url, issuenr):
    response = request('get_issues', "%s/issues/%s" % (url, issuenr))
    result = response.read()
    return json.load(StringIO(result))

def get_comments_on_issue(issue):
	if issue.has_key("comments") \
	  and issue["comments"] is not None \
	  and issue["comments"] != 0:
		response = request('get_comments_on_issue', "%s/comments" % issue["url"])
		result = response.read()
		comments = json.load(StringIO(result))
		return comments
	else :
		return []

# import an issue only with assignee and body
def import_issue_simple(source):
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
        "milestone": None,
        "labels": []
    })

    res = request('import_issues', "%s/issues" % dst_url, dest)
    data = res.read()
    res_issue = json.load(StringIO(data))
    print "Successfully created issue %s" % res_issue["title"]

    # todo: import comment for issue
    comments = get_comments_on_issue(source)

def main():
	#process issues
	issue = get_issue(src_url, issuenumber)
	print issue
	doImport = raw_input("import this issue to %s? (y/n) " % dst_url)
	if doImport == "y":
	    import_issue_simple(issue)


if __name__ == '__main__':
	main()