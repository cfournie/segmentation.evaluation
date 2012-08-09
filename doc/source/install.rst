Detailed Installation
*********************

If you are having difficulty installing SegEval, run through these detailed guides for your operating system.

Mac OSX and Linux
-----------------

Verifying Requirements
++++++++++++++++++++++

First let's verify that you have all of the requirements setup. Let's check for the right version of python.  Open up your terminal and enter::

  user@host$ which python

It should output some string that contains the number ``2.7`` in it, much like::
  
  /Library/Frameworks/Python.framework/Versions/2.7/bin/python

Now type::

  user@host$ python --version

You should see a version string returned that contains the number ``2.7`` in it, much like::

  Python 2.7.3

Now let's try to see whether ``setuptools`` is installed; type::

  user@host$ which easy_install

It should return a path that matches (except for the text after ``/bin/``) the output of the earlier call to ``which python``::

  /Library/Frameworks/Python.framework/Versions/2.7/bin/easy_install


Installing
++++++++++

After installing the required packages, open up your terminal and enter::
  
  user@host$ sudo easy_install segeval

Or, if you are using pip, open up your terminal and enter::
  
  user@host$ sudo pip segeval

To verify that it worked, type::

  user@host$ python -m segeval

It should complain by saying::

  usage: segeval [-h] {pi,k,b,f,r,p,pr,s,pk,wd,wpr} ...
  segeval: error: too few arguments


Windows
-------

Verifying Requirements
++++++++++++++++++++++

First let's verify that you have all of the requirements setup. Let's check for the right version of python.  Open up your terminal and enter::

  C:\>python --version

You should see a version string returned that contains the number ``2.7`` in it, much like::

  Python 2.7.3


Installing
++++++++++

Open up a command prompt (with administrator rights) and run::

  C:\>easy_install segeval

Or, if you are using pip, open up your command prompt and enter::
  
  C:\>pip segeval

To verify that it worked, type::

  C:\>python -m segeval

It should complain by saying::

  usage: segeval [-h] {pi,k,b,f,r,p,pr,s,pk,wd,wpr} ...
  segeval: error: too few arguments


Source Install
--------------

To install from source, clone the `source code repository from github <http://cfournie.github.com/segmentation.evaluation/>`_ using `git <http://git-scm.com/>`_ by running::

  git clone git://github.com/cfournie/segmentation.evaluation.git
  cd segmentation.evaluation/src/python/main/
  python setup.py install

Or `download <http://cfournie.github.com/segmentation.evaluation/>`_,  and extract it, and navigate to the ``src/python/main`` directory and run::

  python setup.py install

To verify that it worked, type::

  python -m segeval

It should complain by saying::

  usage: segeval [-h] {pi,k,b,f,r,p,pr,s,pk,wd,wpr} ...
  segeval: error: too few arguments

