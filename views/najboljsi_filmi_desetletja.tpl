% if filmi:
    <h1>Najboljši filmi desetletja {{ desetletje }}–{{ desetletje + 9}} so:</h1>

    <ol>
        % for naslov, leto, ocena in filmi:
            <li>{{ naslov }} ({{ leto }}), <small>{{ ocena }} / 10</small></li>
        % end
    </ol>
% else:
    <h1>V bazi nimam podatkov o filmih desetletja {{ desetletje }}–{{ desetletje + 9}}</h1>
% end
