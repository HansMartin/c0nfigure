# c0nfigure


_c0nfigure.py_ is just another dotfile manager

with a simple yaml config, you can map your github dotfiles repo to the local config file paths using symlinks


### c0nfig.conf example

```yaml
github: "hansmartin/dotfiles"
install: "install.sh"
bash:
    - ["bashrc", "~/.bashrc"]
    - ["bash_aliases", "~/.bash_aliases"]
i3:
    - ["config", "~/.config/i3/config"]
    - ["i3blocks.conf", "~/.config/i3/i3blocks.conf"]

tmux:
    - ["tmux.conf", "~/.tmux.conf"]

vim:
    - ["vimrc", "~/.vimrc"]
    - ["autoload/plug.vim", "~/.vim/autoload/plug.vim"]

wallpaper:
    - ["mywallpaper.jpg", "~/Pictures/wallpaper.jpg"]

```


**Global Variables**

In the config are some "global" config variables, to adjust the tools settings

* github
* repo_dir
* install

__github__ sets the users github account (Format: username/repository)

__repo_dir__ is a path to a local directory where the repo ist stored

__install__ is a path (relative to the repository) of a shellscript that gets executed before symlinking


**Config Path**

The default config path is ~/.c0nfig.conf

Or can use your a config with the Parameter -c <config>


### Installation

_Note_: Its tested on python2.7 and no dependencies are required

```bash
git clone https://github.com/HansMartin/c0nfigure.git
cd c0nfigure
python c0nfigure.py


Usage: c0nfigure.py <option>

--init           	Use this on first run
--config <config>	Path to config file (=> default @ ~/.c0nfig.conf)
--link           	makes the symlink with given information
--push           	Updates the repository
--pull           	Refreshes the files (git pull)
--verbose, -v    	Some more output
--backup, -b     	Make backup of existing symlinks

```



