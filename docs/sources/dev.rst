.. _GitHub: https://github.com/

.. _Git: https://git-scm.com/

.. _Miniconda: http://conda.pydata.org/miniconda.html

.. _dev:

For developers
==============

This page provides technical notes for the developers of the Linguistica 5 group.
For introductory background about the Linguistica 5 codebase,
please consult :ref:`codebase`.

None of the development notes here are
new, as they all come from the collective wisdom of the open-source and
software development community.
They should be taken as best practice recommendations, and nothing is set in stone.
You are entirely entitled to deviate from any of the advice given here;
in that case, you are on your own and you know what you are doing.

:ref:`dev_reminders`

To get started, please go the section :ref:`dev_overview` below.

.. _dev_reminders:

Important reminders
-------------------

1. **Never commit changes to a master branch.**

      Not even at your own fork -- this ensures that the master branch
      is always clean and serves as a fall back in case anything disastrous
      happens.

2. **Create task-specific branches.**

      Never create a branch like "develop" and "research" and plan to vomit
      a huge amount of your great work into it before making any pull requests
      (this would make code review impossible). Think of a branch as something
      much more concrete and
      a lot smaller in scale like "add-feature-x" or "fix-function-y".

3. **Work in bite sizes**

      Small commits, small pull requests.

4. **No more than 300 lines of changes in each pull request.**

      None of the project's core develoeprs can spend a lot of time working on
      Linguistica 5 in practice. All pull requests have to be small
      so that the code review can be done efficiently and effectively with
      useful feedback.

5. **Follow `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ in coding.**

      The coding conventions exist precisely because we would like to schedule
      exactly no time for discussing things like "how to name variables",
      "whether space is needed" and so on for coding. If we drift away from PEP 8,
      the Linguistica 5 codebase will degrade over time.


.. _dev_overview:

Overview of the development workflow
------------------------------------

brief intro of gitflow

(need graphic aids or something?)

introduce the key terms

- done only once: FORK the repo, CLONE it to local drive, REMOTE (git remote add upstream <url>)
- CHECKOUT master, PULL from upstream/master, CHECKOUT new branch
- make changes and COMMIT them, repeat this step as needed
- PUSH to fork on github
- make PULL REQUEST


Setting up the development environment
--------------------------------------

To work on the Linguistica 5 code:

1. **Set up a personal GitHub account**

      If you are setting a new GitHub_ account,
      pick a username preferably with lowercase letters only, e.g. "joesmith".
      The Linguistica 5 codebase is hosted on GitHub.
      Your contributions will be added to it via the GitHub interface.


2. **Download and install Git**

      Git_ is the version control system of the Linguistica 5 project.
      Your contributions will be managed and passed from your local drive to
      GitHub by Git.


3. **Download and install Miniconda**

      Install Miniconda_ for Python 3.5. (This installs a new Python distribution
      on your machine, but we are not going to use it directly.)

      You may want to take advantage of Miniconda for having a dedicated
      environment with a specific Python version and other dependencies
      for the Linguistica 5 project.

      Having such a dedicated environment is desirable as you are likely working
      on multiple projects at any given time (Linguistica 5 being just one of them),
      and you don't want the environment for one project to contaminate that for
      another project.

      After Miniconda is installed, by default you are at the root environment.
      If you fire up your Python interpreter from the command line,
      you should see you are on Python 3.5 whose distribution is by
      Continuum Analytics, Inc. (the company that maintains Miniconda).
      Exit the interpreter, and run the following command to create the new environment
      for Linguistica 5.

      .. code::

         $ conda create -n lxa5 python=3.5 numpy scipy networkx

      This command creates the new environment called ``lxa5`` with Python 3.5
      as well as the specified dependencies for Linguistica 5. After this command
      is done with all the installation work, run the following to activate the
      new environment:

      .. code::

         $ source activate lxa5

      Now you are in the ``lxa5`` environment (no longer in the root environment).
      As an indicator for this change, your command line prompt is now prefixed
      with ``(lxa5)``. Whenever you are working on the Linguistica 5 codebase,
      be sure you are in this environment at your command line
      (otherwise you might get puzzled: "I thought I had the correct Python
      version, but it's not right?!" or "I thought I already had SciPy but it
      says it's not there?!" etc.)

      To deactivate the environment (for going back to the root environment, or
      for preparing to switch to another environment), simply run this:

      .. code::

         $ source deactivate


$ pip install Sphinx flake8 pytest pytest-cov sphinx_rtd_theme


Getting Linguistica 5
---------------------

To download the Linguistica 5 codebase for development work:

1. Log on to your GitHub account and go to https://github.com/linguistica-uchicago/lxa5

2. At the top right hand corner, click "Fork".
   (If prompted for "where should we fork this repository", choose your own personal GitHub username.)

3. Now under your personal GitHub account, you see a new repository called "lxa5".

4. Clone this repository (i.e. <your-github-username>/lxa5, not linguistica-chicago/lxa5)
   onto your local disk using Git, and also install the Linguistica 5 Python library:

   .. code::

      $ git clone https://github.com/<your-github-username>/lxa5.git
      $ cd lxa5
      $ python setup.py develop

   (If you're on Linux, you will probably need ``sudo`` for the last command above).

   Now you have the Python library (called ``linguistica``) installed in development mode
   (i.e. changes in source code are immediately effective -- no need to uninstall
   and reinstall to try out new code).

5. Add a link to the linguistica-uchicago/lxa5 repository:

   .. code::

      $ git remote add upstream https://github.com/linguistica-uchicago/lxa5.git

   This command adds a new link to the linguistica-uchicago/lxa5 repository
   (not your fork) and names it as "upstream".
   From time to time, you will need to keep your local
   copy of the Linguistica 5 codebase up-to-date by pulling the latest code
   from the linguistica-uchicago/lxa5 repository. This added link (with the name
   "upstream") tells Git where to pull updates from.

   By default, after you have cloned and created a copy of Linguistica 5 on
   your local drive (in step 4 above), there is already a link called "origin"
   set up and linked to your fork on GitHub. Run the following to verify you
   have "origin" pointing to your fork and "upstream" pointing to
   linguistica-uchicago/lxa5:

   .. code::

      $ git remote -v


Committing changes and making a pull request
--------------------------------------------

And you're ready to do awesome work by changing the source code:

verify you are on master
pull from upstream/master


1. Never ever work from the "master" branch. (Run "git branch" to see what branches you have and which branch you're on.)

2. Instead, work on a different branch whose name indicates what you are doing, e.g. "fix-bug-in-stems-to-signatures", "update-docs". You can create a branch by "git checkout -b <branch-name>"

3. Now (and finally!) you can actually make changes to the source code. Make changes incrementally and commit them with git. Run this pair of commands for each commit:

$ git add <files-changed>
$ git commit -m "<commit-message>"

Write brief and meaningful commit messages.

4. Repeat step 3 above as many time as needed for making the new feature you're working on great. If possible, please limit the number of lines changes to below 300, so that it won't take forever to review your changes.

5. When you're ready to get comments on your changes, you will push your code to your fork on github and make a pull request.
6. To push your code to your fork:

$ git push origin <branch-name>

7. To make a pull request (i.e. you want linguistica-chicago/lxa5 to get the changes from <your-github-name>/lxa5, as it were), go to your GitHub page and then to the forked "lxa5" repository. Click "Pull request" (or something like "Make pull request" -- should be something fairly prominent visually). Now you'll wait for feedback.


(incorporate these notes:)

* Each commit is one single meaning and small chunk.

* Write meaningful commit messages
  (see `here <http://chris.beams.io/posts/git-commit/>`_, for instance).
  Each commit message consists of two components:
  (1) the subject line, and (2) the message body.
  The subject line is an imperative sentence (e.g. "Update readme"); note
  the first word is capitalized and there's no ending period. It contains
  no more than 50 characters. The message body explains what the commit
  is about. (If the commit is for something minor, e.g. "Tweak readme format",
  then the message body can be omitted.)

* **Before and after each coding session**, run ``python3 nosetests_run.py``
  to make sure nothing breaks.

