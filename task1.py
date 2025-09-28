def find_min_max(arr, left, right):
    if left == right:
        return arr[left], arr[left]

    if right == left + 1:
        if arr[left] < arr[right]:
            return arr[left], arr[right]
        else:
            return arr[right], arr[left]

    mid = (left + right) // 2
    min1, max1 = find_min_max(arr, left, mid)
    min2, max2 = find_min_max(arr, mid + 1, right)

    return min(min1, min2), max(max1, max2)


def get_min_max(arr):
    if not arr:
        raise ValueError("Array must not be empty")
    return find_min_max(arr, 0, len(arr) - 1)


test_arrays = [
    [5],
    [7, 3],
    [3, 7, 1, 9, 4, -2, 6],
    [10, 10, 10, 10],
    [-5, -9, -3, -11, -1],
    [100, 2, 300, 40, 5],       
    [8, 1, 8, 2, 8, 3, 8, 4],
    [0, 0, 0, 1],    
    [999, -1000, 500, 1000],
    list(range(20, 0, -1))     
]

for arr in test_arrays:
    print(f"{arr}  min/max:  {get_min_max(arr)}")
