def swap(arr, ia, ib):
    arr[ia], arr[ib] = arr[ib], arr[ia]
    return arr


def BubbleSort(arr):
    #number of items in array
    n = len(arr)
    animations = []
    
    for i in range(n):
        for j in range(n-i-1):
            a = arr[j]
            b = arr[j+1]            

            if a > b:
                arr = swap(arr, j, j+1)   
            animations.append([j, j+1, a > b])

    return animations


def MergeSort(arr):
    return arr


def QuickSort(arr):
    return arr


def InsertionSort(arr):
    return arr


def HeapSort(arr):
    return arr


def SelectionSort(arr):
    return arr
