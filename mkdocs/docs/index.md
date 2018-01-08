![RfB](images/renderman_for_blender.png "RenderMan for Blender")

# Introduction

This is the home of the "RenderMan for Blender" addon for Renderman 21.5 and beyond. The addon is a free way to try and learn how to use Pixar's RenderMan rendering software with the Blender CGI solution. The addon can be used for commercial and non commercial releases of RenderMan Pro Server. If you're just getting started, please take a look at the links below.

!!! Tip "Please note!"
    **RenderMan for Blender** _is developed by a small, dedicated group of professionals and weekend warriors working mostly in their spare time. Sometimes we move fast, sometimes not. As a result the documentation on new features may be incomplete, or missing entirely at first. We'll get it in eventually._

## Sample Shell Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the <-- -->  live-reloading docs server.
* `mkdocs build` - Build \\(4\times4\\) matrix the ==documentation== site.
* `mkdocs help` - Print this ~~help~~ message.
* `kjdkfj kjdhsfksdh` H~2~O mfdgkhkh

## Definition List

Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.

Term 1
:   This is a definition with two paragraphs. Lorem ipsum
    dolor sit amet, ++ctrl+alt+delete++ consectetuer adipiscing elit.
    hendrerit mi posuere lectus.

    Vestibulum enim wisi, viverra nec, fringilla in, laoreet
    vitae, risus.

    Second definition for term 1, also <-- --> wrapped in a paragraph
    because of the blank line preceding it.

Term 2
:   This definition has a code block, a blockquote and a list.

        code block.

    > block quote
    > on two lines.

    1.  first list item
    2.  second list item

## Project layout
    :::yaml
    mkdocs.yml      # The configuration file.
    docs/
      index.md      # The documentation homepage.
      ...           # Other markdown pages, images and other files.

## Progressbar

[=0% "0%"]
[=5% "5%"]
[=25% "25%"]
[=45% "45%"]
[=65% "65%"]
[=85% "85%"]
[=100% "Finished"]

## Progressbars Thin

[=0%]{: .thin}
[=5%]{: .thin}
[=25%]{: .thin}
[=45%]{: .thin}
[=65%]{: .thin}
[=85%]{: .thin}
[=100%]{: .thin}


## Footnotes
Footnotes[^1] have a label[^@#$%] and `pygmentize -S default -f html -a codehilite > styles.css` the ^^footnote's^^ content.

## Shell commands
    :::bash
    echo "Hello World mal wieder!" $variable

--8<-- "index_m1.md"

## With linenumbers
    #!/bin/bash
    echo "Hello World!" $variable

## Codehilight
    #!/bin/python
    def fn():
        pass

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%".

## A Task list
* [x] Lorem "ipsum" dolor "sit amet", consectetur 'adipiscing' elit
* [x] Nulla lobortis egestas semper
* [x] Curabitur elit nibh, HTML euismod ++ctrl+print+"&Uuml;"++ et ullamcorper at, iaculis feugiat est
* [ ] Vestibulum convallis sit amet nisi a tincidunt
    * [x] In hac habitasse platea dictumst
    * [x] In scelerisque nibh ´non dolor´ mollis congue sed et metus
    * [x] Sed egestas felis quis elit dapibus, ac aliquet turpis mattis
    * [x] Praesent sed risus massa
* [ ] Aenean pretium efficitur erat, `donec` pharetra, ligula non scelerisque
* [ ] Nulla vel eros venenatis, imperdiet enim id, faucibus nisi

## A Table
First Header | Second Header | Third Header
:------------ | :-------------: | -----------:
Content Cell | Content Cell  | Content Cell
Content Cell | Content Cell  | Content Cell

!!! Warning "Warning!"
    _Qualifier_: warning, caution, attention

!!! Note "Note!"
    _Qualifier_: note, seealso

!!! Summary "Summary!"
    _Qualifier_: summary, tldr

!!! Error "Error!"
    _Qualifier_: danger, error

!!! Tip "Tip"
    _Qualifier_: tip, hint, important

!!! Success "Success!"
    _Qualifier_: success, check, done

!!! Bug "Bug!"
    _Qualifier_: bug, hint, important
    $$
    \begin{aligned}
    x & = {-b \pm \sqrt{b^2-4ac} \over 2a} \cr\cr
    E(\mathbf{v}, \mathbf{h}) & = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
    \end{aligned}
    $$

!!! Failure "Failur!"
    _Qualifier_: failure, fail, missing

Here is some code: `#!js function pad(v){return ('0'+v).split('').reverse().splice(0,2).reverse().join('')}`.

The mock shebang will be treated like text here: `#!js var test = 0;`

## And some python code
```python
def fn():
    pass
```
## Math with Katex

### Inline style
When $a^2 + b^2 = c^2$, then $c$ solves to $\sqrt{a^2 + b^2}$

### Block style

$$
\begin{aligned}
x & = {-b \pm \sqrt{b^2-4ac} \over 2a} \cr\cr
E(\mathbf{v}, \mathbf{h}) & = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
\end{aligned}
$$

### Here are some more equations:

$$
\begin{aligned}
    p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \cr\cr
    p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
\end{aligned}
$$

### Sequence Diagram Example

```sequence
Title: Here is a title
A->B: Normal line
B-->C: Dashed line
C->>D: Open arrow
D-->>A: Dashed open arrow
```

### Flow Chart Example

```flow
st=>start: Start:>http://www.google.com[blank]
e=>end:>http://www.google.com
op1=>operation: My Operation
sub1=>subroutine: My Subroutine
cond=>condition: Yes
or No?:>http://www.google.com
io=>inputoutput: catch something...

st->op1->cond
cond(yes)->io->e
cond(no)->sub1(right)->op1
```

### RaphaelJS Example

--8<-- "index_rjs01.md"


### Emojis

:smile: :heart: :thumbsup:

