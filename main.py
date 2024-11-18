import sys
import os
import random
import base64
import json
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
import cv2
import numpy as np

class Backend(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_a_path = ""
        self.image_b_path = ""
        self.digitais_folder = os.path.join(os.getcwd(), "digitais")
        print(f"Digitais folder: {self.digitais_folder}")
        self.main_window = parent

    @pyqtSlot()
    def loadThumbnails(self):
        """Carrega as miniaturas das digitais disponíveis."""
        print("Carregando miniaturas...")
        if os.path.exists(self.digitais_folder):
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
            images = [file for file in os.listdir(self.digitais_folder)
                      if os.path.splitext(file)[1].lower() in image_extensions]
            print(f"Encontradas {len(images)} imagens.")
            for image in images:
                filepath = os.path.join(self.digitais_folder, image)
                filepath = filepath.replace('\\', '/')
                print(f"Processando imagem: {filepath}")
                img = cv2.imread(filepath, cv2.IMREAD_COLOR)
                if img is None:
                    print(f"Erro ao carregar a imagem: {filepath}")
                    continue
                img = cv2.resize(img, (150, 150))
                _, buffer = cv2.imencode('.png', img)
                img_base64 = base64.b64encode(buffer).decode('utf-8')
                img_data = f"data:image/png;base64,{img_base64}"
                escaped_filepath = filepath.replace('"', '\\"')
                self.main_window.view.page().runJavaScript(f'addThumbnail("{img_data}", "{escaped_filepath}")')
        else:
            print("A pasta 'digitais' não existe.")

    @pyqtSlot()
    def processImages(self):
        """Processa as imagens selecionadas e calcula a similaridade."""
        print("Processando imagens...")
        if not self.image_a_path or not self.image_b_path:
            self.main_window.view.page().runJavaScript('displayResult("Por favor, selecione ambas as imagens.", "red");')
            # Reabilitar o botão "CALCULAR"
            self.main_window.view.page().runJavaScript('enableCalculateButton();')
            print("Ambas as imagens não estão selecionadas.")
            return

        # Carregar as imagens
        img1 = cv2.imread(self.image_a_path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(self.image_b_path, cv2.IMREAD_GRAYSCALE)

        if img1 is None or img2 is None:
            self.main_window.view.page().runJavaScript('displayResult("Erro ao carregar as imagens.", "red");')
            # Reabilitar o botão "CALCULAR"
            self.main_window.view.page().runJavaScript('enableCalculateButton();')
            print(f"Erro ao carregar as imagens: A={self.image_a_path}, B={self.image_b_path}")
            return

        # Redimensionar para o mesmo tamanho
        height, width = img1.shape[:2]
        img2 = cv2.resize(img2, (width, height))

        # # Processamentos morfológicos
        # kernel = np.ones((4, 4), np.uint8)
        # img1_processed = cv2.morphologyEx(img1, cv2.MORPH_OPEN, kernel)
        # img1_processed = cv2.morphologyEx(img1_processed, cv2.MORPH_CLOSE, kernel)
        # img2_processed = cv2.morphologyEx(img2, cv2.MORPH_OPEN, kernel)
        # img2_processed = cv2.morphologyEx(img2_processed, cv2.MORPH_CLOSE, kernel)

        # # Comparação das imagens processadas
        # correlation = np.corrcoef(img1_processed.ravel(), img2_processed.ravel())[0, 1]
        # similarity_threshold = 0.8

        # print(f"Coeficiente de correlação: {correlation}")

        # if correlation > similarity_threshold:
        #     result_text = "CORRESPONDÊNCIA ENCONTRADA"
        #     result_color = "green"
        # else:
        #     result_text = "SEM CORRESPONDÊNCIA"
        #     result_color = "red"

        # # Atualizar o resultado na interface
        # self.main_window.view.page().runJavaScript(f'displayResult("{result_text}", "{result_color}");')
        # print(f"Resultado da similaridade: {result_text}")

        # # Comparação usando ORB
        # orb = cv2.ORB_create()
        # kp1, des1 = orb.detectAndCompute(img1_processed, None)
        # kp2, des2 = orb.detectAndCompute(img2_processed, None)

        # if des1 is None or des2 is None:
        #     self.main_window.view.page().runJavaScript('displayResult("Não foi possível encontrar keypoints em uma das imagens.", "red");')
        #     # Reabilitar o botão "CALCULAR"
        #     self.main_window.view.page().runJavaScript('enableCalculateButton();')
        #     print("Não foi possível encontrar keypoints em uma das imagens.")
        #     return

        # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # matches = bf.match(des1, des2)
        # matches = sorted(matches, key=lambda x: x.distance)

        # print(f"Encontradas {len(matches[:20])} correspondências.")

        # img_matches = cv2.drawMatches(img1_processed, kp1, img2_processed, kp2, matches[:20], None,
        #                               flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        # _, buffer = cv2.imencode('.png', img_matches)
        # img_base64 = base64.b64encode(buffer).decode('utf-8')
        # img_data = f"data:image/png;base64,{img_base64}"

        # # Serializar img_data usando json.dumps para garantir escapamento correto
        # img_data_json = json.dumps(img_data)

        # # Exibir correspondências na interface
        # self.main_window.view.page().runJavaScript(f'displayMatches({img_data_json});')
        # print("Correspondências exibidas na interface.")

        # # Chamar a função JavaScript para esconder elementos e mostrar correspondências
        # self.main_window.view.page().runJavaScript('onProcessImagesComplete();')

        # Processamentos morfológicos
        kernel = np.ones((4, 4), np.uint8)

        # Abertura (Opening)
        img1_opening = cv2.morphologyEx(img1, cv2.MORPH_OPEN, kernel)
        img2_opening = cv2.morphologyEx(img2, cv2.MORPH_OPEN, kernel)

        # Fechamento (Closing)
        img1_closing = cv2.morphologyEx(img1_opening, cv2.MORPH_CLOSE, kernel)
        img2_closing = cv2.morphologyEx(img2_opening, cv2.MORPH_CLOSE, kernel)

        # Gradiente Morfológico
        img1_gradient = cv2.morphologyEx(img1_closing, cv2.MORPH_GRADIENT, kernel)
        img2_gradient = cv2.morphologyEx(img2_closing, cv2.MORPH_GRADIENT, kernel)

        # Top Hat
        img1_tophat = cv2.morphologyEx(img1_closing, cv2.MORPH_TOPHAT, kernel)
        img2_tophat = cv2.morphologyEx(img2_closing, cv2.MORPH_TOPHAT, kernel)

        # Black Hat
        img1_blackhat = cv2.morphologyEx(img1_closing, cv2.MORPH_BLACKHAT, kernel)
        img2_blackhat = cv2.morphologyEx(img2_closing, cv2.MORPH_BLACKHAT, kernel)

        # Função para comparar duas imagens e calcular o coeficiente de correlação
        def compare_images(imgA, imgB):
            return np.corrcoef(imgA.ravel(), imgB.ravel())[0, 1]

        # Comparação das imagens processadas
        correlation_opening = compare_images(img1_opening, img2_opening)
        correlation_closing = compare_images(img1_closing, img2_closing)
        correlation_gradient = compare_images(img1_gradient, img2_gradient)
        correlation_tophat = compare_images(img1_tophat, img2_tophat)
        correlation_blackhat = compare_images(img1_blackhat, img2_blackhat)

        # Média das correlações para decisão final
        average_correlation = (correlation_opening + correlation_closing + correlation_gradient + correlation_tophat + correlation_blackhat) / 5
        print(f"Coeficiente de correlação médio: {average_correlation}")

        # Limiar de similaridade
        similarity_threshold = 0.5  # Ajuste conforme necessário

        if average_correlation > similarity_threshold:
            result_text = "CORRESPONDÊNCIA ENCONTRADA"
            result_color = "green"
        else:
            result_text = "SEM CORRESPONDÊNCIA"
            result_color = "red"

        # Atualizar o resultado na interface
        self.main_window.view.page().runJavaScript(f'displayResult("{result_text}", "{result_color}");')
        print(f"Resultado da similaridade: {result_text}")

        # Comparação usando ORB nas imagens após fechamento
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1_closing, None)
        kp2, des2 = orb.detectAndCompute(img2_closing, None)

        if des1 is None or des2 is None:
            self.main_window.view.page().runJavaScript('displayResult("Não foi possível encontrar keypoints em uma das imagens.", "red");')
            # Reabilitar o botão "CALCULAR"
            self.main_window.view.page().runJavaScript('enableCalculateButton();')
            print("Não foi possível encontrar keypoints em uma das imagens.")
            return

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        print(f"Encontradas {len(matches[:20])} correspondências.")

        img_matches = cv2.drawMatches(img1_closing, kp1, img2_closing, kp2, matches[:20], None,
                                      flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        _, buffer = cv2.imencode('.png', img_matches)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        img_data = f"data:image/png;base64,{img_base64}"

        # Serializar img_data usando json.dumps para garantir escapamento correto
        img_data_json = json.dumps(img_data)

        # Exibir correspondências na interface
        self.main_window.view.page().runJavaScript(f'displayMatches({img_data_json});')
        print("Correspondências exibidas na interface.")

        # Chamar a função JavaScript para esconder elementos e mostrar correspondências
        self.main_window.view.page().runJavaScript('onProcessImagesComplete();')

    @pyqtSlot(str)
    def selectImageB(self, filepath):
        """Seleciona a imagem B e exibe na interface."""
        print(f"Caminho recebido antes da normalização: {filepath}")
        # Normalizar o caminho para corrigir separadores
        filepath = os.path.normpath(filepath)
        print(f"Caminho após normalização: {filepath}")
        self.image_b_path = filepath
        img = cv2.imread(filepath, cv2.IMREAD_COLOR)
        if img is None:
            print(f"Erro ao carregar a imagem: {filepath}")
            return
        img = cv2.resize(img, (200, 200))
        _, buffer = cv2.imencode('.png', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        img_data = f"data:image/png;base64,{img_base64}"
        self.main_window.view.page().runJavaScript(f'displayImage("imageB", "{img_data}");')
        print(f"Imagem B exibida: {filepath}")

        # Limpar a mensagem de erro
        self.main_window.view.page().runJavaScript('clearResult();')

    @pyqtSlot()
    def resetApplication(self):
        """Reseta a aplicação e seleciona uma nova imagem A."""
        print("Resetando aplicação e selecionando nova imagem A.")
        # Resetar o caminho da imagem B
        self.image_b_path = ""
        # Selecionar uma nova imagem A
        self.main_window.select_random_image_a()
        print("Nova imagem A selecionada.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SISTEMA COMPARADOR DE IMPRESSÕES DIGITAIS")
        self.setGeometry(100, 100, 1600, 800)
        self.view = QWebEngineView(self)
        self.setCentralWidget(self.view)

        # Configurar o QWebChannel
        self.channel = QWebChannel()
        self.backend = Backend(parent=self)
        self.channel.registerObject('backend', self.backend)
        self.view.page().setWebChannel(self.channel)

        # Carregar o arquivo HTML
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "assets", "html", "index.html")
        self.view.load(QUrl.fromLocalFile(html_path))

        # Selecionar uma imagem aleatória para Digital A após o carregamento da página
        self.view.loadFinished.connect(self.after_load)

    def after_load(self):
        """Executa após a página HTML ser carregada."""
        self.select_random_image_a()

    def select_random_image_a(self):
        """Seleciona uma imagem aleatória para Digital A e exibe na interface."""
        print("Selecionando imagem aleatória para Digital A...")
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        digitais_folder = self.backend.digitais_folder
        if os.path.exists(digitais_folder):
            images = [os.path.join(digitais_folder, file) for file in os.listdir(digitais_folder)
                      if os.path.splitext(file)[1].lower() in image_extensions]
            if images:
                image_a_path = random.choice(images)
                self.backend.image_a_path = image_a_path
                print(f"Imagem A selecionada: {image_a_path}")
                img = cv2.imread(image_a_path, cv2.IMREAD_COLOR)
                if img is None:
                    print(f"Erro ao carregar a imagem A: {image_a_path}")
                    return
                img = cv2.resize(img, (200, 200))
                _, buffer = cv2.imencode('.png', img)
                img_base64 = base64.b64encode(buffer).decode('utf-8')
                img_data = f"data:image/png;base64,{img_base64}"
                self.view.page().runJavaScript(f'displayImage("imageA", "{img_data}");')
                print("Imagem A exibida na interface.")
            else:
                print("Nenhuma imagem encontrada na pasta 'digitais'.")
        else:
            print("A pasta 'digitais' não existe.")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()