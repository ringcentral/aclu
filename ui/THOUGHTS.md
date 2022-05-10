# Thoughts While Developing the UI Package

## Preamble

What I'm writing here arguably belongs in the wiki for this rpo.
However, this being an open source project, and the wiki not necessairly included in a fork, I decided to add my wanderings directly to the repo.

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
After May 2017, I became fully dependent on accessible UIs and learned what it meant to be marginalized.
So, time to learn to build accessible UIs myself.

As I was learning to code using a screen reader, I was liking Python more and more.
I found it to be cleaner and more intutive than JavaScript with that crazy indentation requirement strongly encouraging me to break down code into smaller chunks.
But when I wanted to do anything remotely complex in a web environment, my only real options involved lots of JavaScrip, including backends based on Node.js.
I'm sure I could use Python on the back end and React for the UI, but why?  So much already exists to bootstrap a React front end with a Node.js backend. 

I learned about a project that was very intentionally back end agnostic,
[HTMX](https://htmx.org).