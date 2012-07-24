import urllib2
import base64
import getpass
import sys

#==== globals =======
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

def get_issues(url):
	response = urllib2.urlopen("%s/issues" % url)
	file = open(issues_filename, 'w')
	file.writelines(response)
	
def get_milestones(url):
	response = urllib2.urlopen("%s/milestones?state=open" % url)
	file = open(milestones_filename, 'w')
	file.writelines(response)

def get_labels(url):
	response = urllib2.urlopen("%s/labels" % url)
	file = open(labels_filename, 'w')
	file.writelines(response)

def main():

	#get the partial name of the file to be created from the 1st argument
	prepend = sys.argv[1]
	
	#set all the filenames
	set_filenames(prepend)
	
	#get the source repository from the 2nd argument
	src_repo = sys.argv[2]
	
	#set the source url
	src_url = "https://%s/repos/%s" % (server, src_repo)
	
	#get issues
	get_issues(src_url)
	
	#get milestones
	get_milestones(src_url)
	
	#get labels
	get_labels(src_url)

if __name__ == '__main__':
	main()