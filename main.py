from multiprocessing.resource_sharer import stop
import cv2 as cv
import pyautogui
from src.rangeColorsConst import *
import src.colorProcessor as colorProcessor

#Variavel de controle para nao clicar no mouse sempre que sua cor for identificada
coldown = 0

#Captura de altura e largura do monitor onde o codigo está rodando
alturaMonitor, larguraMonitor = pyautogui.size()

#Seleção da primeira camera que o dispositivo esta rodando
camera = cv.VideoCapture(1, cv.CAP_DSHOW)

#Variavel de controle para fechar o programa por cor
stop = False

while True:
    #Leitura da imagem da camera, pegando o segundo valor que retorna da funcao
    frame = camera.read()[1]

    #Flipar o frame, para que o movimento da cor para esquerda e direita não fique invertido
    frame = cv.flip(frame, 1)
    
    #Greenimensionamento da camera para o tamanho do monitor
    #Para que o mouse consiga ser movimentado por toda a tela
    frame = cv.resize(frame, (alturaMonitor, larguraMonitor), interpolation=cv.INTER_CUBIC)   

    #Conversao da imagem de BGR para HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    contornosBlue = colorProcessor.findContorsWithRangeColor(hsv, frame, lowerBlue, upperBlue)
    contornosRed = colorProcessor.findContorsWithRangeColor(hsv, frame, lowerRed, upperRed)
    contornosGreen = colorProcessor.findContorsWithRangeColor(hsv, frame, lowerGreen, upperGreen)
    contornosYellow = colorProcessor.findContorsWithRangeColor(hsv, frame, lowerYellow, upperYellow)
    
    #Passar por todos os contornos identificados para o Azul
    for contorno in contornosBlue:
        #Calcular a area do contorno atual
        area = cv.contourArea(contorno)

        #Se esse contorno tiver uma area maior de 1200 px²
        if area > 1200:
            #Identifica a posição que fica o primeiro pixel do contorno
            (x,y,w,h) = cv.boundingRect(contorno)

            #Calculo para saber o ponto central da area do contorno
            x = (x + x+w) //2
            y = (y + y+h) // 2

            #Move o mouse para a posicao identificada
            pyautogui.moveTo(x, y)    

    for contorno in contornosGreen:
        area = cv.contourArea(contorno)

        if area > 1200 and coldown > 15:
            #Clicara o botão esquerdo do mouse
            pyautogui.click(button="left")
            #Zera o coldown, para nao clicar novamente por um tempo
            coldown = 0    

    for contorno in contornosRed:
        area = cv.contourArea(contorno)

        if area > 1200 and coldown > 15:
            #Clicara o botão direito do mouse
            pyautogui.click(button="right")

            coldown = 0    

    #Se a cor amarela for identificada, o programa fechará
    for contorno in contornosYellow:
        area = cv.contourArea(contorno)

        if area > 1200:
            stop = True

    #Mostra o frame capturado da camera
    cv.imshow('coisa', frame)

    #Faz uma leitura das teclas pressionadas de 30 em 30 milisecs
    key = cv.waitKey(30)

    #Se a tecla pressionada for o 'Esc', para o loop
    if key == 27 or stop:
        break

    #Se o coldown for maior que 15, nao e mais necessario incrementar
    if coldown <= 15:
        coldown += 1

#Forca a destruicao de todas as janelas abertas pelo algoritmo
cv.destroyAllWindows()