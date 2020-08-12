def swap(arr, ia, ib):
    arr[ia], arr[ib] = arr[ib], arr[ia]
    return arr



def BubbleSort(arr):
    #number of items in array
    n = len(arr)
    
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            a = arr[j]
            b = arr[j + 1]
            
            if a > b:
                arr = swap(arr, j, j + 1)
    return arr
