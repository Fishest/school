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

--------------------------------------------------------------------------------
What is a Branch
--------------------------------------------------------------------------------

When you commit, git stores a commit object that contains a pointer to the
snapshot of the content you staged, some metadata, and possibly pointers to
direct parents of this commit: zero for initial commit, one for a normal commit,
two or more for merges::

    # -------------------------------------------------------------
    # commits, trees, and blobs link by sha1 ids
    # -------------------------------------------------------------
    [commit: 98ca9..]
     author  -> 'username'
     message -> 'commit message'
     tree    -------------------> [tree: 92ec2..] 
                                   blob: path, ---> [blob: 911e7..]
                                   blob: path,----> [blob: 5b1d3..]
                                                     'blob content'

    # -------------------------------------------------------------
    # commits link together by parent sha1 ids
    # -------------------------------------------------------------
    [commit: 98ca9..] <-- [commit: 98ca9..]
     tree: 92ec2..         tree: 98237..
     parent: null          parent: 98ca9..

So a branch is simply a lightweight movable pointer to one of these commits. By
default you have a branch named `master` which points to the current commit and
is advanced every time one checks in. By creating a branch `develop`, you just
have another pointer. To know what branch you are on, git uses a special pointer
called `HEAD`::

    [HEAD]
     \/
    [branch: master ]     [branch: develop]
     \/                    \/
    [commit: 98ca9..] <-- [commit: 98ca9..]
     tree: 92ec2..         tree: 98237..
     parent: null          parent: 98ca9..

When you merge in git, it will walk back through the hitory of the requested
merge points until it finds the best common ancestor to start the merge from.
It will then create a merge snapshot (a merge commit with multiple parents)
that is the three way merge of the the merge points.

.. note:: When you can merge two branches and one can follow the other's commit
   history and apply its change cleanly at the end, this is called a
   `fast-forward` and git does this automatically.

If git can perform an automatic merge, it will, however if it is unsure (say
multiple people worked on the same lines of the same file) it will mark merge
conflicts that the user must manually resolve. Running a `git status` will show
the files that need to be manually merged and the merge errors will be marked
in the files like this (betwee <<< and === is the master and between === and >>>
is your branch)::

    <<<<<<< HEAD:index.html
    <div id="footer">contact : email.support@github.com</div>
    =======
    <div id="footer">
      please contact us at support@github.com
    </div>
    >>>>>>> iss53:index.html

After you change the file with the data that is correct and save the file,
then just do a `git add` on this file to mark it as resolved. Do this for each
conflicted file reported by `git status`. You can also use a graphical tool to
do this for you by calling `git mergetool`. When you are finished with the
merge, simply `git commit`.

--------------------------------------------------------------------------------
Git branch
--------------------------------------------------------------------------------

What follows is a cheat sheet for working with branches:

.. code-block:: bash

    git branch                # lists all the available local branches
    git branch -a             # lists all the local and remote branches
    git branch -v             # shows the last commit on each branch
    git branch --merged       # show the branches that are merged into HEAD
    git branch --no-merged    # show the branches that are not merged into HEAD
    git branch <branch>       # create the specified branch
    git branch -d <branch>    # delete the specified branch

--------------------------------------------------------------------------------
Workflow: Example
--------------------------------------------------------------------------------

It is considered good practice to use branches as much as possible. In your
daily development. The general idea is called topic branches and they can exist
long term or short term, however, they generally cover some unit of work.
Consider for example using the following branches:

* `master` is used for tracking the mainline
* `develop` is used as a merge point for upstream changes
* `feature-<name>` is for working on a new feature
* `hotfix-<name>` is for working on a quick hotfixes
* `release-<name>` is for working on code that is soon to be released

For a more complete example, follow the gitflow workflow:

.. image:: http://nvie.com/img/2009/12/Screen-shot-2009-12-24-at-11.32.03.png
   :target: http://nvie.com/posts/a-successful-git-branching-model/
   :align: center

.. code-block:: bash

    git pull origin            # update master from origin
    git checkout -b issue-537  # create a new topic branch and change to it
                               # git branch issue-537 && git checkout issue-537
    git commit -am "working"   # commit some code for that issue
                               # something goes wrong in production
    git stash                  # save un-commited changes, or commit them
    git checkout master        # switch back to master
    git checkout -b hotfix     # create a new hotfix branch for fixing issue
                               # do the required work to fix issue
    git checkout master        # switch back to master
    git merge hotfix           # merge in code for fixing issue
    git branch -d hotfix       # delete the unused branch
    git checkout issue-537     # return to your work


--------------------------------------------------------------------------------
Remote Branches
--------------------------------------------------------------------------------

Remote branches are references to the state of branches on your remote
repositories. They are local branches that cannot be moved. They are moved
automatically whenever you do network communication. Think of them as bookmarks
to remind you where the remote repositories were when you last connected::

    <remote>/<branch>          # the format for querying remote branches
    origin/master              # how to query current master
    
    #-------------------------------------------------------------
    # initial state
    #-------------------------------------------------------------
                  [origin/master]
                   \/
    [12345..] <-- [23456..]
                   /\
                  [master]
    
    #-------------------------------------------------------------
    # after `git fetch origin`
    #-------------------------------------------------------------
    
                                [origin/master]
                                 \/
    [12345..] <-- [23456..] <-- [34567..]
                   /\
                  [master]

When you fetch code from remotes, it should be noted that you do not have a
branch you can work on, you just have a `origin/newbranch` pointer.  You can
merge this pointer into your current branch with `git merge origin/newbranch`
or you can create your own branch based on the remote one:

.. code-block:: bash

    git checkout -b <branch> <remote>/<branch>   # local/remote names can differ
    git checkout -b newbranch origin/newbranch   # create a tracking branch
    git checkout -track origin/newbranch         # the same as above

When you checkout a local branch from a remote branch, a tracking branch is
created. This allows one to use `git pull` and `git push` to easily interoperate
with the remote.

--------------------------------------------------------------------------------
Pushing Branches
--------------------------------------------------------------------------------

If you already have a remote setup and the branch already exists remotely (and
you have write access), you can simply push the code to the remote when you are
ready:

.. code-block:: bash

    git push origin serverfix      # push your serverfix branch changes up
    git push origin local:remote   # push your branch named `local` to the
                                   # remote branch named `remote`
    git push origin :serverfix     # delete the remote branch named serverfix

--------------------------------------------------------------------------------
Rebasing
--------------------------------------------------------------------------------

Instead of merging two paths in git, you can re-apply the front-runner to the
back of existing changes, what is known as rebasing. This works by finding the
first common ancestor of the two branches, generating diffs of each commit
since your current local branch, and applying them until you arrive at the
current state of your branch::

    #-------------------------------------------------------------
    # initial state
    #-------------------------------------------------------------
                           [experiment]
                                \/
                       \/  <-- [C3] <--  \/
    [C0] <-- [C1] <-- [C2] <-- [C4] <-- [C5]
                                         /\
                                      [master]

    #-------------------------------------------------------------
    # after rebase
    #-------------------------------------------------------------
    # git checkout experiment
    # git rebase master
    #-------------------------------------------------------------
                                    [experiment]
                                         \/
    [C0] <-- [C1] <-- [C2] <-- [C4] <-- [C3']
                                /\
                             [master]

There are a number of advantages or reasons for doing work this way:

* It makes the commit history appear linear (even though it was parallel)
* It makes commits apply cleanly on a remote branch
* It reduces the burden of an upstream party to just doing a fast-forward

If you have more complex rebasing tasks, you can use the `--onto` flag::

    #-------------------------------------------------------------
    # initial state
    #-------------------------------------------------------------
                             [master]
                                \/    [server]
    [C0] <-- [C1] <-- [C5] <-- [C6]      \/
              /\  <-- [C3] <-- [C4] <-- [C10]
                       /\  <-- [C8] <-- [C9]
                                         /\
                                      [client]

    #-------------------------------------------------------------
    # after rebase
    #-------------------------------------------------------------
    # git rebase --onto master server client    # rebase down
    # git checkout master                       # switch to master
    # git merge client                          # fast forward
    #-------------------------------------------------------------
                                                [master]
                                                   \/    
    [C0] <-- [C1] <-- [C5] <-- [C6] <-- [C8'] <-- [C9']
              /\  <-- [C3] <-- [C4] <-- [C10]      /\
                                         /\     [client]
                                       [server]
    #-------------------------------------------------------------
    # after rebase
    #-------------------------------------------------------------
    # git rebase [base branch] [topic branch]
    # git rebase master server                  # rebase down
    # git checkout master                       # switch to master
    # git merge server                          # fast forward
    # git branch -d client                      # remove client branch
    # git branch -d server                      # remove server branch
    #-------------------------------------------------------------
                                                           [master]
                                                              \/    
    ... <-- [C6] <-- [C8'] <-- [C9'] <-- [C3'] <-- [C4'] <-- [C10']
                 

.. note:: Rebasing replays changes from one line of work onto another in
   the order they were introduced, wheras merging takes the endpoints and
   merges them together.

.. note:: Do not ever rebase commits that have been pushed to a public
   repository!
