import numpy as np
import cv2
from matplotlib import pyplot as plt

def showImage(img):
    imgMPLIB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(imgMPLIB)
    plt.show()

def showMultipleImageGrid(imgsArray, titlesArray, x, y):
    if(x < 1 or y < 1):
        print("ERRO: X e Y não podem ser zero ou abaixo de zero!")
        return
    elif(x == 1 and y == 1):
        showImageGrid(imgsArray, titlesArray)
    elif(x == 1):
        fig, axis = plt.subplots(y)
        fig.suptitle(titlesArray)
        yId = 0
        for img in imgsArray:
            imgMPLIB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            axis[yId].imshow(imgMPLIB)

            yId += 1
    elif(y == 1):
        fig, axis = plt.subplots(1, x)
        fig.suptitle(titlesArray)
        xId = 0
        for img in imgsArray:
            imgMPLIB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            axis[xId].imshow(imgMPLIB)

            xId += 1
    else:
        fig, axis = plt.subplots(y, x)
        xId, yId, titleId = 0, 0, 0
        for img in imgsArray:
            imgMPLIB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            axis[yId, xId].set_title(titlesArray[titleId])
            axis[yId, xId].imshow(imgMPLIB)
            if(len(titlesArray[titleId]) == 0):
                axis[yId, xId].axis('off')

            titleId += 1
            xId += 1
            if xId == x:
                xId = 0
                yId += 1

        fig.tight_layout(pad=0.5)
    plt.show()

def plotThreeImages():
    firstImage = cv2.imread("bin1.png")
    secondImage = cv2.imread("bin2.png")
    addedImage = cv2.add(firstImage, secondImage)
    imgTransparent = np.ones((firstImage.shape[0], firstImage.shape[1], 4), np.uint8) * 255

    #criando grid com 3 imagens, a segunda com borda replicada e a terceira com borda de espelho
    #a ultima imagem é transparente
    imgsArray = [firstImage, secondImage, addedImage, imgTransparent]
    titlesArray = ['Primeira imagem', 'Segunda imagem', 'Soma', '']
    showMultipleImageGrid(imgsArray, titlesArray, 2, 2)

def resizeImage(image, scalePercent):
    width = int(image.shape[1] * scalePercent / 100)
    height = int(image.shape[0] * scalePercent / 100)
    image = cv2.resize(image, (width, height))

    return image

def addImageOverlay(background, foreground, posX, posY, limiar):
    backH, backW, _ = background.shape
    foreH, foreW, _ = foreground.shape
    cropH, cropW = backH - foreH, backW - foreW

    posH = cropH - posY
    posW = cropW - posX

    if cropH - posH + foreH > backH:
        print("Erro: sobreposição com altura maior do que a permitida.")
        print("Posição final que altura do objeto da frente termina:", cropH - posH + foreH)
        print("Altura do fundo:", backH)
        return

    if cropW - posW + foreW > backW:
        print("Erro: sobreposição com largura maior do que a permitida.")
        print("Posição final que largura do objeto da frente termina:", cropW - posW + foreW)
        print("Largura do fundo:", backW)
        return

    #parte do cenário do fundo em que a imagem será adicionada
    crop = background[cropH - posH:backH - posH, cropW - posW:backW - posW]

    #Transformamos o foreground em imagem com tons de cinza e criamos uma máscara binária da mesma com a binarização (cv2.threshold)
    foregroundGray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
    ret, maskFore = cv2.threshold(foregroundGray, limiar, 255, cv2.THRESH_BINARY)

    #Agora aplicamos uma operação de AND binário na imagem recortada 'crop'. No caso, realizar a operação binária entre a mesma imagem não terá efeito. Só que, com a inclusão da máscara no terceiro parâmetro, os pixels pretos de maskFore serão ignorados e, portanto, ficarão escuros. Com isso temos a marcação em que vamos incluir o foreground posteriormente.
    backWithMask = cv2.bitwise_and(crop, crop, mask = maskFore)
    foreWithMask = cv2.bitwise_not(maskFore)
    foreWithMask = cv2.bitwise_and(foreground, foreground, mask = foreWithMask)

    #Faremos a composição entre 'frente' e 'fundo', compondo o foreground na imagem extraída do background.
    combinedImage = cv2.add(foreWithMask, backWithMask)

    #Adicionamos a imagem gerada no background final.
    copyImage = background.copy()
    copyImage[cropH - posH:backH - posH, cropW - posW:backW - posW] = combinedImage

    return copyImage

def addBlending(firstImage, secondImage, weight):
    mask = cv2.cvtColor(firstImage, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(secondImage, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
    copyImg = firstImage.copy()

    altura, largura = mask.shape
    for y in range(0, altura):
        for x in range(0, largura):
            if mask.item(y, x) > 0:
                finalPixelBlue = firstImage.item(y, x, 0) * (1.0 - weight) + secondImage.item(y, x, 0) * weight
                finalPixelGreen = firstImage.item(y, x, 1) * (1.0 - weight) + secondImage.item(y, x, 1) * weight
                finalPixelRed = firstImage.item(y, x, 2) * (1.0 - weight) + secondImage.item(y, x, 2) * weight

                copyImg.itemset((y, x, 0), finalPixelBlue)
                copyImg.itemset((y, x, 1), finalPixelGreen)
                copyImg.itemset((y, x, 2), finalPixelRed)

    return copyImg

def memeGeneratorWithBlending():
    atilaFeliz = cv2.imread("atila_feliz.png")
    background = cv2.imread("background.jpg")
    atilaFeliz = resizeImage(atilaFeliz, 250)
    finalImageUmAtila = addImageOverlay(background, atilaFeliz, 250, 465, 210)

    atilaBravo = cv2.imread("atila_bravo.png")
    atilaBravo = resizeImage(atilaBravo, 250)
    finalImageDoisAtilas = addImageOverlay(finalImageUmAtila, atilaBravo, 1100, 460, 240)

    finalImage = addBlending(finalImageUmAtila, finalImageDoisAtilas, 0.4)

    finalImage = cv2.putText(finalImage, 'Respeito seu argumento!', (80, 420), cv2.FONT_HERSHEY_SIMPLEX ,
                   2.5, (255, 0, 0) , 5, cv2.LINE_AA)

    finalImage = cv2.putText(finalImage, 'Burro do caralho...', (1140, 400), cv2.FONT_HERSHEY_SIMPLEX ,
                   2.5, (0, 0, 255) , 5, cv2.LINE_AA)

    showImage(finalImage)

memeGeneratorWithBlending()
