
================================================================================
Git SCM
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

Git is a distributed SCM that views differences to the filesystem as the unit of
change instead of changes to individual files. Every change is marked with a
unique SHA-1 hash. Each user has a complete copy of the repository when they
check it out.

--------------------------------------------------------------------------------
Getting Code
--------------------------------------------------------------------------------

* `git clone` adds a remote `origin` and does a `git pull`
* `git fetch` pulls down branches, but does not merge them
* `git pull` does `git fetch` followed by `git merge`

--------------------------------------------------------------------------------
Remotes
--------------------------------------------------------------------------------

.. code-block:: bash

    git clone <repository>             # this adds a branch of origin
    git remote                         # show all your remote repositories
    git remote -v                      # show all your remote repositories with full url
    git remote add other <repository>  # add a new remote
    git fetch other                    # you now have all of other's branches as other/<branch>
    git push <remote>> <branch>        # pushes your changes upstream to the remote
    git remote show <remote>           # show information about the remote branch
    git remote rename other newer      # renames the short name of a remote
    git remote rm newer                # removes a remote


