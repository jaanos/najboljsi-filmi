<h1>Pozdravljeni na strani filmov. Na voljo vam je:</h1>

<ul>
% for desetletje in range(1920, 2020, 10):
    <li>
        <a href="/najboljsi-filmi/{{ desetletje }}/">
            Najboljši filmi desetletja {{ desetletje }}–{{ desetletje + 9}}
        </a>
    </li>
% end
</ul>

