# cson2lang

Convert language specs from `.cson` files (used by Atom) to `.lang` format (used by gedit and others).


## Installation

1. Clone this repository.
2. Get into a Python 3 environment.
3. `pip install -r requirements.txt`
4. `python3 convert.py source.cson > output.lang`


## Using your shiny new language file

Copy the output file into wherever gtksourceview language specs live on your machine. Something like this might work:

    sudo cp output.lang /usr/share/gtksourceview-3.0/language-specs/meaningful-name.lang


## License Stuff

The hcl.cson file is from MIT-licensed https://github.com/fd/language-hcl . I did have to add block-comments to it, which are commented in the code; my edits may/may not actually work with Atom, and I don't care, so I didn't submit a PR to upstream.

The other stuff is my original work. It's also MIT Licensed, but I hope you do good with it. (I'd love to hear about the good you're doing. Drop me a line!)


## References

* [Language Definition v2.0 Reference — Reference to the GtkSourceView language definition file format ](https://developer.gnome.org/gtksourceview/stable/lang-reference.html)


## Search Engine Terms

* cson
* Atom
* gedit
* gtksourceview-3.0
* xml
