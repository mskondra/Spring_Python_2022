# n*log(n)
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        numbers = sorted(enumerate(numbers), key=lambda i: i[1])
        a = 0
        b = len(numbers) - 1
        while a < b:
            s = numbers[a][1] + numbers[b][1]
            if s > target:
                b -= 1
            if s < target:
                a += 1
            if s == target:
                return numbers[a][0], numbers[b][0]