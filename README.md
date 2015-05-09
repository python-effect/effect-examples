# Effect Examples

This repository contains examples of using Effect. They demonstrate basic use
of Effect to isolate side-effects from code, but also to provide alternative
implementations of those side-effecting actions without requiring changes to
core application logic.

This package isn't meant to be installed, but rather just copied to your local
dev environment and tinkered with. To install dependencies use ``pip install -r
requirements.txt``.

## http

The [`http`](http) directory contains a very simple `HTTPRequest` intent and
performers using common HTTP client libraries:
[requests](http://warehouse.python.org/project/requests/) and
[treq](https://warehouse.python.org/project/treq/).

treq is a Twisted-based library, showing that Effect can be used (with the
additional [txeffect](https://github.com/python-effect/txeffect) package) to
write generic code that can use either Twisted-based asynchronous IO or normal
blocking IO. Other asynchronous frameworks (such as Python 3's ``asyncio``)
could also be used in this way.

## readline_intent

The [`readline_intent.py`](readline_intent.py) file has a simple `ReadLine`
intent that uses `raw_input` (or `input` in Py3) to prompt the user for input.

## github

The `github` directory contains a simple application that lets the user input a
GitHub username and prints out a list of all repositories that that user has
access to. It depends on the `http` and `readline_intent` modules.

Note that if you run this example too rapidly, GitHub might temporarily block
your IP from making anonymous API requests for some short period of time.

There are two entrypoints into the example:
[`github.sync_main`](github/sync_main.py) and
[`github.twisted_main`](github/twisted_main.py). `sync_main` does
typical blocking IO, and `twisted_main` uses asynchronous IO. Note that the
vast majority of the code doesn't need to care about this difference; the only
part that cares about it is the `*_main.py` files. All of the logic in
[`core.py`](github/core.py) is generic.

To run them:

    python -m github.sync_main

or

    python -m github.twisted_main


Note that the twisted example does not run on Python 3, but all other examples
do.


The github example app has unit tests in
[`test_core.py`](github/test_core.py). They can be discovered and run simply by
running ``py.test`` in the top-level directory.
