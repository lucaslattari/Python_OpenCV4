import numpy as np
import cv2

def showImage(img):
    from matplotlib import pyplot as plt
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()

def getImageWithRedColorOnly(img):
    altura, largura, cores = img.shape
    for y in range(0, altura):
        for x in range(0, largura):
            azul = img.item(y, x, 0) #posição x, y e a coordenada de cor (0 é azul)
            verde = img.item(y, x, 1) #posição x, y e a coordenada de cor (1 é verde)
            vermelho = img.item(y, x, 2) #posição x, y e a coordenada de cor (2 é vermelho)

            img.itemset((y, x, 0), 0) #na posição x, y e coordenada azul, atribui-se o valor 0
            img.itemset((y, x, 1), 0) #na posição x, y e coordenada vermelha, atribui-se o valor 0
            #como vamos manter o vermelho como está, não é necessário adicionar uma chamada para tal

    return img

def main():
    img = cv2.imread("ada.jpg")
    print("As dimensões dessa imagem são: " + str(img.shape))

    eye = img[168:190,97:124]
    img[137 : 137 + eye.shape[0] , 141 : 141 + eye.shape[1]] = eye
    showImage(img)

main()
