import numpy as np
import cv2
from matplotlib import pyplot as plt

def showImage(img):
    imgMPLIB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(imgMPLIB)
    plt.show()

def showImageGrid(img, title):
    fig, axis = plt.subplots()
    imgMPLIB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    axis.imshow(imgMPLIB)
    axis.set_title(title)
    plt.show()

def showMultipleImageGrid(imgsArray, titlesArray, x, y):
    if(x < 1 and y < 1):
        print("ERRO: X e Y não podem ser zero simultaneamente!")
        return
    elif(x == 1 or y == 1):
        showImageGrid(imgsArray[0], titlesArray[0])
    elif(x == 0):
        fig, axis = plt.subplots(y)
        fig.suptitle(titlesArray)
        axisId = 0
        for img in imgsArray:
            imgMPLIB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            axis[axisId].imshow(imgMPLIB)

            axisId += 1
    elif(y == 0):
        fig, axis = plt.subplots(1, x)
        fig.suptitle(titlesArray)
        axisId = 0
        for img in imgsArray:
            imgMPLIB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            axis[axisId].imshow(imgMPLIB)

            axisId += 1
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

def plotSingleImage():
    #criando grid com a imagem original apenas
    imgOriginal = cv2.imread("ada.jpg")
    showImageGrid(imgOriginal, "Foto da Ada")

def plotTwoImageHorizontal():
    imgOriginal = cv2.imread("ada.jpg")
    imgReplicate = cv2.copyMakeBorder(imgOriginal, 100, 100, 100, 100, cv2.BORDER_REPLICATE)

    #criando grid com 2 imagens, a segunda com borda replicada
    imgsArray = [imgOriginal, imgReplicate]
    titlesArray = 'Imagem Original e Imagem com Borda Replicada'
    showMultipleImageGrid(imgsArray, titlesArray, 0, 2)
    #showMultipleImageGrid(imgsArray, titlesArray, 2, 0)

def plotTwoImageVertical():
    imgOriginal = cv2.imread("ada.jpg")
    imgReplicate = cv2.copyMakeBorder(imgOriginal, 100, 100, 100, 100, cv2.BORDER_REPLICATE)

    #criando grid com 2 imagens, a segunda com borda replicada
    imgsArray = [imgOriginal, imgReplicate]
    titlesArray = 'Imagem Original e Imagem com Borda Replicada'
    showMultipleImageGrid(imgsArray, titlesArray, 2, 0)

def plotThreeImages():
    imgOriginal = cv2.imread("ada.jpg")
    imgReplicate = cv2.copyMakeBorder(imgOriginal, 100, 100, 100, 100, cv2.BORDER_REPLICATE)
    imgReflect = cv2.copyMakeBorder(imgOriginal, 100, 100, 100, 100, cv2.BORDER_REFLECT)
    imgTransparent = np.ones((imgOriginal.shape[0], imgOriginal.shape[1], 4), np.uint8) * 255

    #criando grid com 3 imagens, a segunda com borda replicada e a terceira com borda de espelho
    #a ultima imagem é transparente
    imgsArray = [imgOriginal, imgReplicate, imgReflect, imgTransparent]
    titlesArray = ['Imagem Original', 'Imagem com Borda Replicada', 'Imagem com Borda de Espelho', '']
    showMultipleImageGrid(imgsArray, titlesArray, 2, 2)

def plotFourImages():
    imgOriginal = cv2.imread("ada.jpg")
    imgReplicate = cv2.copyMakeBorder(imgOriginal, 100, 100, 100, 100, cv2.BORDER_REPLICATE)
    imgReflect = cv2.copyMakeBorder(imgOriginal, 100, 100, 100, 100, cv2.BORDER_REFLECT)
    imgReflect101 = cv2.copyMakeBorder(imgOriginal, 100, 100, 100, 100, cv2.BORDER_REFLECT_101)

    #criando grid com 4 imagens, a segunda com borda replicada e a terceira e quarta com borda de espelho
    imgsArray = [imgOriginal, imgReplicate, imgReflect, imgReflect101]
    titlesArray = ['Imagem Original', 'Imagem com Borda Replicada', 'Imagem com Borda de Espelho', 'Imagem com Borda de Espelho Diferente']
    showMultipleImageGrid(imgsArray, titlesArray, 2, 2)

def plotSixImages():
    imgOriginal = cv2.imread("ada.jpg")
    imgReplicate = cv2.copyMakeBorder(imgOriginal, 100, 100, 100, 100, cv2.BORDER_REPLICATE)
    imgReflect = cv2.copyMakeBorder(imgOriginal, 100, 100, 100, 100, cv2.BORDER_REFLECT)
    imgReflect101 = cv2.copyMakeBorder(imgOriginal, 100, 100, 100, 100, cv2.BORDER_REFLECT_101)
    imgWrap = cv2.copyMakeBorder(imgOriginal, 100, 100, 100, 100, cv2.BORDER_WRAP)

    BLUE = [255, 0, 0]
    imgConstant = cv2.copyMakeBorder(imgOriginal, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value = BLUE)

    #criando grid com 6 imagens, a segunda com borda replicada e a terceira e quarta com borda de espelho
    #constant insere uma moldura e wrap só olhando pra entender =)
    imgsArray = [imgOriginal, imgReplicate, imgReflect, imgReflect101, imgConstant, imgWrap]
    titlesArray = ['Original', 'Borda Replicada', 'Borda de Espelho', 'Borda de Espelho 2', 'Moldura', 'Efeito Wrap']
    showMultipleImageGrid(imgsArray, titlesArray, 3, 2)

def main():
    plotSixImages()

if __name__ == "__main__":
    main()
