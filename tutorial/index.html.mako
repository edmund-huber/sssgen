---
title: Introduction to sssgen
layout: default.html.mako_layout
---

<h2>Introduction</h2>

<div>
    An <code>sssgen</code> project is a directory tree of four kinds of files:
    <ul>
        <li><code>.mako</code> files: these will be rendered using the <a href="http://www.makotemplates.org/">Mako templating engine</a>.</li>
        <li><code>.mako_layout</code> files: these are made available to <code>.mako</code> files for <a href="http://docs.makotemplates.org/en/latest/inheritance.html">layout purposes</a>.</li>
        <li>Ignored files: files that exist in the tree but won't in the output tree, for example any file beginning with <code>_</code>.</li>
        <li>Any other file is copied to the destination directory.</li>
    </ul>
</div>

<div>
    The interesting work in an <code>sssgen</code> project is done in
    <code>.mako</code> files. For example, the source to to this page is
    available at <code>tutorial/index.html.mako</code>.
</div>

<div>
    Every <code>.mako</code> template gets two variables:
    <code>page</code> and <code>tree</code>.
</div>

<h2>The <code>page</code> variable</h2>

<div>
    Here is the content of <code>page</code> for this file:
</div>

<%!
    import pprint
%>

<pre>${pprint.PrettyPrinter(indent=4).pformat(page)}</pre>

<div>
    If you look at the source for this page, you'll see that the keys
    <code>title</code> and <code>layout</code> were taken from the so-called
    "front matter" of the file. The front matter is just <a
    href="http://yaml.org/">YAML</a> placed at the beginning of the file,
    delimited by <code>---</code>. Front matter is one of four sources for the
    contents of the <code>page</code> variable:
</div>

<div>
    <code>page</code> is defined as inherited YAML + layout YAML + front matter
    YAML + intrinsic YAML. Each N+1th source of <code>page</code> keys overrides
    the Nth source.
</div>

<div>
    The first source of keys in the <code>page</code> variable is inherited
    YAML. Inherited YAML is the collected of YAML as constructed by walking
    down the directory to your file, aggregating <code>_inherit.yaml</code>
    files along the way. We don't use inherited YAML in this tutorial but it's
    very useful.
</div>

<div>
    The next source of <code>page</code> keys is the chain of layouts.  Each
    <code>.mako_layout</code> file may contain front matter, which is merged into
    <code>page</code>.
</div>

<div>
    Then comes front matter YAML.
</div>

<div>
    The final source of keys is intrinsic YAML. The <code>url</code> key is
    provided by <code>sssgen</code> itself. It gives you the URL for this file,
    relative to the root of the project.
</div>

<h2>The <code>tree</code> variable</h2>

<div>
    Here is the content of <code>tree</code> for this file:
</div>

<pre>${pprint.PrettyPrinter(indent=4).pformat(tree)}</pre>

<div>
    <code>tree</code> reflects the directory tree of the project. The leaves
    are the <code>page</code> variable for a given file. <code>tree</code> is
    useful, for example, for listing sub-contents. In the following block of
    code, we use the <code>tree</code> variable and the intrinsic YAML key
    <code>url</code> that we discussed earlier, to list Spongebob characters:
</div>

<code><%text filter="h,trim">
<ul>
    Here are my favorite Spongebob Squarepants characters:
    % for name_of_file, yaml in tree['textfiles'].items():
        <li><a href="${yaml['url']}">${name_of_file}</a></li>
    % endfor
</ul>
</%text></code>

<ul>
    Here are my favorite Spongebob Squarepants characters:
    % for name_of_file, yaml in tree['textfiles'].items():
        <li><a href="${yaml['url']}">${name_of_file}</a></li>
    % endfor
</ul>
