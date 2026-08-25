import collections

class Processor:
    """Creative data processor with reorganization via deque operations."""

    def __init__(self, raw_data):
        self._data = collections.deque(raw_data)

    def _deduplicate(self, data):
        counts = collections.Counter(data)
        return [item for item in data if counts[item] == 1]

    def cleanup(self):
        temp = [x for x in self._data if x]
        self._data = collections.deque(self._deduplicate(temp))
        return self

    def reorganize(self):
        if not self._data:
            return self
        lst = list(self._data)
        mid = len(lst) // 2
        first_half = lst[:mid][::-1]
        second_half = lst[mid:]
        interleaved = []
        for i in range(max(len(first_half), len(second_half))):
            if i < len(first_half):
                interleaved.append(first_half[i])
            if i < len(second_half):
                interleaved.append(second_half[i])
        self._data = collections.deque(interleaved)
        return self

    def apply(self, operation):
        self._data = collections.deque(operation(item) for item in self._data)
        return self

    def finalize(self):
        return list(self._data)

def main():
    sample = [0, 1, 2, 2, 3, 4, 5, 0, 6, 7, 7, 8]
    p = Processor(sample)
    result = p.cleanup().reorganize().apply(lambda x: x + 10).finalize()
    print(result)

if __name__ == "__main__":
    main()