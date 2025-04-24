from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Configuração das pastas de upload
if os.environ.get('RENDER'):
    UPLOAD_FOLDER = '/opt/render/project/src/uploads'
else:
    UPLOAD_FOLDER = os.path.abspath('uploads')

FOTOS_FOLDER = os.path.join(UPLOAD_FOLDER, 'fotos')
VIDEOS_FOLDER = os.path.join(UPLOAD_FOLDER, 'videos')

# Criar as pastas se não existirem
os.makedirs(FOTOS_FOLDER, exist_ok=True)
os.makedirs(VIDEOS_FOLDER, exist_ok=True)
os.chmod(UPLOAD_FOLDER, 0o777)
os.chmod(FOTOS_FOLDER, 0o777)
os.chmod(VIDEOS_FOLDER, 0o777)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def apagar_arquivo(caminho_arquivo):
    # 12 horas em segundos = 12 * 60 * 60 = 43200 segundos
    time.sleep(43200)  
    try:
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)
            print(f"Arquivo apagado após 12 horas: {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao apagar arquivo: {str(e)}")

@app.route('/uploads/fotos/<filename>')
def foto_file(filename):
    return send_from_directory(FOTOS_FOLDER, filename)

@app.route('/uploads/videos/<filename>')
def video_file(filename):
    return send_from_directory(VIDEOS_FOLDER, filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/telegram')
def telegram():
    return render_template('telegram.html')

@app.route('/salvar_midia', methods=['POST'])
def salvar_midia():
    response = {'success': False, 'message': '', 'path': ''}
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                # Limpa fotos antigas do mesmo IP para evitar duplicação
                ip = request.remote_addr
                for arquivo in os.listdir(FOTOS_FOLDER):
                    if ip in arquivo:
                        try:
                            os.remove(os.path.join(FOTOS_FOLDER, arquivo))
                        except:
                            pass
                
                nome_foto = f"{ip}_{timestamp}.jpg"
                caminho_foto = os.path.join(FOTOS_FOLDER, nome_foto)
                foto.save(caminho_foto)
                response['success'] = True
                response['path'] = f'/uploads/fotos/{nome_foto}'
                thread_foto = threading.Thread(target=apagar_arquivo, args=(caminho_foto,))
                thread_foto.daemon = True
                thread_foto.start()
                
        if 'video' in request.files:
            video = request.files['video']
            if video.filename != '':
                # Limpa vídeos antigos do mesmo IP para evitar duplicação
                ip = request.remote_addr
                for arquivo in os.listdir(VIDEOS_FOLDER):
                    if ip in arquivo:
                        try:
                            os.remove(os.path.join(VIDEOS_FOLDER, arquivo))
                        except:
                            pass
                            
                nome_video = f"{ip}_{timestamp}.webm"
                caminho_video = os.path.join(VIDEOS_FOLDER, nome_video)
                video.save(caminho_video)
                response['success'] = True
                response['path'] = f'/uploads/videos/{nome_video}'
                thread_video = threading.Thread(target=apagar_arquivo, args=(caminho_video,))
                thread_video.daemon = True
                thread_video.start()
                
        response['message'] = 'Mídia salva com sucesso!'
    except Exception as e:
        response['message'] = f'Erro ao salvar mídia: {str(e)}'
    
    return response

@app.route('/fotos')
def listar_fotos():
    fotos = os.listdir(FOTOS_FOLDER)
    return render_template('fotos.html', fotos=fotos)

@app.route('/videos')
def listar_videos():
    videos = os.listdir(VIDEOS_FOLDER)
    return render_template('videos.html', videos=videos)

if __name__ == '__main__':
    app.run(debug=True)
