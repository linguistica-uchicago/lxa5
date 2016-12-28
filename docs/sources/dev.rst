.. _GitHub: https://github.com/

.. _Git: https://git-scm.com/

.. _Miniconda: http://conda.pydata.org/miniconda.html

.. _PyCharm: https://www.jetbrains.com/pycharm/

.. _dev:

For developers
==============

This page provides technical notes for the developers of the Linguistica 5 group.
For introductory background about the Linguistica 5 codebase,
please consult :ref:`codebase`.

None of the development notes here are
new, as they all come from the collective wisdom of the open-source and
software development community -- notably, for what is known as "gitflow".
They should be taken as best practice recommendations, and nothing is set in stone.
While your general goal is to get pull requests up,
the way how you make pull requests is entirely up to you.
Naturally, you can deviate from any of the advice given here;
in that case, you are on your own and you know what you are doing.

.. _dev_reminders:

Important reminders
-------------------

1. **Never commit changes to a master branch.**

      Not even at your own fork -- this ensures that the master branch
      is always clean and serves as a fall back.

2. **Create task-specific branches.**

      Never create a branch like "develop" and "research" and plan to vomit
      a huge amount of your great work into it before making any pull requests
      (this would make code review impossible). Think of a branch as something
      much more concrete like a mini project, with branch names like
      "add-feature-x" or "fix-function-x".

3. **Keep pull requests small.**

      A pull request has to be small (say, fewer than 300 lines of changes)
      so that the code review can be done efficiently and effectively with
      useful feedback.

4. **Follow PEP 8 in coding.**

      The `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_
      coding conventions exist precisely because we would like to schedule
      exactly no time for discussing things like "how to name variables",
      "whether space is needed" and so on for coding.
      There are excellent IDEs such as PyCharm_ for maintaining Python projects
      at a high level of quality.


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

      If you are sure that you have Python 3 with the required dependencies
      (NumPy, SciPy and networkx) and are happy to use it for the Linguistica 5
      development work, then you may skip this section. Otherwise,
      consider using Miniconda_ (get Python 3.5).

      Miniconda allows you to set up specific environments with a specific version
      of Python and dependencies. For our purposes, you can use Miniconda to
      create a dedicated environment for the Linguistica 5 project (and no other
      projects).
      Having such a dedicated environment is desirable as you are likely working
      on multiple projects at any given time (Linguistica 5 being just one of them),
      and you don't want the environment for one project to contaminate that for
      another project.

      After Miniconda is installed,
      run the following command to create the new environment
      for Linguistica 5:

      .. code::

         $ conda create -n lxa5 python=3.5 numpy scipy networkx

      This command creates the new environment called ``lxa5`` with Python 3.5
      as well as the specified dependencies for Linguistica 5. After this command
      is done with all the installation work, run the following to activate the
      new environment ``lxa5``:

      .. code::

         $ source activate lxa5

      Now you are in the ``lxa5`` environment (no longer in the root environment).
      As an indicator for this change, your command line prompt is now prefixed
      with ``(lxa5)``. Whenever you are working on the Linguistica 5 codebase,
      be sure you are in this environment at your command line
      (otherwise you might get puzzled: "I thought I had the correct Python
      version, but it's not right?" or "I thought I already had SciPy but it
      says it's not there?" etc.). If you run ``python`` now, you will see
      the Python interpreter says it is the Python 3.5 distribution by
      Continuum Analytics, Inc. (the company that maintains Miniconda).

      To deactivate the environment (for going back to the root environment, or
      for preparing to switch to another environment), simply run this:

      .. code::

         $ source deactivate


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

After you have set up your system and downloaded Linguistica 5 as described above,
you are now (almost) ready to do awesome work!

1. **Verify that the master branch on your local drive is up-to-date in sync with
   the master on linguistica-uchicago/lxa5.**

      It is important to make sure you start working with the latest
      codebase:

      .. code::

         $ git checkout master  # go to master branch
         $ git pull upstream master  # pull latest from master branch of upstream

      Recall that "upstream" means the linguistica-uchicago/lxa5 repository.


2. **Create a new branch for your great work.**

      Never work from the master branch.
      (Run "git branch" anytime to see what branches you have and which branch you're on.)

      Instead, work on a different branch whose name indicates what you are doing,
      e.g. "revamp-stems-to-signatures", "update-docs", "fix-bug-in-function-x":

      .. code::

         $ git checkout -b <branch-name>

      After this command is run, the new branch is created *and* you are on
      that branch as well (no longer on master branch).

3. **Start committing changes to source code.**

      Now (and finally!) you can actually make changes to the source code.
      Make changes incrementally and commit them with Git.
      Run this pair of commands for each commit:

      .. code::

         $ git add <files-changed>
         $ git commit -m "<commit-message>"

      Write brief and meaningful commit messages,
      e.g. "Fix bug in stems_to_signatures".
      Aim at making each commit a logical and meaningful chunk of changes.

4. **Repeat step 3 above as needed.**

      Repeat step 3 for making more commits on your way to what the branch
      is for. Limit the number of line changes to below 300 to make
      efficient and effective code review possible.

5. **Push your changes to your fork on GitHub.**

      To make your changes available for review and for merging,
      you will first have to push your changes to your fork on GitHub:

      .. code::

         $ git push origin <branch-name>

      Recall that "origin" is the (default) name of your fork <your-github-username>/lxa5 on GitHub.

6. **Make a pull request.**

      Log on to your GitHub and go to your fork <your-github-username>/lxa5.
      Now you are ready to make a pull request
      (i.e. you want linguistica-chicago/lxa5 to get the changes
      from your <branch-name> of <your-github-name>/lxa5, as it were).
      Click "Pull request"
      (or something like "Make pull request" -- it should be something fairly prominent visually).
      Now you'll wait for feedback.

7. **Start a new branch for a new mini project.**

      After all your hard work in the pull request has been accepted (= merged
      into linguistica-uchicago/lxa5), you can go back to step 1
      to update your master branch for the latest code and prepare
      for a new branch and an upcoming pull request!
