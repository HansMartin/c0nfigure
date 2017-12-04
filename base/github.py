from config import base
from config import perror, psuccess, pinfo

from subprocess import Popen, PIPE
import os



class github:

    def __init__(self, config):
        self.config = config
        self.url = "https://github.com/" + self.config["github"]
        self.cloneThatRepo()
        

    def cloneThatRepo(self):

        pinfo("Cloning the repository...")
        os.chdir(self.config["repo_dir"])
        proc = Popen(["git", "clone", self.url], stdout=PIPE, stderr=PIPE)

        stdout, stderr = proc.communicate()

        if stderr != "" and "already exists" in stderr: 
            perror("Repository already exists")



    def refresh(self, reponame=""):

        pinfo("Getting newest Version...")
        
        if reponame == "":
            reponame = self.config["github"].split("/")[1]


        fullPath = self.config["repo_dir"] + "/" + reponame

        os.chdir(fullPath)


        proc = Popen(["git", "pull"], stdout=PIPE, stderr=PIPE)

        stdout, stderr = proc.communicate()

        if stderr != "":
            perror(stderr)


    def updateRepo(self, reponame=""):
        pinfo("Updating repository...")

        if reponame == "":
            reponame = self.config["github"].split("/")[1]


        fullPath = self.config["repo_dir"] + "/" + reponame

        os.chdir(fullPath)

        procAdd = Popen(["git", "add", "."], stdout=PIPE, stderr=PIPE)

        stdout, stderr = procAdd.communicate()

        # Error checking
        if stderr != "": 
            perror(stderr)


        procCommit = Popen(["git", "commit", "-m", "c0nfigure"], stdout=PIPE, stderr=PIPE)

        stdout, stderr = procCommit.communicate()

        if stderr != "": 
            perror(stderr)

        procPush = Popen(["git", "push"], stdout=PIPE, stderr=PIPE, stdin=PIPE)


        procPush.wait()

        if stderr != "": 
            perror(stderr)


    """
    For a Full github URL, get only the username/repo combo
    """
    def getRepoName(self):
        tmpUrl = self.url
        tmpUrl = tmpUrl.replace("https://","").replace("http://", "")
        tmpUrl = tmpUrl.replace("github.com/", "").replace("www", "")

        return tmpUrl


    def update(self):
        os.chdir(self.config.repo_dir + "/" + self.getRepoName(self.config.github_url))

        proc = Popen(["git", "pull"], stdout=PIPE, stderr=PIPE)
