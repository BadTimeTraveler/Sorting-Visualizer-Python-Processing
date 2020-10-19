from hscrollbar import HScrollbar
import time

####################################################################################################
#global variable declarations
ArrayToSort = [] #random array to be sorted
SortedArray = [] 
SortAnimations = [] #animation info from sorting algorithm

resolution = [1290, 720] # window resolution
rectwidth = 0

colorHSB = False
fr = 30

#indices for sorting animations
AnimationIndex = 0
CountingIndex = 0

isAnimating = False # flag to keep track of when a sorting animation is running
ReadyToSort = False # flag to keep track of when a sorting algorithm can be ran

#Counters for drawing MergeSort
MergeCount = 0
prevStart = 0

#flags for if the mouse is over a specific button
OverGenerate = False
OverSort = False
OverBubble = False
OverMerge = False
OverQuick = False
OverGravity = False
OverCounting = False
OverRadixLSD = False

Algorithm = 'Bubble' #String for the current selected algorithm, Bubble is the default animation


####################################################################################################


def setup():
    global ArrayToSort, NumOfValues, controlHeight, controlWidth, offsetPercent, rectwidth
    global ArraySizeScrollbar, FrameRateScrollbar, colorHSB, prevArrayPos, prevFramePos, f
    
    size(*resolution)
    
    controlHeight = floor(0.15*height) # Total height of control box
    controlWidth = floor(width/3) # 1/3 total width of control box eg: width of control sub boxes
    offsetPercent = 0.1 # for control formatting
    #colorMode(HSB, controlHeight, controlHeight, controlHeight)
    #colorHSB = True
    
    #noStroke()
    #create scrollbars for array size and framerate
    ArraySizeScrollbar = HScrollbar(controlWidth, controlHeight / 2 - 8, controlWidth, 16, 16)
    FrameRateScrollbar = HScrollbar(controlWidth, controlHeight - 8, controlWidth, 16, 16)
    
    #used to check if the scrollbars have been adjusted, starting point is middle of the window
    prevArrayPos = width / 2
    prevFramePos = width / 2
    
    #number of values to be sorted, and the pixel width of the individual rectangles
    NumOfValues = floor(width/10)
    rectwidth = width / NumOfValues
    
    #generate a starting array
    GenerateArray()
    
    #create font for controlbox text
    f = createFont("Arial", 16, True)
    
####################################################################################################


def draw():
    global ArrayToSort, NumOfValues, controlHeight, controlWidth, offsetPercent, isAnimating, AnimationIndex, SortAnimations, SortedArray, ReadyToSort, MergeCount, prevStart, rectwidth
    global ArraySizeScrollbar, FrameRateScrollbar, prevArrayPos, prevFramePos, f, fr
    
    #check if a button was pressed
    mouseClick()
    #update flags for mouse position
    update(mouseX, mouseY)
    
    background(0)
    stroke(0)
    fill(150)
    
    #draw control box at top of window
    rect(0,0,width, controlHeight)    
    
    #vertical lines at 1/3 and 2/3 width
    line(controlWidth, 0, controlWidth, controlHeight)
    line(2*controlWidth, 0, 2*controlWidth, controlHeight)
    
    #fill control box with controls
    fill(220)
    rect(0, 0, controlWidth, controlHeight)
    line(0, controlHeight/2, controlWidth, controlHeight/2)
    
    #Generate New Array Button
    #0, 0, controlWidth, controlHeight/2
    #Sort Button
    #0, controlHeight/2, controlWidth, controlHeight/2

    #Lines for Algorithm Buttons
    rect(2*controlWidth, 0, controlWidth, controlHeight)
    line(2.5*controlWidth, 0, 2.5*controlWidth, controlHeight)
    line(2*controlWidth, controlHeight/3, 3*controlWidth, controlHeight/3)
    line(2*controlWidth, 2*controlHeight/3, 3*controlWidth, 2*controlHeight/3)
    
    #draw text for control buttons
    textFont(f, 36)
    fill(0)
    textAlign(CENTER)
    #Left
    text("Generate New Array", controlWidth/2, controlHeight/3)
    text("Start Sorting", controlWidth/2, 5*controlHeight/6)
    #Mid
    textFont(f, 24)
    text("Array Size: " + str(NumOfValues), 1.5*controlWidth, controlHeight/4)
    text("FrameRate: " + str(fr), 1.5*controlWidth, 3*controlHeight/4)
    #Right
    text("Bubble Sort", 2.25*controlWidth, controlHeight/4)
    text("Merge Sort", 2.75*controlWidth, controlHeight/4)
    text("Quick Sort", 2.25*controlWidth, 7*controlHeight/12)
    text("Gravity Sort", 2.75*controlWidth, 7*controlHeight/12)
    text("Counting Sort", 2.25*controlWidth, 11*controlHeight/12)
    text("RadixLSD Sort", 2.75*controlWidth, 11*controlHeight/12)
    
    #select drawing animation based on currently selected algorithm
    #Would us dictionary unpacking if this was Python 3...
    if Algorithm == 'Bubble':
        DrawBubble()
    elif Algorithm == 'Merge':
        DrawMerge()
    elif Algorithm == 'Quick':
        DrawQuick()
    elif Algorithm == 'Gravity':
        DrawGravity()
    elif Algorithm == 'Counting':
        DrawCounting()
    elif Algorithm == 'RadixLSD':
        DrawRadixLSD()  

    #update the scrollbar positions and display them
    ArraySizeScrollbar.update()
    ArraySizeScrollbar.display()
    FrameRateScrollbar.update()
    FrameRateScrollbar.display()
    
    #save the updated scrollbar positions
    curArrayPos = ArraySizeScrollbar.getPos()
    curFramePos = FrameRateScrollbar.getPos()
    
    # map numofvalues to be between 10 and width/2
    if curArrayPos !=  prevArrayPos:
        NumOfValues = int(map(curArrayPos, 447, 861, 10, width/2))
        rectwidth = float(width) / NumOfValues
        GenerateArray()
        prevArrayPos = curArrayPos
    
    # map framerate to be between 2 and 60
    if curFramePos != prevFramePos:
        fr = int(map(curFramePos, 447, 861, 2, 60))
        frameRate(fr)
        prevFramePos = curFramePos
    
    
    #originally was going to use keyboard shortcuts
    """
    #This breaks the sorting algorithm if 'n' is held down for a few seconds... no idea why.
    #check for key pressed
    if keyPressed:
        if key == 's':
            startSort()
        elif key == 'n':
            GenerateArray()
    """
    
####################################################################################################

        
def GenerateArray():
    #generates a new array of random values
    
    global NumOfValues, ArrayToSort, SortedArray, SortAnimations, ReadyToSort, AnimationIndex, isAnimating
    
    #call reset function to reset arrays/indices
    reset()
    # #stop animating and reset arrays/index associated with the sorted array/animations
    # isAnimating = False
    # SortedArray = []
    # SortAnimations = []
    # AnimationIndex = 0

    #generates a list with len = NumOfValues and values from 1 to height  
    ArrayToSort = [floor(random(1, height)) for value in range(NumOfValues)]
    
    ReadyToSort = True
    return            
                                    

def startSort():
    # calls the currently selected sorting algorithm and then sets the animation flag to start animating the sort
    
    global ArrayToSort, SortedArray, ReadyToSort, isAnimating
    
    #call reset function to reset arrays/indices
    reset()
        
    #if a new array hasn't been generated, don't start sorting
    if not ReadyToSort:
        return
    
    #SortedArray = MergeSort(list(ArrayToSort))  # would use .copy() but processing isn't Python 3...
    
    #call the currently selected sorting algorithm
    if Algorithm == 'Bubble':
        SortedArray = BubbleSort(list(ArrayToSort))
    elif Algorithm == 'Merge':
        SortedArray = MergeSort(list(ArrayToSort))
    elif Algorithm == 'Quick':
        SortedArray = QuickSort(list(ArrayToSort), 0, len(ArrayToSort)-1)
    elif Algorithm == 'Gravity':
        SortedArray = GravitySort(list(ArrayToSort))
    elif Algorithm == 'Counting':
        SortedArray = CountingSort(list(ArrayToSort))
    elif Algorithm == 'RadixLSD':
        SortedArray = RadixLSDSort(list(ArrayToSort))
    
    #start animating
    isAnimating = True
    return


def update(x, y):
    #updates mouse position and checks if it's over any control boxes
    
    global OverGenerate, OverSort, OverBubble, OverMerge, OverQuick, OverGravity, OverCounting, OverRadixLSD, controlHeight, controlWidth, offsetPercent
    
    OverGenerate = overRect(0, 0, controlWidth, controlHeight/2)
    OverSort = overRect(0, controlHeight/2, controlWidth, controlHeight/2)
    
    OverBubble = overRect(2*controlWidth, 0, controlWidth/2, controlHeight/3)
    OverMerge = overRect(2.5*controlWidth, 0, controlWidth/2, controlHeight/3)
    
    OverQuick = overRect(2*controlWidth, controlHeight/3, controlWidth/2, controlHeight/3)
    OverGravity = overRect(2.5*controlWidth, controlHeight/3, controlWidth/2, controlHeight/3)
    
    OverCounting = overRect(2*controlWidth, 2*controlHeight/3, controlWidth/2, controlHeight/3)
    OverRadixLSD = overRect(2.5*controlWidth, 2*controlHeight/3, controlWidth/2, controlHeight/3)


def mouseClick():
    #checks if the mouse has been clicked. if it has, checks if the mouse is over a control button and if so calls the appropriate function
    #also calls reset() if an algorithm button was clicked
    
    global Algorithm, Algorithms
    if mousePressed:
        time.sleep(0.1)
        if OverGenerate:
            GenerateArray()
        if OverSort:
            startSort()
        if OverBubble:
            Algorithm = 'Bubble'
            reset()
        if OverMerge:
            Algorithm = 'Merge'
            reset()
        if OverQuick:
            Algorithm = 'Quick'
            reset()
        if OverGravity:
            Algorithm = 'Gravity'
            reset()
        if OverCounting:
            Algorithm = 'Counting'
            reset()
        if OverRadixLSD:
            Algorithm = 'RadixLSD'
            reset()
    return


def reset():
    #stop animating and reset arrays/index associated with the sorted array/animations
    
    global SortedArray, SortAnimations, AnimationIndex, isAnimating
    
    isAnimating = False
    SortedArray = []
    SortAnimations = []
    AnimationIndex = 0
    return


####################################################################################################
def overRect(x, y, width, height):
    #function for determining if the mouse is over a control button
    return x <= mouseX <= x+width and y <= mouseY <= y+height


####################################################################################################
#Sorting Algorithm Functions
#all functions must use SortAnimations as a global variable and only return the final sorted array


def swap(arr, ia, ib):
    #swaps two elements in an array
    
    arr[ia], arr[ib] = arr[ib], arr[ia]
    return arr


def BubbleSort(Arr):
    #implementation of BubleSort algorithm
    
    global SortAnimations
    
    #number of items in array
    n = len(Arr)
    
    for i in range(n):
        for j in range(n-i-1):
            a = Arr[j]
            b = Arr[j+1]            

            if a > b:
                Arr = swap(Arr, j, j+1)   
            #records the indices being compared and if they should be swapped
            SortAnimations.append([j, j+1, a > b])

    return Arr


def MergeSort(Arr):
    #implementation of recursive MergeSort algorithm

    if len(Arr) <= 1:
        return Arr

    left, right = [], []

    for index, value in enumerate(Arr):
        if index < len(Arr)/2:
            try:
                left.append([value[0], value[1]])
            except TypeError:
                left.append([index, value])
        else:
            try:
                right.append([value[0], value[1]])
            except TypeError:
                right.append([index, value])

    left = MergeSort(left)
    right = MergeSort(right)

    return Merge(left, right)


def Merge(left, right):
    #merges two arrays for MergeSort
    
    global SortAnimations

    Merged = []

    FirstIndex = left[0][0]
    EndIndex = right[-1][0]
    MergedCounter = FirstIndex


    # SortAnimations = [Start of left array, end of right array, index original, index moved, value]
    # probably don't need the value

    while len(left) and len(right):
        if left[0][1] <= right[0][1]:
            SortAnimations.append([FirstIndex, EndIndex, MergedCounter, MergedCounter, left[0][1]])
            left[0][0] = MergedCounter
            Merged.append(left.pop(0))
            MergedCounter += 1
        else:
            SortAnimations.append([FirstIndex, EndIndex, right[0][0], MergedCounter, right[0][1]])
            left[0][0] += 1
            right[0][0] = MergedCounter
            Merged.append(right.pop(0))
            MergedCounter += 1

    while len(left):
        SortAnimations.append([FirstIndex, EndIndex, MergedCounter, MergedCounter, left[0][1]])
        left[0][0] = MergedCounter
        Merged.append(left.pop(0))
        MergedCounter += 1

    while len(right):
        SortAnimations.append([FirstIndex, EndIndex, MergedCounter, MergedCounter, right[0][1]])
        right[0][0] = MergedCounter
        Merged.append(right.pop(0))
        MergedCounter += 1

    return Merged


def HoarePartition(arr, startindex, endindex):
    #Hoare Partition function for QuickSort algorithm
    
    global SortAnimations

    pivotIndex = int((endindex + startindex)/2)
    pivot = arr[pivotIndex]

    i = startindex - 1
    j = endindex + 1

    while True:
        i += 1
        while not arr[i] >= pivot:
            i += 1
        j -= 1
        while not arr[j] <= pivot:
            j -= 1
        if i >= j:
            return j
        #records the ends of the sub array and the pivot index as well as the two indices being checked
        SortAnimations.append([startindex, endindex, pivotIndex, i, j])
        swap(arr, i, j)
        
        
def QuickSort(arr, start, end):
    #implementation of recursive QuickSort algorithm using Hoare Partition function
    
    Sorted = list(arr)
    
    if start < end:
        pivot = HoarePartition(Sorted, start, end)
        QuickSort(Sorted, start, pivot)
        QuickSort(Sorted, pivot + 1, end)

    return Sorted


def GravitySort(arr):
    #implmentation of GravitySort(Bead Sort) algorithm
    
    NumOfPoles = max(arr)
    Intermeadiate = []
    Sorted = []

    for Pole in range(NumOfPoles):
        Intermeadiate.append(sum([1 for value in arr if value > Pole]))

    NumOfPoles = max(Intermeadiate)

    for Pole in range(NumOfPoles):
        Sorted.append(sum([1 for value in Intermeadiate if value > Pole]))

    Sorted = Sorted[::-1]

    return Sorted


def CountingSort(arr):
    #implementation of CountingSort algorithm

    maxValue = max(arr)
    count = [0 for x in range(maxValue+1)]
    output = [0 for x in range(len(arr))]

    for index, value in enumerate(arr):
        count[value] += 1

    for index in range(maxValue):
        count[index+1] += count[index]

    for index, value in enumerate(arr):
        output[count[value]-1] = value
        count[value] -= 1

    return output


def RadixLSDSort(arr):
    #implementation of RadixLSDSort(Least Significant Digit) algorithm

    global SortAnimations

    maxValue, minValue = max(arr), min(arr)
    base = 10
    LSD = 1

    while (maxValue - minValue) / LSD >= 1:
        arr = RadixCountSort(arr, LSD, base, minValue)
        SortAnimations.append(arr)
        LSD *= 10

    return arr



def RadixCountSort(arr, LSD, base, minValue):
    #modified counting sort for RadixLSDSort

    count = [0 for x in range(base)]
    output = [0 for x in range(len(arr))]

    for value in arr:
        index = int((value-minValue)/LSD) % base  # grabs digit based on value of base
        count[index] += 1

    for index in range(base-1):
        count[index+1] += count[index]

    for value in reversed(arr):
        index = int((value-minValue)/LSD) % base
        count[index] -= 1
        output[count[index]] = value

    return output


####################################################################################################
#Drawing functions for sorting algorithms

def drawArray(arr, rectwidth, fillcolor):
    #draws an array of rectangles
    
    push()
    #translate to bottom left corner, +x is right, -y is up
    translate(0, height)
    
    for index, value in enumerate(arr):
        #draw rectangle for each element in array
        fill(*fillcolor)
        rect(index*rectwidth, 0, rectwidth, -0.85*value)
    
    pop()
    return


def drawSingleRect(value, index, rectwidth, fillcolor):
    #draws a single rectangle
    
    push()
    #translate to bottom left corner, +x is right, -y is up
    translate(0, height)
    
    #draw rectangle for each element in array
    fill(*fillcolor)
    rect(index*rectwidth, 0, rectwidth, -0.85*value)
    
    pop()
    return


# def drawPreSort(arr):
#     push()
#     pop()
#     return


# def drawPostSort(arr):
#     push()
#     pop()
#     return


def DrawBubble():
    #animates BubbleSort algorithm
    
    global ArrayToSort, SortAnimations, AnimationIndex, isAnimating, ReadyToSort, rectwidth

    #if there are no animations to animate, draw current array
    if len(SortAnimations) == 0:
        drawArray(ArrayToSort, rectwidth, [255])
        
    else:
        #array has been sorted
        
        #check if sorting animation has been completed. if finished, reset animation index and flag
        if AnimationIndex > len(SortAnimations)-1:
            isAnimating = False
            AnimationIndex = 0
            backIndex = 0
        
        #check if sort animation is in progress    
        if isAnimating:
            #draw current array
            drawArray(ArrayToSort, rectwidth, [255])

            #get current animation variables
            Animation = SortAnimations[AnimationIndex]
            
            #color in indices being compared
            
            translate(0, height)
            
            #set color to green
            fill(0, 255, 0)
            #if the values being compared are out of order, set color to red
            if Animation[2]:
                fill(255, 0 , 0)
        
            #draw two rectangles being compared
            rect(Animation[0]*rectwidth, 0, rectwidth, -0.85*ArrayToSort[Animation[0]])
            rect(Animation[1]*rectwidth, 0, rectwidth, -0.85*ArrayToSort[Animation[1]])
            
            translate(0, - height)

            #if the values being compared are out of order, swap values
            if Animation[2]:
                ArrayToSort = swap(ArrayToSort, Animation[0], Animation[1])
                   
            AnimationIndex +=1
            
        else:
            #animation has finished, color final sorted array green
            drawArray(ArrayToSort, rectwidth, [0, 255, 0])

    return


def DrawMerge():
    #animates recursive MergeSort algorithm
    
    global ArrayToSort, SortAnimations, AnimationIndex, isAnimating, ReadyToSort, rectwidth, MergeCount, prevStart
    
    #if there are no animations to animate, draw current array
    if len(SortAnimations) == 0:
        drawArray(ArrayToSort, rectwidth, [255])
        
    else:
        #array has been sorted
        
        #check if sorting animation has been completed. if finished, reset animation index and flag
        if AnimationIndex > len(SortAnimations)-1:
            isAnimating = False
            AnimationIndex = 0
            backIndex = 0
        
        #check if sort animation is in progress
        if isAnimating:
            if AnimationIndex == 0:
                prevStart = 0
            #draw current array
            drawArray(ArrayToSort, rectwidth, [255])
            
            #get current animation variables
            Animation = SortAnimations[AnimationIndex]
            LeftStart = Animation[0]
            RightEnd = Animation[1]
            indexOG = Animation[2]
            indexNew = Animation[3]
            Value = Animation[4]
            
            #color start and end rectangles red
            drawSingleRect(ArrayToSort[LeftStart], LeftStart, rectwidth, [255, 0, 0])
            drawSingleRect(ArrayToSort[RightEnd], RightEnd, rectwidth, [255, 0, 0])
            
            #color value being moved
            drawSingleRect(ArrayToSort[indexOG], indexOG, rectwidth, [255, 0, 0])
            
            #add the value being moved to it's new position in array
            ValueToMove = ArrayToSort.pop(indexOG)
            ArrayToSort.insert(indexNew, ValueToMove)
            
            AnimationIndex +=1
            
            #used to keep track of how many values have been merged
            if LeftStart == prevStart:
                MergeCount +=1
            else:
                MergeCount = 0
                
            #color all the merged values green
            greenArray = [0 for x in range(LeftStart)] + ArrayToSort[LeftStart:LeftStart + MergeCount]
            drawArray(greenArray, rectwidth, [0, 255, 0])
            prevStart = LeftStart  
            
        else:
            #animation has finished, color final sorted array green
            drawArray(ArrayToSort, rectwidth, [0, 255, 0])

            
    return


def DrawQuick():
    #animates recursive QuickSort algorithm
    
    global ArrayToSort, SortAnimations, AnimationIndex, isAnimating, ReadyToSort, rectwidth, MergeCount, prevStart
    
    #if there are no animations to animate, draw current array
    if len(SortAnimations) == 0:
        drawArray(ArrayToSort, rectwidth, [255])
        
    else:
        #array has been sorted
        
        #check if sorting animation has been completed. if finished, reset animation index and flag
        if AnimationIndex > len(SortAnimations)-1:
            isAnimating = False
            AnimationIndex = 0
        
        #check if sort animation is in progress
        if isAnimating:
            if AnimationIndex == 0:
                prevStart = 0
            #draw current array
            drawArray(ArrayToSort, rectwidth, [255])
            
            #get current animation variables
            Animation = SortAnimations[AnimationIndex]
            LeftStart = Animation[0]
            RightEnd = Animation[1]
            pivotIndex = Animation[2]
            i = Animation[3]
            j = Animation[4]
            
            #color start and end rectangles red
            drawSingleRect(ArrayToSort[LeftStart], LeftStart, rectwidth, [255, 0, 0])
            drawSingleRect(ArrayToSort[RightEnd], RightEnd, rectwidth, [255, 0, 0])
            
            #color pivot rectangle blue
            drawSingleRect(ArrayToSort[pivotIndex], pivotIndex, rectwidth, [0, 0, 255])
            
            #color rectangles being swapped
            drawSingleRect(ArrayToSort[i], i, rectwidth, [255, 0, 0])
            drawSingleRect(ArrayToSort[j], j, rectwidth, [255, 0, 0])
            
            swap(ArrayToSort, i, j)
            
            AnimationIndex +=1
            
            #used to keep track of how many values have been merged
            if LeftStart == prevStart:
                MergeCount +=1
            else:
                MergeCount = 0
            """        
            greenArray = [0 for x in range(LeftStart)] + ArrayToSort[LeftStart:LeftStart + MergeCount]
            drawArray(greenArray, rectwidth, [0, 255, 0])
            """
            prevStart = LeftStart  
            
        else:
            #animation has finished, color final sorted array green
            drawArray(ArrayToSort, rectwidth, [0, 255, 0])

    return


def DrawGravity():
    #animates GravitySort(Bead Sort) algorithm
    
    global ArrayToSort, SortedArray, isAnimating, ReadyToSort, rectwidth, AnimationIndex
    
    #if there are no animations to animate, draw current array
    if len(SortedArray) == 0:
        #draw the unsorted array
        drawArray(ArrayToSort, rectwidth, [255])
        
    else:
        #array has been sorted
        
        #check if sorting animation has been completed. if finished, reset animation flag
        if ArrayToSort == SortedArray:
            isAnimating = False
            AnimationIndex = 0
        
        #check if sort animation is in progress    
        if isAnimating:
            #animate scaning through array
            if AnimationIndex < len(ArrayToSort):
                drawArray(ArrayToSort, rectwidth, [255])
                drawSingleRect(ArrayToSort[AnimationIndex], AnimationIndex, rectwidth, [0, 0, 255])
                AnimationIndex +=1
               
            #animate values transforming to sorted values 
            else:
                #draw current array
                drawArray(ArrayToSort, rectwidth, [255])
                
                #go through array, if current value is the sorted value, color green,
                #if value is not the sorted value, color red and add/subtract 1 from value
                for index, value in enumerate(ArrayToSort):
                    if value == SortedArray[index]:
                        drawSingleRect(ArrayToSort[index], index, rectwidth, [0, 255, 0])
                    elif value > SortedArray[index]:
                        ArrayToSort[index] -= 1
                        drawSingleRect(ArrayToSort[index], index, rectwidth, [255, 0, 0])
                    else:
                        ArrayToSort[index] += 1
                        drawSingleRect(ArrayToSort[index], index, rectwidth, [255, 0, 0])
            
        else:
            #animation has finished, color final sorted array green
            drawArray(ArrayToSort, rectwidth, [0, 255, 0])

    return


def DrawCounting():
    #animates CountingSort algorithm
    
    global ArrayToSort, SortedArray, isAnimating, ReadyToSort, rectwidth, AnimationIndex, CountingIndex
    
    #if there are no animations to animate, draw current array
    if len(SortedArray) == 0:
        #draw the unsorted array
        drawArray(ArrayToSort, rectwidth, [255])
    else:
        #array has been sorted
        
        #check if sorting animation has been completed. if finished, reset animation flag
        if ArrayToSort == SortedArray:
            isAnimating = False
            AnimationIndex = 0
            CountingIndex = 0
        
        #check if sort animation is in progress    
        if isAnimating:
            
            #animate scaning through array
            if AnimationIndex < len(ArrayToSort):
                drawArray(ArrayToSort, rectwidth, [255])
                drawSingleRect(ArrayToSort[AnimationIndex], AnimationIndex, rectwidth, [0, 0, 255])
                AnimationIndex +=1
                
            #animate rewriting array to the sorted values
            elif CountingIndex < len(ArrayToSort): 
                ArrayToSort[CountingIndex] = SortedArray[CountingIndex]
                drawArray(ArrayToSort, rectwidth, [255])
                drawSingleRect(ArrayToSort[CountingIndex], CountingIndex, rectwidth, [0, 0, 255])
                
                greenArray = ArrayToSort[:CountingIndex] + [0 for x in range(len(ArrayToSort)-CountingIndex)]
                drawArray(greenArray, rectwidth, [0, 255, 0])
                
                CountingIndex +=1
                
        else:
            #animation has finished, color final sorted array green
            drawArray(ArrayToSort, rectwidth, [0, 255, 0])
    return


def DrawRadixLSD():
    #animates RadixLSD algorithm
    
    global ArrayToSort, SortedArray, isAnimating, ReadyToSort, rectwidth, AnimationIndex, CountingIndex
    
    NumOfLoops = 2*len(SortAnimations)
    
    #if there are no animations to animate, draw current array
    if len(SortedArray) == 0:
        #draw the unsorted array
        drawArray(ArrayToSort, rectwidth, [255])
    else:
        #array has been sorted
        
        #check if sorting animation has been completed. if finished, reset animation flag
        if ArrayToSort == SortedArray:
            isAnimating = False
            AnimationIndex = 0
            CountingIndex = 0
        
        #check if sort animation is in progress
        if isAnimating:
            drawArray(ArrayToSort, rectwidth, [255])

            #animate scaning through array
            if CountingIndex % 2 == 0:
                drawSingleRect(ArrayToSort[AnimationIndex], AnimationIndex, rectwidth, [0, 0, 255])
               
            #animate rewriting array to the next set of sorted values     
            else:
                ArrayToSort[AnimationIndex] = SortAnimations[int(CountingIndex/2)][AnimationIndex]
                drawSingleRect(ArrayToSort[AnimationIndex], AnimationIndex, rectwidth, [0, 0, 255])
                
            AnimationIndex +=1
            
            if AnimationIndex == len(ArrayToSort):
                AnimationIndex = 0
                CountingIndex +=1              
             
        else:
            #animation has finished, color final sorted array green
            drawArray(ArrayToSort, rectwidth, [0, 255, 0])
    
    return
