RZGithubUtils
=============

RZGithubUtils

ARCHIVING DATA FROM AN OLD REPO AND LATER ADDING IT AGAIN
---------------------------------------------------------
Github allows us to archive repos, but we also want to asve the issues, milestones, and labels as well in case we want to reopen the repository on github.  
These are not included in the native archiving feature on github so here are 2 scripts to handle the migration of this data.  It should be done in conjunction with the github archiving feature.

There are just 2 steps:
1.export from source repo on github (RZ-gh-issues-export.py)
2.import to new repo on github (RZ-gh-issues-import.py)

HOW TO USE RZ-gh-issues-export.py
---------------------------------

Use the following bash commands:
$cd (to the local folder where you want to store the issues, milestones, and labels, this is where the scripts should probably be located as well)
$python RZ-gh-issues-export.py :fileprefix :source-repo
->Where fileprefix determines the name to prepended to the 3 files outputted by export.  
So, for example, if you type "reponame" then it will output reponame_issues.json, reponame_milestones.json, and reponame_labels.json
***The fileprefix will need to be the same in both export and import for this to work***
->Where source-repo is the name/path of the repo you want to download the data from.
So, for example, for the Rue La La repo we would use "Raizlabs/RueLaLa"
->Example script: $python RZ-gh-issues-export.py 1234 Raizlabs/RueLaLa

HOW TO USE RZ-gh-issues-import.py
---------------------------------

Use the following bash commands:
$cd (to the same dir that the files outputted from RZ-gh-issues-export are located)
$python RZ-gh-issues-import.py :fileprefix :username :destination-repo
->Where fileprefix is the same one from export (if you forgot you can just look at the part of the filename that comes before the last underscore)
->Where username is your github username
->Where source-repo is the name/path of the repo you want to upload the data to
