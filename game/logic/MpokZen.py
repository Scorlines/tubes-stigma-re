from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from collections import deque

class MpokZenBot(BaseLogic):
    def __init__(self):
        self.diamonds = []
        self.obstacles = set()

    def get_objects(self, board: Board):
        self.diamonds = []
        self.obstacles = set()

        for obj in board.game_objects:
            if obj.type in ["DiamondGameObject", "DiamondButtonGameObject"]:
                self.diamonds.append(obj)
            elif obj.type in ["BotGameObject", "WallGameObject"]:
                self.obstacles.add((obj.position.x, obj.position.y))

    def bfs(self, start: Position, goal: Position, board: Board) -> int:
        visited = set()
        queue = deque([(start.x, start.y, 0)]) 
        visited.add((start.x, start.y))

        while queue:
            x, y, dist = queue.popleft()
            if (x, y) == (goal.x, goal.y):
                return dist
            
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board.width and 0 <= ny < board.height:
                    if (nx, ny) not in visited and (nx, ny) not in self.obstacles:
                        queue.append((nx, ny, dist + 1))
                        visited.add((nx, ny))
        return float('inf') 

    def next_move(self, board_bot: GameObject, board: Board):
        self.get_objects(board)

        my_pos = board_bot.position
        inventory = board_bot.properties.diamonds
        capacity = board_bot.properties.inventory_size
        space_left = capacity - inventory
  

        best_target = None
        best_ratio = -1
        best_distance = float('inf')

        for diamond in self.diamonds:
            if diamond.properties.points is not None and diamond.properties.points <= space_left:
                dist = self.bfs(my_pos, diamond.position, board)
                if dist != float('inf'):
                    ratio = diamond.properties.points / dist
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_target = diamond
                        best_distance = dist

        if best_target is None:
            target = board_bot.properties.base
        else:
            target = best_target.position

        dx, dy = 0, 0
        if my_pos.x < target.x:
            dx = 1
        elif my_pos.x > target.x:
            dx = -1
        elif my_pos.y < target.y:
            dy = 1
        elif my_pos.y > target.y:
            dy = -1

        return dx, dy
