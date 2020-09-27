======================
Multiple Dispatch Test
======================

.. image:: https://img.shields.io/badge/github-goerz--testing/multiple__dispatch__test-blue.svg
   :alt: Source code on Github
   :target: https://github.com/goerz-testing/multiple_dispatch_test

.. image:: https://img.shields.io/badge/License-BSD-green.svg
   :alt: BSD License
   :target: https://opensource.org/licenses/BSD-3-Clause

Experimental implementation of multiple dispatch.

This is an implementation based on, inspired by, and extending multimethod_, with the following features:

* It should be possible to register multiple implementations for the same signature
* An implementation the raises ``NotImplemented`` delegates to the next possible implementation
* multi-functions remain functions, so that Sphinx works correctly.
* Must work within Jupyter notebook
* Must allow multi=functions to be mapped with multiprocessing

.. _multimethod: https://github.com/coady/multimethod
