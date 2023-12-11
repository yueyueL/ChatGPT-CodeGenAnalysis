class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Create a dictionary to store the indices of numbers as values and 
        # the numbers themselves as keys
        d = {}
        # Use enumerate to loop through the list and keep track of index and value
        for i, num in enumerate(nums):
            # Calculate the complement of num
            complement = target - num
            # Check if the complement is already in the dictionary
            if complement in d:
                # Return the indices of num and its complement
                return [d[complement], i]
            # If complement is not in dictionary, add num to the dictionary with its index as value
            d[num] = i
            # If there is no pair that adds up to target, return an empty list
        return []