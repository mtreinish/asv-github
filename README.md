asv-github
==========

This repo contains a wsgi app for running asv against an arbitrary number of
repos based on github webhooks. It will maintain a local clone of a github
repo and run asv benchmarks each time a commit (or tag) is pushed.
