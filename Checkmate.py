
from PIL import Image 
from numpy import array
import imageio
import os
import copy
import enum

class Colors(enum.Enum):
    WHITE=0
    BLACK=1
    NONE=2
    BOTH=3

class Figure():
    def __init__(self,id=""):
        self.id=id
        if id.islower():
            self.color=Colors.BLACK    
        else:
            self.color=Colors.WHITE

class Square ():
    def __init__(self,x,y,occupied=False,figure=Figure(""),threatened=2,mov=[]):
        self.x=x
        self.y=y
        self.occupied=occupied
        self.figure=figure
        self.threatened=threatened #0-od belog ,1-od crnog ,2-nije,3-oba
        self.possible_moves=mov
    

    def add_possible_move(self,square):
        self.possible_moves.append(square)

    def update_threatened(self,threat):
        if not (self.threatened==threat or self.threatened==Colors.BOTH):
            if self.threatened==Colors.NONE:
                self.threatened=threat
            else:
                self.threatened=Colors.BOTH



    
class Rook(Figure):
    move_direction=[(1,0),(-1,0),(0,1),(0,-1)]
    move_reoccurring=True
    def __init__(self,id):
        super().__init__(id)

class Bishop(Figure):
    move_direction=[(1,1),(-1,-1),(-1,1),(1,-1)]
    move_reoccurring=True
    def __init__(self,id):
        super().__init__(id)

class Queen(Figure):
    move_direction=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
    move_reoccurring=True
    def __init__(self,id):
        super().__init__(id)

class King(Figure):
    move_direction=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
    move_reoccurring=False
    def __init__(self,id):
        super().__init__(id)

class Knight(Figure):
    move_direction=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(-1,-2),(1,-2)]
    move_reoccurring=False
    def __init__(self,id):
        super().__init__(id)

class Pawn(Figure):
    
    move_reoccurring=False
    def __init__(self,id,x_coor):
        self.threat=False
        super().__init__(id)
        self.move_direction=[]
        #self.threat_direction=[]
        sign=0
        if self.color==Colors.BLACK:
            sign=1
        else:
            sign=-1
        self.move_direction.append((sign,0))
        self.move_direction.append((sign,1))
        self.move_direction.append((sign,-1))


class Board():
    def __init__(self):
        self.squares=[]
        for i in range(8):
            self.squares.append([])
            for j in range(8):
                self.squares[i].append(Square(i,j,mov=[]))

    def addFigure(self,x,y,id):
        self.squares[x][y].occupied=True
        if id.lower()=='b':
            self.squares[x][y].figure=Bishop(id)
        elif id.lower()=='k':
            self.squares[x][y].figure=King(id)
        elif id.lower()=='n':
            self.squares[x][y].figure=Knight(id)
        elif id.lower()=='q':
            self.squares[x][y].figure=Queen(id)
        elif id.lower()=='r':
            self.squares[x][y].figure=Rook(id)
        elif id.lower()=='p':
            self.squares[x][y].figure=Pawn(id,x) 

    def move_figure(self,fromx,fromy,tox,toy):
        if not self.squares[fromx][fromy].occupied:
            print("There is no figure to move on square",fromx,fromy)
        else:  
            self.squares[tox][toy].figure=self.squares[fromx][fromy].figure
            self.squares[tox][toy].occupied=True
            self.squares[fromx][fromy].occupied=False
            self.squares[fromx][fromy].figure=Figure("")


    def analyse(self):
        for x in range(8):
            for y in range(8):
                #self.squares[x][y]=self.squares[x][y]#menjanem self.squares[x][y] menja se orginal ?QQQQQQQQQQQQ############################
                if not self.squares[x][y].occupied:
                    continue
                
                for direction in self.squares[x][y].figure.move_direction:#svaki smer ####za Pijuna ovde trena threat direct
                    curx=x
                    cury=y               
                    moving=True
                    threatening=True

                    if self.squares[x][y].figure.id.lower()=='p':#posebno za pijuna
                        curx+=direction[0]
                        cury+=direction[1]
                        if curx<0 or curx>7 or cury<0 or cury>7:
                            continue
                        if not self.squares[x][y].figure.threat and not self.squares[curx][cury].occupied: #prvi mod, kretanje u napred
                            self.squares[x][y].add_possible_move(self.squares[curx][cury])  #ide napred
                        if self.squares[x][y].figure.threat:#drugi mod, jedenje
                            if self.squares[curx][cury].occupied and self.squares[curx][cury].figure.color==(self.squares[x][y].figure.color+1)%2:
                                self.squares[x][y].add_possible_move(self.squares[curx][cury]) #jede dijagonalno
                            self.squares[curx][cury].update_threatened(self.squares[x][y].figure.color)
                        self.squares[x][y].figure.threat=True
                    else:                        
                        while moving or threatening: #"pomera" se u jednom smeru dok moze i oznacava polja
                            curx+=direction[0]
                            cury+=direction[1]
                            #provera opsega
                            if curx<0 or curx>7 or cury<0 or cury>7:
                                break
                            
                            if (not self.squares[curx][cury].occupied or self.squares[curx][cury].figure.color==(self.squares[x][y].figure.color+1)%2 ): #ako je prazno ili popunjeno sa suprotna boja   
                                if threatening:
                                    self.squares[curx][cury].update_threatened(self.squares[x][y].figure.color)
                                    if self.squares[curx][cury].occupied and not self.squares[curx][cury].figure.id.lower()=='k': #ako nije kralj, kraj(oznacice i prvu figuru iza kralja !!!!!ISPRAVITI)
                                        threatening=False
                                if moving:
                                    self.squares[x][y].add_possible_move(self.squares[curx][cury])
                                    if self.squares[curx][cury].occupied:                     
                                        moving=False #kad naidje na figuru
                            else:
                                moving=False
                                threatening=False

                            if not self.squares[x][y].figure.move_reoccurring:
                                break

    def check(self):
        for x in range(8):
            for y in range(8):
                if self.squares[x][y].figure.id.lower()=='k' and (self.squares[x][y].threatened==(self.squares[x][y].figure.color+1)%2 or self.squares[x][y].threatened==Colors.BOTH):
                    return (self.squares[x][y].figure.color+1)%2
        return Colors.NONE
    
    def clean(self):
        for x in range(8):
            for y in range(8):
                self.squares[x][y].threatened=2
                self.squares[x][y].possible_moves=[]

    def check_check(self,CHECK): #provera da li je i dalje sah
        for i in range(8):
            for j in range(8):
                if self.squares[i][j].figure.id.lower()=='k' and self.squares[i][j].figure.color==(CHECK+1)%2: #find king
                    if (self.squares[i][j].threatened==(self.squares[i][j].figure.color+1)%2 or self.squares[i][j].threatened==Colors.BOTH):
                        return True
                    else:
                        return False

                
    def mate(self,CHECK):
        for x in range(8):
            for y in range(8): 
                if self.squares[x][y].occupied and self.squares[x][y].figure.color==(CHECK+1)%2:
                    for move in self.squares[x][y].possible_moves:
                        new_board=copy.deepcopy(self)
                        new_board.move_figure(x,y,move.x,move.y)
                        new_board.clean()
                        new_board.analyse()
                        if not new_board.check_check(CHECK):
                            return 0
                        self.squares
        return 1


                        
                        


thumbnail_mode=Image.NEAREST

path=input()

img = Image.open(path+"\\"+path[path.rindex("\\")+1:]+".png").convert('L')

img_arr=array(img)
#img_arr=imageio.imread(path+"\\"+path[path.rindex("\\")+1:]+".png")
#print (img_arr[0][0])

pix=0
x=0
y=0
for x in range(len(img_arr)):
    y=0
    for y in range(len(img_arr[x])):
        #pix=int(img_arr[x][y][0])+int(img_arr[x][y][1])+int(img_arr[x][y][2])
        pix=img_arr[x][y]
        if pix>0:
            break
    if pix>0:
        break
upper_left=(x,y)

for y in range(upper_left[1],len(img_arr[x])):
    #pix=int(img_arr[x][y][0])+int(img_arr[x][y][1])+int(img_arr[x][y][2])
    pix=img_arr[x][y]
    if pix==0:
        break
upper_right=(x,y)

tile_width=(upper_right[1]-upper_left[1])//8
tile_size=(tile_width,tile_width)


black_tile_img=Image.open(path+"\\tiles\\black.png").convert('L')
white_tile_img=Image.open(path+"\\tiles\\white.png").convert('L')
black_tile_img.thumbnail(tile_size,thumbnail_mode)
white_tile_img.thumbnail(tile_size,thumbnail_mode)
black_tile_img_arr=array(black_tile_img)
white_tile_img_arr=array(white_tile_img)
tiles_arr=[white_tile_img_arr,black_tile_img_arr]

TILE_COLOR=(white_tile_img_arr[0][0],black_tile_img_arr[0][0])

#pravljenje slika figura na poljima odgovarajuce velicine
board_images=[ [], [] ]
for tile_color in Colors.WHITE,Colors.BLACK:
    for directory_name in os.listdir(path+"\\pieces"):
        if directory_name=="Colors.WHITE":
            figure_color=Colors.WHITE
        else:
            figure_color=Colors.BLACK
        for filename in os.listdir(path+"\\pieces\\"+directory_name):
            letter=0
            if filename=="knight.png":
                letter=1
            figure_name=filename[letter] #ime figure za FEN notaciju
            if figure_color==Colors.WHITE:
                figure_name=figure_name.upper()
            figure_img=Image.open(path+"\\pieces\\"+directory_name+"\\"+filename).convert('LA') #######################mozda treba convert to LA!!!!!
            figure_img.thumbnail(tile_size,thumbnail_mode)
            figure_arr=array(figure_img)

            fig_and_tile=[]
            for x in range(tile_width):
                fig_and_tileR=[]
                for y in range(tile_width):
                    if(figure_arr[x][y][1]==0):
                        fig_and_tileR.append(tiles_arr[tile_color][x][y])
                    else:
                        fig_and_tileR.append(figure_arr[x][y][0])
                fig_and_tile.append(fig_and_tileR)
            fig_and_tile_arr=array(fig_and_tile)
            board_images[tile_color].append((fig_and_tile_arr,figure_name))


#prolazenje kroz tablu
board=Board()
board_matrix=[]

startx=upper_left[0]
for i in range(8):#offset x /tileWidth
    board_matrix.append([])
    starty=upper_left[1]
    if img_arr[startx+i*tile_width][starty]!=TILE_COLOR[i%2]:      #za slucaj da visina table nije deljiva sa 8, neka polja ce biti za jedan visa od drugih
        startx+=1
    for j in range(8):#offset y
        if img_arr[startx+i*tile_width][starty+j*tile_width]!=TILE_COLOR[(i+j)%2]:      #za slucaj da sirina table nije deljiva sa 8, neka polja ce biti za jedan sira od drugih
            starty+=1

        similar=0
        for x in range(tile_width):
            for y in range(tile_width):
                if abs(int(img_arr[startx+i*tile_width+x][starty+j*tile_width+y])-int(tiles_arr[(i+j)%2][x][y]))<10:
                    similar+=1
        similarity_percent=similar/(tile_width**2)
         
        if(similarity_percent>0.9): #polje je prazno
            if j>0 and isinstance(board_matrix[i][-1], int):
                board_matrix[i][-1]+=1
            else:
                board_matrix[i].append(1)
            continue
        else:#nije prazno, uporedjuje se sa ostalima
            max_similarity=0
            sim_fig="" #ime figure koja je najslicnija
            for example in board_images[(i+j)%2]: #primer polja sa figurom, example=(array,name)
                similar=0
                differ_from_bckgrnd=0
                for x in range(tile_width):
                    for y in range(tile_width):
                        if img_arr[startx+i*tile_width+x][starty+j*tile_width+y]==TILE_COLOR[(i+j)%2] and example[0][x][y]==TILE_COLOR[(i+j)%2]:
                            continue
                        differ_from_bckgrnd+=1
                        if abs(int(img_arr[startx+i*tile_width+x][starty+j*tile_width+y])-int(example[0][x][y]))<30:
                            similar+=1
                similarity_percent=similar/differ_from_bckgrnd
                
                if similarity_percent>max_similarity:
                    max_similarity=similarity_percent
                    sim_fig=example[1]
            board_matrix[i].append(sim_fig)
            board.addFigure(i,j,sim_fig)
            
                
FEN=""
for row in board_matrix:
    for field in row:
        FEN+=str(field)
    FEN+="/"
FEN=FEN[:-1]


#RESENJA
print ("{},{}".format(upper_left[0],upper_left[1]))
print(FEN)

board.analyse()
check=board.check()
answer3="-"
if check==Colors.WHITE:
    answer3='W'
elif check==Colors.BLACK:
    answer3='B'
print(answer3)

print(board.mate(check))







    