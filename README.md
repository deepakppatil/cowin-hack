# cowin-hack

CLI written for announcing the co-win vaccination booking. 

## Setup (MacOS)

##### Requirements
* Python 3(3.9)
* Pip 3

##### For quik dev environment
* Jupyter-lab

```bash
$ brew install python3
```

##### No homebrew, no problem..run:

```bash
$ mkdir homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C homebrew
```

Pip3 is installed with Python3, to ross check the version, Run:

```bash
$ python --version
$ pip --version
```

##### Installation python 

To install python run:
```bash
$ brew install python3
```

[Trouble](https://ahmadawais.com/how-to-set-python-default-version-to-3-on-macos/) installing on Macos?

To install virtualenv via pip run:

```bash
$ pip install virtualenv
```
[About Virtualenv](https://virtualenv.pypa.io/en/stable/)


## Setup the crawler

##### Git clone 

```bash
$ git clone https://github.com/deepakppatil/cowin-hack.git

$ cd cowin-hack
```

##### How to run

Creation of virtualenv:
```bash
$ virtualenv -p python ./cowinhack
```

Activate the virtualenv & Install all required packages
```bash
$ source cowinhack/bin/activate

$ pip install -r ./requirements.txt
```

Run Cli

Help|list|start


```bash

# For help
$ python cowinhack.py --help

# For listing all the centers or specific centers

python cowinhack.py list -p 421301

# Or just

python cowinhack.py list

# start the crawler

python cowinhack.py start --show --interval 5 --pincode 421301

```


Deactivate the virtualenv(Only when we are done with work.):
```bash
$ deactivate
```

#### How to set the Development: You are all set for private environment - Run 

To install jupyterlab via pip run:

```bash
$ pip install jupyterlab

$ pip list
```

Start Jupyterlab, since jupyter is now available in you private virtual machine over here - <desired-path>/cowinhack

```bash
$ jupyter notebook
```

Use the notebooks..



