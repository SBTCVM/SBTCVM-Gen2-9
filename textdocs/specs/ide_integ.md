The following is a standardized guide to integrating support for
common SBTCVM development files into IDEs.

keyword listing list names are in italics

## SSTNPL IDE notes:

### syntax highlighting:

- commands & conditional mode keywords
- text in print/prline statements
- ternary, decimal, & character literals. (the docs have detailed descriptions of these.)
- references to constants (prefaced with a `$`, e.g. `$module.myconstant`)
- comments, prefaced with a `#`
- highlight var, label, include, marker, constant, macro, & table statements specifically.

### If applicable, IDE keyword listing should have lists of: 

- var statements _vars_
- labels _labels_
- marker statements. (debugging markers) _markers_
- table statements. _tables_
- const statements _constants_
- def statements _macros_ (note these technically are **NOT** functions, but syntax-wise they behave similarly enough)

Also:

- Ensure code blocks are properly marked if applicable. Generally everything 
that requires a matching **end** statement creates a block.

in addition, You should apply the SBTCVM Assembly IDE notes to inline-assembly
statements (asm/a commands). keyword list names for assembler code should
be prefixed with `asm`
## SBTCVM Assembly IDE notes:

 

### syntax highlighting:

- keywords
- comments
- labels (always delineated with second semicolon. e.g. `setreg2;0;my_label`)
- namespace references (usage of labels/namespace variables)
- v> namespace definition statements
- header variables. i.e. head-nspin=stdnsp
- include keyword should be highlighted especially.


### If applicable, IDE keyword listing should have lists of: 

- v> namespace definition statements _namespace vars_
- goto reference labels _labels_
- header variables. i.e. head-nspin=stdnsp _header_
- include/includeas keyword statements. _include_ 