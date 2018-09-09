
Some simple extensions for use with Sphinx.

## Contextual admonition extension for Sphinx

### Example

```rst
.. contextual-admonition::
    :context: warning
    :title: Title for the admonition

    - Admonition text. This admonition will be stylized the same as the `.. warning::`
    directive (defined in `:context:`), but with a custom title as defined by `:title:`.
```

## Custom literal include extension for Sphinx

Similar to the `.. literalinclude::` directive, but instead of including the content of
an entire file (or defining line numbers), it includes dynamically generated data.

### Example

In **conf.py** declare the extension option `custom_literalincludes`:

```python
custom_literalincludes = {
    "directive-argument": dynamically_generated_data,
}
```

The `dinamically_generated_data` content can be anything from properties of an imported
module or the return of a function and always have to be of type str (string).

In the .rst files use like follows:

```rst
.. custom-literalinclude:: directive-argument
```

## docopt docstrings extension for Sphinx.

Similar to the custom literal include extension (`.. custom-literalinclude::` directive), but it slightly "highlights" the code.

### Example

In **conf.py** declare the extension option `docopt_docstrings`:

```python
docopt_docstrings = {
    "directive-argument": dinamically_generated_data,
}
```

The `dinamically_generated_data` content can be anything from properties of an imported
module or the return of a function and always have to be of type str (string).

In the .rst files use like follows:

```rst
.. docopt-docstring:: directive-argument
```
