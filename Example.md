Title: My Example Slide Stack
Author: Seppe vanden Broucke
slide-theme: times
code-theme: borland

# Markdown Slides

---

# Welcome

This example slide stack illustrates the different functionality of the Markdown slides editor.

The rationale behind developing this basically boils down to me getting increasingly fed up by PowerPoint. As such, I wanted an editor which allowed me to:

- Author slides using Markdown
- Basic theming support focusing more on content than beauty
- Support for Markdown extensions. Mainly tables, Graphviz and math
- Support to deal with image placement, deliberately simple
- Export to PDF support and a simple presentation mode

---

# Alternatives

I considered various HTML/CSS/JS based alternatives such as [Reveal](https://revealjs.com/) and [WebSlides](https://webslides.tv/), but those focus too much on HTML authoring and beauty.

I also heavily used [Marp](https://yhatt.github.io/marp/) in the past, but wanted an alternative since Marp is going full on Node.js nowadays and doesn't support all the functionality I wanted. Nevertheless, a lot of the CSS code was directly taken and modified from Marp -- so strong shoutout to this project!

The following slides highlight the different features of the editor.

---

# Basic Markdown support

Basic Markdown support is available, together with *all* styling **options** you'd normally expect. Slides are separated using a horizontal ruler: `---`.

- Bullet lists are of course a staple of any presentation and hence provided as well

A typograhic extension provides "smart quotes" and -- nice looking -- dashes.

`pygments` provides the code highlighting part:

```python
# Reasonable good looking code
my_list [x**2 for x in range(4)]
```

MathJax provides the math rendering functionality:

- A formula: \(\sum_{x}^{x=k} x^2\)
- Note that dollar sign formula notation is not supported

---

> This slide only has a blockquote

---

# Tables

Support for Markdown tables is provides as well:

| Tables        | Are               | Handy         |
| ------------- |:-----------------:| -------------:|
| Left aligned  | Center aligned    | Right aligned |
| 88            | \[X=\frac{Z}{Y}\] | $12           |
| Background    | alternating       | colors        |

---

# GraphViz

Graphviz diagrams can be rendered as well using `dot` or `neato`:

{% dot attack_plan.svg
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
        Earth -> Moon
        Mars -> Venus
    }
%}

---

# HTML support: inline tags

I've come to terms with the fact that HTML cannot be fully avoided (even though I don't mind it so much for small formatting changes). However, to make the formatting a bit easier, "curly-brace" statements can be used to put down simple inline tags:

[This is *some text* wrapped in a `mark` tag]{/mark}

[Another line wrapped in a `u` tag]{/u}

[Other attributes can be set as well, such as classes, e.g. this line has the `c` class]{.c}

And this works in [the middle]{/del} of a paragraph as well

---

# HTML support: blocks

In case you want to include formatted blocks of HTML, you can use the `::: {}` notation:

::: { style="color: red; border: 1px solid black; padding: 12px;" .nomargin }
This complete div block will be colored red and have a border
:::

---

# Multiple columns

The block notation can also be used to make double column slides. Note that the block parsing allows to only provide a single CSS class name as a shorthand, e.g. `::: col-left`:

::: col-left
This text is placed in the first column
:::

::: col-right
This text is placed in the second column
:::

---

# Images

Image positioning is by far the most annoying thing to get right. As such, the alt attribute can be used to provide some sizing and other guidelines, e.g. by using `s50%` for sizing and `o30%` for opacity:

![s50% o30%](//blog.macuyiko.com/images/avatar.jpg)

---

# Images (continued)

Images can also be positioned on the `left`, `right`, or `center`:

![s50% o30% center](//blog.macuyiko.com/images/avatar.jpg)

![s50% o30% left](//blog.macuyiko.com/images/avatar.jpg)

Note that left uses floats, so text will be placed to the right of the image.

---

# Images (continued)

In many cases, you want to set a caption for an image. To do so, an alternative syntax can be utilized, similar to the inline HTML blocks:

```
![](image location){.fright .mleft .w20 caption="Caption comes here"}
```

This also allows positioning on the left, right and center. Note that captions can be Markdown formatted to provide simple formatting (like links and bold text), though all extensions are disabled

![](//blog.macuyiko.com/images/avatar.jpg){.fleft .w20 caption="This is the **first** image"}

![](//blog.macuyiko.com/images/avatar.jpg){.fright .w20 caption="This is the **second** image"}

---

# Images (continued)

In most cases, you'll want to use this to center an image with a caption:

![](//blog.macuyiko.com/images/avatar.jpg){.center .w20 caption="A simple centered image with a caption"}

For more complex use cases, it's advised to resort to custom HTML blocks and your CSS styling, or use the `<figcaption>` tag.

---

# Backgrounds

Full slide backgrounds (like on this slide) can be set with the `bg` alt property. `fit` and custom opacities can be added here as well. Use `original` to remove the default opacity.

![bg](https://blog.macuyiko.com/images/backgrounds/noita.jpg)

---

# Meta information

Following the Markdown meta information extension, it's recommended to add in a series of meta tags at the beginning of each file as follows:

```
Title: My Example Slide Stack
Author: Seppe vanden Broucke
Date: 2019-07-04
pages: allbutfirst
footer: My Example Slide Stack
slide-theme: times
code-theme: borland
```

You can add as many meta statements as you want, though some will be picked up by the renderer:

- `pages` indicates whether you want page numbers. Possible values are `all`, `allbutfirst` and `none`
- `footer` indicates that you want to include a footer
- `slide-theme` and `code-theme` indicate which CSS themes you want to use for the slides and code highlighting

---

# Meta information (continued)

The defaults above work well for my setting, though I might change extend this a bit more in the future. Possible other meta tags to include would be:

- `background-color` to override the slide background color
- Allow to include more than one CSS style sheet
- Slide sizes to change the default slide size (see later)

Though generally I'd recommended to just create a new single theme style sheet to make your customizations there.

---

# Hotkeys and icons

The interface is currently very sparse by design and only provides the following:

- 📺 (F11): go into presenter mode
- 🔍 (ctrl+v): switch view between slide list (all), slide list (single slide following the cursor), and a document view
- 🖨️ (ctrl+p):open the current view in a popup and invoke a print dialog
- 📄 (ctrl+l): create a new presentation
- 💾 (ctrl+s): save the presentation
- 📂 (ctrl+o): open a Markdown file

Note that the editor doesn't warn when you're overriding existing files or you have any unsaved changes. This might become better in the future. The hotkey library I'm using also doesn't like to play along with the editor pane that much, so you probably first have to click in the title bar.

Note that the file name can be changed by editing it in the title bar above.

---

# Presenting

In the presenter mode, you can use `left`, `right`, `up`, `down`, `home`, `end` to move from slide to slide. Press F11 in the popup window to go full screen (i.e. just use your browser's full screen mode).

Click events are **not** captured, as I might want to use the mouse to interact with frames, open links, ... (and my pointer sends keyboard events anyway).

---

# Printing

Basically, this assumes you're going to want to print the current view to a PDF. I had hoped that since the last time I tried getting a good lucking custom-sized book using CSS, browsers would have evolved to the point where support for this had gotten better and I wouldn't have to resort to things like [wkhtmltopdf](https://wkhtmltopdf.org/) or [Bindery](https://evanbrooks.info/bindery/). Sadly, browsers haven't evolved that much, and at the moment only Chrome somewhat understood what I was trying to do (Opera is also supposed to have relatively good support).

This being said, Chrome is still extremely picky about what you try to throw into a `@page` directive. Using variables doesn't seem to work correctly, using both sizes and `landscape` doesn't work. Using anything other than inches is almost sure to fail. Trying to create different page "types" (as I only want to print the slide list view using a custom page size but not the normal document view) doesn't work.

---

# Slide sizes

The default slide size is 16:9.

There's currently not a very easy way to change this except to dig into the `<style>` tag in the `preview.html` file and change it over there. I might think about adding some additional meta statements for this later on, though I haven't found a strong reason to do so yet.
