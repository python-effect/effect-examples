"""
Run this example with:
    python -m github.sync_main

This is an example of using Effect in a normal program that uses
synchronous/blocking functions to do I/O.

This code has these responsibilities:

- set up a dispatcher that knows how to find performers for all intents
  used in this application. The application uses ReadLine, HTTPRequest, and
  ParallelEffects.
- use :func:`effect.sync_perform` to perform an effect, which returns the
  result of the effect (or raises an exception it it failed).
"""

from __future__ import print_function

from functools import partial
from multiprocessing.pool import ThreadPool

from effect import ComposedDispatcher, ParallelEffects, TypeDispatcher, sync_perform
from effect.threads import perform_parallel_with_pool


from ehttp.http_intent import HTTPRequest
from ehttp.sync_http import perform_request_requests
from readline_intent import ReadLine, perform_readline_stdin

from .core import main_effect


def get_dispatcher():
    """
    Create a dispatcher that can find performers for :obj:`ReadLine`,
    :obj:`HTTPRequest`, and :obj:`ParallelEffects`.  There's a built-in
    performer for ParallelEffects that uses a multiprocessing ThreadPool,
    :func:`effect.perform_parallel_with_pool`.
    """
    my_pool = ThreadPool()
    pool_performer = partial(perform_parallel_with_pool, my_pool)
    return ComposedDispatcher(
        [
            TypeDispatcher(
                {
                    ReadLine: perform_readline_stdin,
                    HTTPRequest: perform_request_requests,
                    ParallelEffects: pool_performer,
                }
            )
        ]
    )


def main():
    dispatcher = get_dispatcher()
    eff = main_effect()
    print(sync_perform(dispatcher, eff))


if __name__ == "__main__":
    main()
