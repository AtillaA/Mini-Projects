class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        # get the dimensions of the board (length = rows, length of the first row = cols)
        ROWS, COLS = len(board), len(board[0])
        path = set() # to add all the positions that are currently in the path (traveled)

        # nested to prevent passing in the local variables
        def dfs(r, c, i): # i = current letter in the target word we are looking for
            if i == len(word): # if the entire word is achieved
                return True
            
            if (r < 0 or c < 0 or r >= ROWS or c >= COLS or 
                word[i] != board[r][c] or (r, c) in path): # out of bounds/edge conditions
                return False

            path.add((r, c)) # when the character is found, add the current position to the path
            res = (dfs(r + 1, c, i + 1) or  # recursive call for all adjacent cells, correct adjacent cell(s) will return true
                   dfs(r - 1, c, i + 1) or  # res will be true if any of the adjacent cells contain the next letter
                   dfs(r, c + 1, i + 1) or 
                   dfs(r, c - 1, i + 1))
            
            path.remove((r, c)) # remove the most recent position since it will no longer be visited
            return res

        for r in range(ROWS):
            for c in range(COLS):
                if dfs(r, c, 0): return True # go through all elements, dfs returns true once the expected word is achieved
        
        return False

        # time complexity = O( m * n * dfs ) = O ( m * n * 4^len(word))
