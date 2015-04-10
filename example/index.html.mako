<html>
    <body>
        <div>hello, this is a webpage</div>
        <div>i also wrote some blog posts</div>
        <ul>
            % for post in sorted(tree['blog'].values(), key=lambda x: x['date']):
                <li>${post['date']} - <a href="${post['url']}">${post['title']}</a></li>
            % endfor
        </ul>
    </body>
</html>
