================================================================================
Chapter 1: Git SCM
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

Git is a distributed SCM that views differences to the filesystem as the unit of
change instead of changes to individual files. Every change is marked with a
unique SHA-1 hash. Each user has a complete copy of the repository when they
check it out. Think of git as a versioned filesystem with each version being
the next snapshot of the filesystem.

Files in a git repository can be in four(4) different states (the first three
are tracked):

* `commited`  - file is safely committed to the local database
* `modified`  - file is changed but not yet committed to the local database
* `staged`    - file is marked to go into next database commit
* `untracked` - file is not being tracked by git

These states are represented by three sections of a git project:

* `git directory` - stores the current repository information
* `working directory` - a single checked out version from the repository
* `staging area` - generally a file listing the operations to be committed

================================================================================
Chapter 2: Git Basics
================================================================================

--------------------------------------------------------------------------------
Common Operations
--------------------------------------------------------------------------------

The following is rough cheat sheet of the common git operations:

.. code-block:: bash

    git add <untracked>        # start tracking the file
    git add <modified>         # add the file to the staging area
    git add <merge-conflict>   # mark the merge conflict as complete
    git rm <tracked>           # delete a file from the repository
    git rm -f <modified>       # force a delete of a modified file
    git rm --cached <tracked>  # stop tracking a file (leave it on disk)
    git mv                     # move a file in the repository
    git commit                 # store the staging directory to the database
    git commit -a              # store all modified tracked files (skip staging)
    git commit --amend         # performs the last commit again (with possible changes)
    git reset HEAD <staged>    # unstage a file or all the files
    git checkout -- <modified> # reverts the changes to a modifed file
    git status                 # show the current state of the files in the repository
    git diff                   # show diffs of the files that are changed but not staged
    git diff --staged          # show the changes that are currently staged
    git config --list          # lists all your current settings
    git init                   # starts a new empty repository
    git clone                  # adds a remote `origin` and does a `git pull`
    git fetch                  # pulls down branches, but does not merge them
    git pull                   # does `git fetch` followed by `git merge`

--------------------------------------------------------------------------------
Git Log
--------------------------------------------------------------------------------

There are many ways to operate with the repository log; the followig are some
of the more common methods:

* `git log` displays the commit log of the repository
* `git log -p` displays the commit log of the repository with diffs
* `git log --stat` displays the commit log of the repository with statistics
* `git log --pretty=<format>` display the commit log in various formats

  - predefined values are: oneline, full, fuller
  - can supply own format string with `format:"%s"`

* `git log --graph` shows a simple merge graph (see also `gitk`)
* `git log -<N>` limits the log to the last N commits
* `git log --since=<time>` limits the log to a time point or range

  - can specify an absolute or relative date (`2008-01-05` or `2 years 1 day ago`)
  - can use helper units: `2.weeks`, `5.days`
  - also suported are since, before, after, until
  - can also filter `--author=<filter>`, `--committer=<filer>`
  - can filter for keywords in message with `--grep`
  - can filter for a file or directory by supplying it after `-- <file>`

--------------------------------------------------------------------------------
Ignoring Files
--------------------------------------------------------------------------------

Files can be ignored by adding them the .gitignore file. Here is an example
showing the various formats it accepts::

    # a comment  this is ignored
    *.a        # no .a files
    !lib.a     # but do track lib.a, even though you’re ignoring .a files above
    /TODO      # only ignore the root TODO file, not subdir/TODO
    build/     # ignore all files in the build/ directory
    doc/*.txt  # ignore doc/notes.txt, but not doc/server/arch.tx

--------------------------------------------------------------------------------
Remotes
--------------------------------------------------------------------------------

Git allows remote repositories to be linked via a number of protocals:

* **ssh**   : `ssh://user@host:<port>/path/to/repo`
* **https** : `https://github.com/user/repo.git`
* **git**   : `git://github.com/user/repo.git`
* **file**  : `/path/to/repo`

What follows is a cheat sheet for the common commands for working with remotes:

.. code-block:: bash

    git clone <repository>             # this adds a tracking branch as origin
    git remote                         # show all your remote repositories
    git remote -v                      # show all your remote repositories with full url
    git remote add other <repository>  # add a new remote
    git fetch other                    # you now have all of other's branches as other/<branch>
    git push <remote>> <branch>        # pushes your changes upstream to the remote
    git remote show <remote>           # show information about the remote branch
    git remote rename other newer      # renames the short name of a remote
    git remote rm newer                # removes a remote

When you do a `git remote add name <repo>` and then a `git fetch name`, git
pulls down the remote repository which can then be viewed, merged, etc from
`name/<branch>`. When you do a `git clone <repo>`, git creates a branch
named `origin` and then allows you to perform a `git pull` which essentially
does a `git fetch origin` and `git merge`. Also, you can only `git push` to
a repository that you have originally cloned from (if you have permission).

--------------------------------------------------------------------------------
Tags
--------------------------------------------------------------------------------

Tags can be used to mark significant points in the projects history (1.0
version, bug-fix, etc). Tags are not pushed with normal pushes, they must
be pushed like branches to remotes. There are two kinds of tags:

* **annotated** are represented as full objects in the git database with
  checksums, tagger name, email, message, and GPG signed. It is best to
  use these whenever possible.

* **light-weight** are simple pointers to a version (like a branch that
  does not change).

What follows is a cheat sheet for the common commands for working with tags:

.. code-block:: bash

    git tag                          # lists the available tags
    git tag -l 'v1.*'                # search for tags that match the query
    git tag v1.2                     # create a simple tag
    git tag -a v1.2 -m 'my message'  # create an annotated tag
    git tag -s v1.2 -m 'my message'  # create an signed annotated tag
    git tag -v v1.2                  # verify the signed tag (need public key)
    git tag -a v1.2 9cef3            # tag a previous commit
    git show v1.2                    # show information about the tag
    git push origin <tag>            # push a single tag to the remote
    git push origin --tags           # push all tags to the remote

--------------------------------------------------------------------------------
Common Aliases
--------------------------------------------------------------------------------

.. code-block:: bash

    git config --global alias.co      'checkout'      # git co
    git config --global alias.ci      'commit'        # git ci
    git config --global alias.br      'brach'         # git br
    git config --global alias.st      'status'        # git st
    git config --global alias.unstage 'reset HEAD --' # git unstage <file>
    git config --global alias.last    'log -1 HEAD'   # git last
    git config --global alias.visual  '!gitk'         # git visual


================================================================================
Chapter 3: Git Branching
================================================================================
