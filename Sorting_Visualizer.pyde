import Sorting_Algorithms as SA


#global variable declarations
ArrayToSort = []
resolution = [1290, 720]

def GenerateArray(): 
    global NumOfValues
    #generates a list with len = width and values from 1 to height   
    return [floor(random(1, height)) for value in range(NumOfValues)]


def setup():
    global ArrayToSort
    global NumOfValues 
    
    size(*resolution)
    
    NumOfValues = width/10
    #NumOfValues = 10
    
    ArrayToSort = GenerateArray()
    #ArrayToSort = SA.BubbleSort(ArrayToSort)
    #ArrayToSort = BubbleSort(ArrayToSort)
    
    
def draw():
    global ArrayToSort
    global NumOfValues 
    background(0)
    stroke(0)
    
    #draw control box at top of window
    fill(color(204))
    rect(0,0,width, floor(height * 0.15))
    #fill control box with controls
    



    #translate to bottom left corner, +x is right, -y is up
    translate(0, height)
    
    
    rectwidth = width / NumOfValues
    
    for index, value in enumerate(ArrayToSort):
        #line(index, height, index, height - value)
        #draw rectangle for each element in array
        fill(255)
        rect(index * rectwidth + rectwidth, 0, rectwidth, -value * 0.85)


    translate(0, - height)
    




    #check for key presses
    if keyPressed:
        if key == 's':
            ArrayToSort = SA.BubbleSort(ArrayToSort)
        elif key == 'n':
            ArrayToSort = GenerateArray()
            
            
            
#functions for determining if the mouse is over a control button
def overNewArr():
    return

def overSort():
    return

def overBubble():
    return

def overMerge():
    return

def overQuick():
    return

def overInsertion():
    return

def overHeap():
    return

def overSelection():
    return
