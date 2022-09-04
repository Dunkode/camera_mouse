import cv2 as cv

def findContorsWithRangeColor(hsv, frame, lower, upper):
    #Faz mascara na imagem da camera, baseado nos limites do Azul
    maskBlue = cv.inRange(hsv, lower, upper)
    #Aplica a mascara no frame, para manter a cor
    bitBlue = cv.bitwise_and(frame, frame, mask=maskBlue)
    #Conversao do frame mascarado para tons de cinza
    grayBlue = cv.cvtColor(bitBlue, cv.COLOR_BGR2GRAY)
    #Acentua as bordas
    borderBlue = cv.threshold(grayBlue, 3, 255, cv.THRESH_BINARY)[1]
    #Identifica e retonra as bordas
    return cv.findContours(borderBlue, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]
    