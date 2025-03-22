import unittest
from classes import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
    
    def test_maze_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_entrance_and_exit()
        self.assertEqual(
            m1._cells[0][0].has_left_wall,
            True,
        )
        self.assertEqual(
            m1._cells[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            m1._cells[num_cols - 1][num_rows - 1].has_right_wall,
            True,
        )
        self.assertEqual(
            m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall,
            False,
        )

    def test_break_walls(self):
        # Create a small maze with a fixed seed for deterministic testing
        maze = Maze(0, 0, 3, 3, 10, 10, seed=42)
        
        # Initially, all cells should be unvisited and have all walls
        for i in range(maze._num_cols):
            for j in range(maze._num_rows):
                self.assertFalse(maze._cells[i][j].visited)
                self.assertTrue(maze._cells[i][j].has_left_wall)
                self.assertTrue(maze._cells[i][j].has_right_wall)
                self.assertTrue(maze._cells[i][j].has_top_wall)
                self.assertTrue(maze._cells[i][j].has_bottom_wall)
        
        # Call the method we're testing
        maze._break_walls_r(0, 0)
        
        # After breaking walls:
        # 1. All cells should be visited
        for i in range(maze._num_cols):
            for j in range(maze._num_rows):
                self.assertTrue(maze._cells[i][j].visited, f"Cell ({i}, {j}) was not visited")
        
        # 2. There should be a path from start to end
        # This is harder to test directly, but we can check that not all walls remain
        walls_broken = False
        for i in range(maze._num_cols):
            for j in range(maze._num_rows):
                cell = maze._cells[i][j]
                if (not cell.has_left_wall or not cell.has_right_wall or 
                    not cell.has_top_wall or not cell.has_bottom_wall):
                    walls_broken = True
                    break
        
        self.assertTrue




if __name__ == "__main__":
    unittest.main()