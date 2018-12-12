from bottle import get, run, template
import modeli


@get('/')
def osnovna_stran():
    return template(
        'osnovna_stran',
    )


@get('/najboljsi-filmi/')
@get('/najboljsi-filmi/<desetletje:int>/')
def najboljsi_filmi_desetletja(desetletje=2010):
    desetletje, najboljsi_filmi = modeli.najboljsi_filmi_desetletja(desetletje)
    return template(
        'najboljsi_filmi_desetletja',
        desetletje=desetletje,
        filmi=najboljsi_filmi,
    )

run(reloader=True, debug=True)
