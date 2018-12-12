% rebase('osnova')

<h1 class="title">Pozdravljeni na strani filmov. Na voljo vam je:</h1>

<ul>
% for desetletje, url in desetletja:
    <li>
        <a href="{{ url }}">
            Najboljši filmi desetletja {{ desetletje }}–{{ desetletje + 9}}
        </a>
    </li>
% end
</ul>
