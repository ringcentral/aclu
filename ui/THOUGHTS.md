# Thoughts While Developing the UI Package

## Preamble

What I'm writing here arguably belongs in the wiki for this rpo.
However, this being an open source project, and the wiki not necessarily included in a fork, I decided to add my wanderings directly to the repo.

I'm starting this thoughts experiment in May, 2022.
It's intended to be a append only file, though I might edit previous entries for clarity (and, of course, change anything that looks completely ridiculous in hindsight)
The goal though is to honestly, with humility, document the progression of an idea.

### Background

I lost my sight suddenly in May, 2017.
I had been in the software development industry (mainly telecom/VoIP) for just over 20 years.
My experience had primarily been focused on backend systems in C, C++, and some Java.
I had poked around in Python, JavaScript (with Node.js), and a bit of Ruby.
I liked to write pure HTML in vim as documentation.
I had literally no experience developing UIs and knew nothing at all about accessibility.
After May 2017, I became fully dependent on accessible UIs and learned what it meant to be thoroughly frustrated and at the whims of others.
So, time to learn to build accessible UIs myself.

As I was learning to code using a screen reader, I was liking Python more and more.
I found it to be cleaner and more intutive than JavaScript with that crazy indentation requirement strongly encouraging me to break down code into smaller chunks.
But when I wanted to do anything remotely complex in a web environment, my only real options involved lots of JavaScrip, including backends based on Node.js.
I'm sure I could use Python on the back end and React for the UI, but why?  So much already exists to bootstrap a React front end with a Node.js backend. 

I learned about a project that was very intentionally back end agnostic,
[HTMX](https://htmx.org),
which will query a backend and accept HTML elements in response to modify the DOM.
This sounded like exactly what I want.

With HTMX and this ui package, I can create server side HTML and respond with a complete document, or with an element to update the existing document in the DOM.
With accessibility built in to the ui package, a developer can use the Python classes from the ui package to build accessible applications without having a complete understanding of accessibility.
(developers ought to have at least a high level understanding of accessibility and screen readers, this ui package can help them with the detils though.)

The ui package does not exclude including JavaScript in the HTML, an app can do client side work as well.
The app developer will create the templates that use the ui package thus are welcome to use any front end technologies desired.

## And Now, the Evolution of the Story

I'll add entries here at heading level 3 with the most recent entries at the end.  The frequency will be arbitrary and each heading will include the date.

If you do start reading from the beginning, the oldest posts, while looking at the code in its latest form, you'll notice there's very little correlation.  The posts were made with regard to how the code was then.  If you're very patient and read all the posts, hopefully it will become clear why the code looks like it does now.

### 2022-05-11 - Start Simple

As of this writing, I already have some basic structure in the ui package.
There's a templates directory with  base.html with blocks for an app to extend.
The directory also contains a few html template files with macros to generate elements.
There are already classes in the elements sub package to represent headings (h1, ..., h6) and the beginning of list elements (ul, ol, dl).
When I was thinking of what to support as list items, I started thinking more generically about the class hierarchy.
That is, what should be the type of a list element?
I was also thinking about moving some functionality from templates to the Python classes.
Let's think through those points.

#### More Formatting in the Python Classes?

Currently the classes in the elements package contain the data needed to create the HTML.
A class object is passed to a template where the data is extracted and used to format the text of the HTML element.

I thought, why not just have a __repr__ or __str__ generate the text of the HTML element?
It's a lot easier to debug Python code and would make the templates cleaner.

However, it also violates the idea of keeping the data and its presentation independent.
Is that important?  After all, the classes explicitly represent data used to generate HTML elements.
Why not have the class itself generate the actual text?

As I was heading down that path, and thought of other things I might add to the classes, I realized I was starting to implelent jinja.

So, for now at least, the macros in the templates will generate the HTML text and the classes will focus on holding the data for those macros.

#### Thoughts on the Class Hierarchy

Every HTML element has an opening angle bracket and tag name, followed by an optional set of attributes.
Some attributes are global, can appear with any tag (e.g. 'id', 'class'), some are limited to certain tags or sets of tags.
And a developer can add their own attributes, e.g., data-my-favorite-colour="red no blue ahhhh".
That in mind, we need to accomodate an unknown list of attributes for an element.

The root of the class hierarchy is the BaseElement.
It has a tagName, id, and dictionary to hold an unspecified number of attributes as key value pairs.
I opted to keep the id separate as that must be unique across all elements of a document.
It could be a developer has many attributes that are the same across many elements and wants to use the same dict when creating those elements.
By enabling the specification of the id in the argument list, multiple elements can be created with the same attributes dict and different id.

When it is time to generate the attributes list as a template is being rendered, the template can access the method on the base class to get the string of attributes.
And of course any derived class can override that functionality or modify the attributes list if necessary.

#### Start Small

The last point I want to address in this post is how complex the elements can be initially.
I started thinking of this as I was creating the list elements.
What can be in a list item?
And the more general question; for any element, which elements can appear in their contents.
Searching around I ran across the live standard for HTML,
[Web Hypertext Application Technology Working Group (WHATWG)](https://whatwg.org/).
Specifically, from the sections 
[content categories at MDN](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Content_categories) and 
[more details of types of content on WHATWG](https://html.spec.whatwg.org/multipage/dom.html#kinontent), 
I realized I will need a more complicated class hierarchy than just everything extends the BaseElement.

For example, what can be part of a list item is defined based on content categories.
Same is true for table cells.

This makes me think elements need to have content categories in their derivation chain.
I'm not sure though how to work that in, or if that's really the best way to go about deciding whether an element can be contained within another element.

So, for the time being, list items will be strings or anchors.
Maybe I'll initially support lists within lists and lists within table cells.
Time will tell.

### 2022-05-17

The 11th seems so long ago, and so much has changed.  I started off with the simple plan of bailing out on Dataclasses in favor of standard Python classes.  I found I needed to implement the __init__ myself if I want to hide the tags from the higher level classes.  If I'm going to implement __init__, why use Dataclasses?

As I was removing Dataclasses and running in the REPL to unit test the changes, I realized how nice it would be if I could simply type the name of the object just created and it would give me the HTML output.  Ha, okay, I'll put that in the __repr__.  Now I really don't need Dataclasses.

Now I have __repr__ in the BaseElement that works quite well for generating HTML for derived classes.  There are a few places I have needed to override __repr__ but in general, this is working very well.

So, what about jinja?

As I think more about this, and read more about HTML, I realize I could generate HTML documents entirely from these Python classes.  By using __repr__, so each object can generate its own HTML, the objects are very composeable.  That is, I can easily have a <li> with an Anchor object as its contents.  As the ListItem object is generating its HTML, it has the contents object generate its own HTML.  Now I have an <li> element with an <a> as its content and it feels like I got most of that for free.  In fact, <li> can have a <ul> and we easily get lists within lists.

As I looked at the template, most notably the jinja macros, I realize I don't need the macros.  And, at least the way I had initially developed them, it would be much more difficult to have elements within elements.

Maybe the right answer is to use very little jinja.  Maybe just supply the base.html document to help lesss HTML technical people (myself included though becoming less so each day) get started.

I need to develop tests for the lists elements.  Maybe as I do that, how much jinja to use will be clearer.

And regarding content categories, my thoughts are now to not include that in any class hierarchy.  I was thinking if I did, I could use types to ensure elements had proper contents.  Maybe that will be useful someday.  For now I'm going to let the site developer worry about which elements are part of another's element's contents.  That is, developing correct HTML is left as an exercise for the reader (well, developer in this case).

<div>dunder scores within div __repr__</div>
<pre>duncder scores within pre __repr__</pre> 
