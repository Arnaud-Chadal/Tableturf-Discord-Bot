from PIL import Image

def resizer(liste) :
    img2 = Image.new('RGBA', (len(liste[0]*5), len(liste)*5), (255,255,255,1))
    for i in range(len(liste[0])) :
        for j in range(len(liste)) :
            r = liste[i][j][0]
            g = liste[i][j][1]
            b = liste[i][j][2]
            img2.putpixel((j,i), ((r, g, b)))
            i += 4
            j += 4
    img2.show()
    
    
d = [[(0, 0, 0), (0, 0, 0), (0, 0, 0)],
     [(255, 255, 255), (0, 0, 0), (255, 255, 255)],
     [(255, 255, 255), (255, 255, 255), (255, 255, 255)]]