import Sorting_Algorithms as SA

#global variable declarations
ArrayToSort = [] #random array to be sorted
SortAnimations = [] #animation info from sorting algorithm

resolution = [1290, 720]

AnimationIndex = 0
isAnimating = False

OverGenerate = False
OverSort = False
OverBubble = False
OverMerge = False
OverQuick = False
OverInsertion = False
OverHeap = False
OverSelection = False

ReadyToSort = False
Algorithm = ''






def setup():
    global ArrayToSort, NumOfValues, controlHeight, controlWidth, offsetPercent
    
    size(*resolution)
    
    controlHeight = floor(0.15*height) # Total height of control box
    controlWidth = floor(width/3) # 1/3 total width of control box eg: width of control sub boxes
    offsetPercent = 0.1
    
    NumOfValues = floor(width/50)
    #NumOfValues = 10

    GenerateArray()
    
    #frameRate(2)

        
def draw():
    global ArrayToSort, NumOfValues, controlHeight, controlWidth, offsetPercent, isAnimating, AnimationIndex, SortAnimations, SortedArray
    update(mouseX, mouseY)
    background(0)
    stroke(0)
    
    #draw control box at top of window
    fill(150)
    rect(0,0,width, controlHeight)    
    
    #vertical lines at 1/3 and 2/3 width
    line(controlWidth, 0, controlWidth, controlHeight)
    line(2*controlWidth, 0, 2*controlWidth, controlHeight)
    
    #Need to fix hardcoding of values on some spots
    
    fill(220)
    #Generate New Array Button
    rect(offsetPercent*controlWidth, offsetPercent*controlHeight, controlWidth*(1- 2*offsetPercent), 0.35*controlHeight)
    
    #Sort Button
    rect(offsetPercent*controlWidth, 0.55*controlHeight, controlWidth*(1- 2*offsetPercent), 0.35*controlHeight)
    
    #Bubble Button
    ellipse(7*width/9, controlHeight/4, controlHeight/4, controlHeight/4)
    
    #Merge Button
    ellipse(8*width/9, controlHeight/4, controlHeight/4, controlHeight/4)
    
    
    
    #fill control box with controls


    
    rectwidth = width / NumOfValues
    
    
    if len(SortAnimations) == 0:
        #draw the unsorted array
        drawArray(ArrayToSort, rectwidth, [255])
        
    else:
        #array has been sorted
        
        #check if sorting animation has been completed. if finished, reset animation index and flag
        if AnimationIndex > len(SortAnimations)-1:
            isAnimating = False
            AnimationIndex = 0
            backIndex = 0
            
        if isAnimating:
            #draw current array
            drawArray(ArrayToSort, rectwidth, [255])

            Animation = SortAnimations[AnimationIndex]
            
            #color in indices being compared
            translate(0, height)
            
            fill(0, 255, 0)
            if Animation[2]:
                fill(255, 0 , 0)
        
            rect(Animation[0]*rectwidth, 0, rectwidth, -0.85*ArrayToSort[Animation[0]])
            rect(Animation[1]*rectwidth, 0, rectwidth, -0.85*ArrayToSort[Animation[1]])
            
            translate(0, - height)

            if Animation[2]:
                ArrayToSort = SA.swap(ArrayToSort, Animation[0], Animation[1])
                    
            AnimationIndex +=1
            
        else:
            #animation has finished, color final sorted array green
            drawArray(ArrayToSort, rectwidth, [0, 255, 0])

    #check for key presses
    if keyPressed:
        if key == 's':
            startSort()
        elif key == 'n':
            GenerateArray()


def drawArray(arr, rectwidth, fillcolor):
    #translate to bottom left corner, +x is right, -y is up
    translate(0, height)
    
    for index, value in enumerate(arr):
        #draw rectangle for each element in array
        fill(*fillcolor)
        rect(index*rectwidth, 0, rectwidth, -0.85*value)
    
    #translate back to origin
    translate(0, -height)
    return


def GenerateArray(): 
    global NumOfValues, ArrayToSort, SortAnimations, ReadyToSort
    SortAnimations = []

    #generates a list with len = width and values from 1 to height  
    ArrayToSort = [floor(random(1, height)) for value in range(NumOfValues)]
    
    ReadyToSort = True
    return            
                                    

def startSort():
    global ArrayToSort, SortAnimations, ReadyToSort, isAnimating
    SortAnimations = []
    
    if not ReadyToSort:
        return
    
    SortAnimations = SA.BubbleSort(list(ArrayToSort)) #would use .copy() but processing isn't Python 3...
    
    isAnimating = True
    return


def update(x, y):
    global OverGenerate, OverSort, controlHeight, controlWidth, offsetPercent
    
    OverGenerate = overRect(offsetPercent * controlWidth, offsetPercent * controlHeight, controlWidth * (1 - 2 * offsetPercent), 0.35 * controlHeight)
    OverSort = overRect(offsetPercent * controlWidth, 0.55 * controlHeight, controlWidth * (1 - 2 * offsetPercent), 0.35 * controlHeight)

            
def mousePressed():
    if OverGenerate:
        GenerateArray()
    if OverSort:
        startSort()
    return


#functions for determining if the mouse is over a control button
def overRect(x, y, width, height):
    return x <= mouseX <= x+width and y <= mouseY <= y+height


def overCircle(x, y, diameter):
    distance = dist(x, y, mouseX, mouseY)
    return distance < diameter/2
