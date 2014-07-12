Markdown Resume
===============

A Python CLI that takes a resume in Markdown and renders it to PDF and/or HTML using pandoc.  Inspired by [https://github.com/mszep/pandoc_resume](pandoc_resume), with a number of additions that I wanted:

   * Be able to specify on the command line which theme to use on the resume
   * Have a separate, untracked, file containing all the sensitive information, which is then rendered into the resume at runtime so that all of the source can be on the web (this is achieved using pystache templates)
   * Simple find and replace so you can use Font Awesome icons by referring to them using their name, e.g. ``:fa-twitter:``

Installation
------------

The Python script has the following external dependencies:

   * pandoc
   * conTeXt


Usage
-----
