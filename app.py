from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>avalia.se</title>
        <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Quicksand', sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            .container {
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-top: 20px;
            }
            .app-list {
                width: 100%;
                max-width: 300px;
                margin-top: 20px;
            }
            .app-link {
                display: block;
                margin: 10px 0;
                padding: 15px;
                text-decoration: none;
                color: #333;
                background-color: #f0f0f0;
                border-radius: 10px;
                transition: background-color 0.3s, box-shadow 0.3s;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .app-link:hover {
                background-color: #e0e0e0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .logo {
                width: 200px;
                height: auto;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/"><img src="{{ url_for('static', filename='avalia.png') }}" class="logo"></a>
            <div class="app-list">
                <a href="/gradio_app_1" class="app-link">
                    Regressão Linear
                </a>
                <a href="/gradio_app_2" class="app-link">
                    Bens Móveis
                </a>
                <a href="/streamlit_app" class="app-link">
                    Dashboard Geoespacial
                </a>
            </div>
        </div>
    </body>
    </html>
    ''')



@app.route('/gradio_app_1')
def gradio_app_1():
    return render_template_string('''
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Quicksand', sans-serif;
                text-align: center;
            }
            iframe {
                border: none;
                width: 100%;
                height: 800px;
            }
            .logo {
                width: 200px;
                height: auto;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <iframe src="https://fschwartzer-rl-2.hf.space"></iframe>
        <a href="/"><img src="{{ url_for('static', filename="avalia.png") }}" class="logo"></a>        
    </body>
    </html>
    ''')

@app.route('/gradio_app_2')
def gradio_app_2():
    return render_template_string('''
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Quicksand', sans-serif;
                text-align: center;
            }
            iframe {
                border: none;
                width: 100%;
                height: 800px;
            }
            .logo {
                width: 200px;
                height: auto;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <iframe src="https://fschwartzer-bens-moveis-vision.hf.space"></iframe>
        <a href="/"><img src="{{ url_for('static', filename="avalia.png") }}" class="logo"></a>
    </body>
    </html>
    ''')

@app.route('/streamlit_app')
def streamlit_app():
    return render_template_string('''
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Quicksand', sans-serif;
                text-align: center;
            }
            iframe {
                border: none;
                width: 100%;
                height: 800px;
            }
            .logo {
                width: 200px;
                height: auto;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <iframe src="https://fschwartzer-geo-dash-tabs.hf.space"></iframe>
        <a href="/"><img src="{{ url_for('static', filename="avalia.png") }}" class="logo"></a>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
