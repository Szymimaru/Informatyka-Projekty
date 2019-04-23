from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QLineEdit, QGridLayout, QColorDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import matplotlib.pyplot as plt

class Window(QWidget):
	def __init__(self):
		QWidget.__init__(self)
        
		self.button = QPushButton('Rysuj i oblicz \n współrzędne punktu \n przecięcia', self)
		self.button2 = QPushButton('Wyczyść pola', self)
		self.button3 = QPushButton('Zapisz współrzędne punktu przecięcia', self)
		self.clrChoose = QPushButton('Wybierz kolor', self)
		self.label1 = QLabel("Podaj współrzędne punktu 1:", self)
		self.xlabel = QLabel("X:", self)
		self.xEdit = QLineEdit()
		self.ylabel = QLabel("Y:", self)
		self.yEdit = QLineEdit()
		self.label2 = QLabel("Podaj współrzędne punktu 2:", self)
		self.x2label = QLabel("X:", self)
		self.x2Edit = QLineEdit()
		self.y2label = QLabel("Y:", self)
		self.y2Edit = QLineEdit()
		self.label3 = QLabel("Podaj współrzędne punktu 3:", self)
		self.x3label = QLabel("X:", self)
		self.x3Edit = QLineEdit()
		self.y3label = QLabel("Y:", self)
		self.y3Edit = QLineEdit()
		self.label4 = QLabel("Podaj współrzędne punktu 4:", self)
		self.x4label = QLabel("X:", self)
		self.x4Edit = QLineEdit()
		self.y4label = QLabel("Y:", self)
		self.y4Edit = QLineEdit()
		self.label5 = QLabel("Współrzędne punktu przecięcia", self)
		self.Xplabel = QLabel("X:", self)
		self.Xplabeldisp = QLineEdit()
		self.Yplabel = QLabel("Y:", self)
		self.Yplabeldisp = QLineEdit()
		self.wniosek = QLabel()
        
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
        
        # ladne ustawienie i wysrodkowanie
		layout =  QGridLayout(self)
        
		layout.addWidget(self.label1, 1, 1)
		layout.addWidget(self.xlabel, 2, 0)
		layout.addWidget(self.xEdit, 2, 1)
		layout.addWidget(self.ylabel, 3, 0)
		layout.addWidget(self.yEdit, 3, 1)
		layout.addWidget(self.label2, 1, 3)
		layout.addWidget(self.x2label, 2, 2)
		layout.addWidget(self.x2Edit, 2, 3)
		layout.addWidget(self.y2label, 3, 2)
		layout.addWidget(self.y2Edit, 3, 3)
		layout.addWidget(self.label3, 1, 5)
		layout.addWidget(self.x3label, 2, 4)
		layout.addWidget(self.x3Edit, 2, 5)
		layout.addWidget(self.y3label, 3, 4)
		layout.addWidget(self.y3Edit, 3, 5)
		layout.addWidget(self.label4, 1, 7)
		layout.addWidget(self.x4label, 2, 6)
		layout.addWidget(self.x4Edit, 2, 7)
		layout.addWidget(self.y4label, 3, 6)
		layout.addWidget(self.y4Edit, 3, 7)
		layout.addWidget(self.label5, 4, 10, 1, 1)
		layout.addWidget(self.Xplabel, 4, 9, 2, 1)
		layout.addWidget(self.Yplabel, 4, 9, 3, 1)
		layout.addWidget(self.button3, 9, 10, 1, 1)
		layout.addWidget(self.button2, 10, 10, 1, 1)
		layout.addWidget(self.Xplabeldisp, 4, 10, 2, 1)
		layout.addWidget(self.Yplabeldisp, 4, 10, 3, 1)
		layout.addWidget(self.button, 2, 10, 2, 1) 
		layout.addWidget(self.canvas, 4, 0, -1, 8)
		layout.addWidget(self.clrChoose, 1, 10)
		layout.addWidget(self.wniosek, 4, 10, 5, 1)
        
        # połączenie przycisku (signal) z akcją (slot)
		self.button.clicked.connect(self.handleButton)
		self.clrChoose.clicked.connect(self.clrChooseF)
		self.button2.clicked.connect(self.wyczysc)
		self.button3.clicked.connect(self.zapisz)
        
	def checkValues(self,lineE):
		if lineE.text().lstrip('-').replace(".", '').isdigit():
			return float(lineE.text())
		else:
			return None
    
	def rysuj(self,clr='black'):      #Funkcja rysująca wykres i wykonująca obliczenia
		x = self.checkValues(self.xEdit)
		y = self.checkValues(self.yEdit)
		x2 = self.checkValues(self.x2Edit)
		y2 = self.checkValues(self.y2Edit)
		x3 = self.checkValues(self.x3Edit)
		y3 = self.checkValues(self.y3Edit)
		x4 = self.checkValues(self.x4Edit)
		y4 = self.checkValues(self.y4Edit)

        #Kontrola wpisanych wartosci
		if x==None or y==None or x2==None or y2==None or x3==None or y3==None or x4==None or y4==None:
			self.figure.clear()
			msg_err = QMessageBox()
			msg_err.setWindowTitle("Komunikat")
			msg_err.setStandardButtons(QMessageBox.Ok)
			msg_err.setText("Podane współrzędne są nieprawidłowe")
			msg_err.exec_()
			self.figure.clear()
			self.canvas.draw()

		deltax12=x2-x
		deltax13=x3-x
		deltax34=x4-x3
		deltay12=y2-y
		deltay13=y3-y
		deltay34=y4-y3
		mianownik=deltax12*deltay34-deltay12*deltax34
		if mianownik!=0:
			t1=(deltax13*deltay34-deltay13*deltax34)/mianownik
			t2=(deltax13*deltay12-deltay13*deltax12)/mianownik
			if 0<=t1<=1 and 0<=t2<=1:
				Xp=x+t1*deltax12
				Yp=y+t1*deltay12
				X="{0:.3f}".format(Xp)
				Y="{0:.3f}".format(Yp)
				self.Xplabeldisp.setText(X)
				self.Yplabeldisp.setText(Y)
				self.wniosek.setText("Odcinki się przecinają")
			elif 0<=t2<=1:
				Xp=x+t1*deltax12
				Yp=y+t1*deltay12
				X="{0:.3f}".format(Xp)
				Y="{0:.3f}".format(Yp)
				self.Xplabeldisp.setText(X)
				self.Yplabeldisp.setText(Y)
				self.wniosek.setText("Odcinki przecinają się na przedłużeniu pierwszego odcinka")
			elif 0<=t1<=1:
				Xp=x+t1*deltax12
				Yp=y+t1*deltay12
				X="{0:.3f}".format(Xp)
				Y="{0:.3f}".format(Yp)
				self.Xplabeldisp.setText(X)
				self.Yplabeldisp.setText(Y)
				self.wniosek.setText("Odcinki przecinają się na przedłużeniu drugiego odcinka")
			else:
				Xp=x+t1*deltax12
				Yp=y+t1*deltay12
				X="{0:.3f}".format(Xp)
				Y="{0:.3f}".format(Yp)
				self.Xplabeldisp.setText(X)
				self.Yplabeldisp.setText(Y)
				self.wniosek.setText("Odcinki przecinają się na przedłużeniu obu odcinków")
		elif mianownik==0:
			self.wniosek.setText("Odcinki są równoległe, więc się nie przecinają")
			
			
        #Wykres
		if x!=None and y!=None and x2!=None and y2!=None and x3!=None and y3!=None and x4!=None and y4!=None:
			self.figure.clear()
			ax=self.figure.add_subplot(111)
            #Rysowanie punktóW
			ax.plot(x,y,'o',color='black')
			ax.plot(x2,y2,'o',color='black')
			ax.plot(x3, y3,'o',color='black')
			ax.plot(x4, y4,'o',color='black')
            #Rysowanie linii
			ax.plot((x,x2),(y,y2),color=clr)
			ax.plot((x3,x4),(y3,y4),color=clr)
            #Opisanie punktów na wykresie
			if mianownik==0:
				ax.text(x,y,"Punkt 1 ["+str(x)+","+str(y)+"]",fontsize=10,color="black")
				ax.text(x2,y2,"Punkt 2 ["+str(x2)+","+str(y2)+"]",fontsize=10,color="black")
				ax.text(x3,y3,"Punkt 3 ["+str(x3)+","+str(y3)+"]",fontsize=10,color="black")
				ax.text(x4,y4,"Punkt 4 ["+str(x4)+","+str(y4)+"]",fontsize=10,color="black")
			else:
				ax.plot(Xp, Yp, 'o', color='magenta')
                #Rysowanie przedłużeń
				ax.plot((x,Xp),(y,Yp),linestyle='--',dashes=(2,5),color=clr)
				ax.plot((x2,Xp),(y2,Yp),linestyle='--',dashes=(2,5),color=clr)
				ax.plot((x3,Xp),(y3,Yp),linestyle='--',dashes=(2,5),color=clr)
				ax.plot((x4,Xp),(y4,Yp),linestyle='--',dashes=(2,5),color=clr)
                #Opisanie punktów
				ax.text(x,y,"Punkt 1 ["+str(x)+","+str(y)+"]",color="black")
				ax.text(x2,y2,"Punkt 2 ["+str(x2)+","+str(y2)+"]",color="black")
				ax.text(x3,y3,"Punkt 3 ["+str(x3)+","+str(y3)+"]",color="black")
				ax.text(x4,y4,"Punkt 4 ["+str(x4)+","+str(y4)+"]",color="black")
				ax.text(Xp,Yp,"Punkt Przecięcia ["+str(X)+","+str(Y)+"]",color="magenta")
			self.canvas.draw()

    #Funkcja zapisująca wyniki do pliku
	def zapisz(self): 
		self.plik=open('wyniki.txt' ,'w') 
		self.plik.write('|{}|'.format('Współrzędne punktu przecięcia')+'\n')
		self.plik.write(31*'-'+'\n')
		self.plik.write('|{}|{:^26.3f}|'.format('Xp',self.checkValues(self.Xplabeldisp))+'\n')
		self.plik.write('|{}|{:^26.3f}|'.format('Yp',self.checkValues(self.Yplabeldisp))+'\n')
		self.plik.write(31*'-'+'\n')
		self.plik.close()   
    
    #Funkcja czyszcząca dane wpisane przez użytkownika
	def wyczysc(self):        
		self.xEdit.clear()
		self.yEdit.clear()
		self.x2Edit.clear()
		self.y2Edit.clear()
		self.x3Edit.clear()
		self.y3Edit.clear()
		self.x4Edit.clear()
		self.y4Edit.clear()
		self.Xplabeldisp.clear()
		self.Yplabeldisp.clear()
		self.wniosek.clear()
		self.figure.clear()
        
        
	def handleButton(self):
		self.rysuj()
        
    #Funkcja wybierająca kolor
	def clrChooseF(self):
		color = QColorDialog.getColor()
		if color.isValid():
			self.rysuj(color.name())
		else:
			pass
        
if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    window = Window()
    window.show()
    app.exec_()