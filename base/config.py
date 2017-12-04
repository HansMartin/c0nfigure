import os

class base:

    config = {"config_file":os.path.expanduser("~/.c0nfig.conf"), "repo_dir":os.path.expanduser("~/.c0nfigure/repos")}
    # (var_name, isRequired), ...
    globals = [("github", True), ("repo_dir", False)]

    def __init__(self):
        pass

    def getHome(self, path=""):
        if path == "":
            return os.path.expanduser("~")
        return os.path.expanduser(path)


    """Creates the basic dir structure, should happen at the first run """
    def firstRun(self):

        try:
            os.makedirs(self.getHome(self.config["repo_dir"]))
            pinfo("Lets go!")
        except Exception as e:
            if e.errno == 17:
                pinfo("Looks like its already initialized")
            else:
                # Repository dir already created
                perror("Strange error creating directory structure")




def perror(msg):
    print("[-] " + msg)

def psuccess(msg):
    print("[+] " + msg)

def pinfo(msg):
    print("[*] " + msg)
