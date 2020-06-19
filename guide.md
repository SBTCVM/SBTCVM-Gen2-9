# Quick start guide



Run a trom application in pygame frontend:      
`./pyg_sbtcvm.py maze`

Start SBTCVM XAS interactive shell:      
`./xas.py`
     
Start TUI Shell (SBTGSH) _(PYGAME FRONTEND ONLY)_:    
`./pyg_sbtcvm.py sbtgsh`

Start GUI 'desktop' (SBTCVM BENCH) _(PYGAME FRONTEND ONLY)_:    
`./pyg_sbtcvm.py bench`

Boot into VDI shell (unfinished):     
`./pyg_sbtcvm.py`


Run a trom application in curses frontend:     
`./cur_sbtcvm.py maze`

_**Notice:**  curses frontend is somewhat buggy & incomplete. pygame frontend HIGHLY recommended._



### where does SBTCVM search for applications and source code?
In order _(non-bold text describes what applications & source code is kept there)_

 - **vmsystem**: assembler standard libs.
 - **vmsystem/roms**: system roms live here.
 - **roms**: quite a lot of test troms.
 - **apps**: Interactive trom applications.
 - **demos**: a variety of demos, showing off SBTCVM's graphical capabilities.
 - **vmuser**: your personal directory.

Notes:

 - Any directory within these, prefixed with **`r_`** Will have its contents in the
path. i.e. **`r_standard_lib`** in vmsystem
 - Most trom applications & demos use **`auto directories`**. where a directory name can 
be used as an argument for a certain SBTCVM filetype, if it contains a file of that type 
prefixed with **`auto_`**

[XAS help](/textdocs/mdhelp/xas.md) has more information on working with directories.

### where should i install 3rd party trom apps and assembler libraries?

 - vmuser

### more information:
- [SBTCVM Technical Glossary](/textdocs/mdhelp/glossary/glossary.md) A, markdown-based, Glossary of various technical terms used in SBTCVM.
- [SBTCVM Help Index](/textdocs/mdhelp/index.md) A, markdown-based, set of help documents (main index)
- [XAS help](/textdocs/mdhelp/xas.md) Help on SBTCVM's XAS shell/build script system, with detailed command listing.

- The [textdocs](/textdocs/) directory in this repository contains both technical and user documentation.
- [textdocs/SSTNPL](textdocs/SSTNPL/) contains documentation to the SSTNPL programming language.
- [apps/directory.txt](/apps/directory.txt) in this repository, has a guide on the TROM applications available there.

#### Before filing bug reports, read the troubleshooting guide:
- [Troubleshooting guide](/textdocs/mdhelp/troubleshoot/troubleshoot.md)


### Links:
- [Project blog](https://sbtcvm.blogspot.com/)
- [FAQ](https://sbtcvm.blogspot.com/p/faqs.html)
- [SSTNPL guide](https://sbtcvm.blogspot.com/p/sstnpl-guide.html)
- [SBTCVM Assembly guide](https://sbtcvm.blogspot.com/p/g2asm-faq-and-start-guide-sbtcvm.html)
