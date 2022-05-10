# ui 

TL;DR - Python code and jinja2 templates to create accessible HTML.

## Motivation

The UI package comes from a desire to generate HTML that is accessible by default.
Using jinja2 macros with properties supplied by the application, HTML elements of arbitrary complexity can be created dynamically.
With those elements, extending the base.html template, and data obtained from any available resource, and application can dynamically render HTML documents.

I wanted to keep track of my thoughts during the evolution of this project especially background on some of the decisions and approaches.
To not clutter the README with my ramblings, I created a 
[separate md file for those thoughts.](THOUGHTS.md)

### As Is or Customize

An application can override any part of the UI templates by creating its own templates directories, creating templates in that directory, then passsing that directory to the initEnv function.
The jinja2 FileSystemLoader will search an ordered list of directories for a given template, returning the first one found.
By adding the local templates directory to the jinja environment, templates in the local directory will override templates with the same name in the UI templates directory.

## Properties (props) Data

If a template uses any data to generate the HTML, that data is passed in as a properties object.
The name of the object isn't set though "props" seems common.
The props object is created by the application using its data.
The template expects the props object to have a certain form, defined by how the data is accessed in the template.
I suppose you could argue the template accesses the data based on its form as created by the application.
considering we're trying to build generic HTML elements though, it will be the template defining the structure of the props object.
So how does the application know the format of props?

### Elements - Properties Data Classes

For each UI template macro requiring props data, there is a corresponding class defined in the UI package to generate that data.
Each class interface is specific to the macro using it, but abstract enough to keep the application from being tightly coupled to a template.

## Getting Started

Above it is mentioned the user can create a local templates directory and pass that to initEnv to override templates in the UI package.
In fact, the user MUST create a local templates directory and pass that to initEnv.
Okay, it doesn't have to be a local directory, the directory can be anywhere accessible to the application.
The application defines its own template(s) there and uses its own templates along with those provided by the UI pakcage to generate accessible HTML for the application.
There is a base.html template in the UI an application can extend using the jinja2 extends mechanism.

## References

If you underdstand jinja2, you will likely find the UI package easy to use.
See [jinja2 template designer documentation](https://jinja.palletsprojects.com/en/latest/templates/)
for how to write jinja2 templates.

## Examples

See the 
[uiTest package](../uiTest/)
package for examples of using the ui package.