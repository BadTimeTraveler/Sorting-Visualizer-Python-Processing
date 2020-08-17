import Sorting_Algorithms as SA

def DrawBubble(ArrayToSort, SortAnimations, AnimationIndex, isAnimating, rectwidth):
    
    
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
            
    return ArrayToSort, SortAnimations, AnimationIndex, isAnimating


def DrawMerge():
    return


def DrawQuick():
    return


def DrawInsertion():
    return


def DrawHeap():
    return


def DrawSelection():
    return


def DrawTest(offsetPercent, controlWidth, controlHeight):
    rect(offsetPercent*controlWidth + 2*controlWidth, 0.55*controlHeight, controlWidth*(1- 2*offsetPercent), 0.35*controlHeight)
    return

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
