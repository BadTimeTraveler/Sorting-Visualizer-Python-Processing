# Sorting Visualizer
Sorting visualizer written in Python 2.7 in the Processing environment. Generate random arrays between 11 and 645 elements long and choose between 6 different sorting algorithms.

## How To Use
Download the appropriate executable folder(32 vs 64) and run the "Sorting_Visualizer.exe" inside.
Additionally, if you have Processing 3 and the Python Mode extension installed then you can run the "Sorting_Visualizer.pyde" file to open the Processing sketchbook for this project.

Begin by selecting the array size and framerate using the two center scrollbars. Larger array sizes and lower framerates will increase the sorting time. Next, click on a sorting algorithm in the top right and then click the "Start Sorting" button in the top left to being animating the algorithm.

## Algorithms
[Bubble Sort](https://en.wikipedia.org/wiki/Bubble_sort): Simplistic sorting algorithm where adjacent elements are compared and then swapped if they're in the wrong order

[Merge Sort](https://en.wikipedia.org/wiki/Merge_sort): Efficient divide and conquer algorithm, splits the array is smaller and smaller sub-arrays which are then sorted and merged recursively

[Quick Sort](https://en.wikipedia.org/wiki/Quicksort): Efficient divide and conquer algorithm, recursively splits the array around a pivot and then swaps values in the sub-arrays according to whether they are less than or greater than the pivot.

[Gravity(Bead) Sort](https://en.wikipedia.org/wiki/Bead_sort): Natural sorting algorithm, trades space complexity, O(n<sup>2</sup>), for time complexity, O(n).

[Counting Sort](https://en.wikipedia.org/wiki/Counting_sort): Integer sorting algorithm, counts the number of distinct values and then uses arithmetic to determine the final position of each value.

[RadixLSD Sort](https://en.wikipedia.org/wiki/Radix_sort): Sorts values by their radix(base) using counting sort for each radix. Starts with the Least Significant Digit and finishes with the Most Significant Digit.

## Demo

### Quick Sort

![github](Gifs/Quick.gif)

### Merge Sort

![github](Gifs/Merge.gif)
