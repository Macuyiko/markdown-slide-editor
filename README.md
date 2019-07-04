# A browser-based Markdown slide editor

The rationale behind developing this basically boils down to me getting increasingly fed up by PowerPoint. As such, I wanted an editor which allowed me to:

- Author slides using Markdown
- Basic theming support focusing more on content than beauty
- Support for Markdown extensions. Mainly tables, Graphviz and math
- Support to deal with image placement, deliberately simple
- Export to PDF support and a simple presentation mode

I considered various HTML/CSS/JS based alternatives such as [Reveal](https://revealjs.com/) and [WebSlides](https://webslides.tv/), but those focus too much on HTML authoring and beauty.

I also heavily used [Marp](https://yhatt.github.io/marp/) in the past, but wanted an alternative since Marp is going full on Node.js nowadays and doesn't support all the functionality I wanted. Nevertheless, a lot of the CSS code was directly taken and modified from Marp -- so strong shoutout to this project!

See `Example.md` for feature overview.
