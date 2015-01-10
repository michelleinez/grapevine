from flask import Flask, render_template, request, url_for
app = Flask(__name__,static_url_path='/static')

@app.route('/')
def render(name=None):
    render = render_template('./childtemplate.html', name=name)
    print render
    return render

if __name__ == '__main__':
	app.debug = True
	app.run('0.0.0.0')

