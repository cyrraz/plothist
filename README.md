# Installation instructions

* Install flit
`pip3 install --upgrade flit --user`

* Install boost_histogram
`pip3 install --upgrade boost_histogram --user`

* Clone the plothist repository
`git clone git@github.com:cyrraz/plothist.git`

* Install the plothist library. Go inside the plothist folder and run
`flit install --symlink`
(If does not work, try `python3 -m flit install --symlink`)

The plothist library can now be imported in any of your scripts. Check examples.
To update the plothist library, go to the library repository, and run `git pull`.

# Notes

* To run the python examples, you may need to install python3-tk: `sudo apt-get install python3-tk`.
