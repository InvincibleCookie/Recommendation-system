def get_array_window(arr: list, skip: int, leng: int):
    if skip >= len(arr):
        return []

    return arr[skip:min(len(arr), skip + leng)]

