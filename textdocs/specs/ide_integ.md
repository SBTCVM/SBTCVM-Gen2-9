The following is a standardized guide to integrating support for
common SBTCVM development files into IDEs.

keyword listing list names are in italics

## SSTNPL IDE notes:

### syntax highlighting:

- commands & conditional mode keywords
- text in print/prline statements
- ternary, decimal, & character literals.
- comments
- highlight var, label, marker, & table statements specifically.

### If applicable, IDE keyword listing should have lists of: 

- var statements _vars_
- labels _labels_
- marker statements. (debugging markers) _markers_
- table statements. _tables_

in addition, You should apply the SBTCVM Assembly IDE notes to inline-assembly
statements (asm/a commands). keyword list names for assembler code should
be prefixed with `asm`
## SBTCVM Assembly IDE notes:

 

### syntax highlighting:

- keywords
- comments
- goto reference labels
- v> namespace definition statements
- header variables. i.e. head-nspin=stdnsp
- include keyword should be highlighted especially.


### If applicable, IDE keyword listing should have lists of: 

- v> namespace definition statements _custom vars_
- goto reference labels _labels_
- header variables. i.e. head-nspin=stdnsp _header_
- include keyword statements. _include_ (list filenames themselves)