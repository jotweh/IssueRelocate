Issue Relocator
=============

This is a fork of https://github.com/Raizlabs/RZGithubUtils

In addition to the original script, this fork provides also a simple issue copy script to copy a single issue from one repository to another.
* Usage: <pre>python gh-issue-import-simple.py</pre>
* Supports private repositories as well
* Will display the issue in json format and ask you to confirm before copying
* Copies labels and milestones as well
* It does **not** copy the issue comments
* Instead, it is closing the issue in the source repository and adding a referencing comment to the old issue.

