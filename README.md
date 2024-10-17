![My Package Logo](assets/logo.png)

This is dbnl_bear, a python package to make it easier to use AI for reading assistance in historical analaysis. 

The "bear" part of the package name is inspired by a passage from Alex Komoroske's Bits and Bobs:

"LLMs are like a trained circus bear that can make you porridge in your kitchen. It's a miracle that it's able to do it at all, but watch out because no matter how well they can act like a human on some tasks they're still a wild animal. They might ransack your kitchen, and they could kill you, accidentally or intentionally. Just because it can talk like a human doesn't mean it deserves the responsibility of a human!" (editorial changes by AvD)

Currently, this package is under construction. 

The goal of the package is to make it easier for historians to use AI in their research. It will assist in parsing texts, sending them to the OpenAI API, and viewing the results. 

Workflow I aim for: 

- User has folder with ~10 xml files from dbnl
- Package strips xlm to txt
- User looks for certain object
- Package filters txt files for relevant parts
- User wants to see these parts in a clear way
- User can see the relevant data in barcode plot, highglighted in word document, or in txt document list per text