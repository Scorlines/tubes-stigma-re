from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from collections import deque


#Membuat class bot dengan nama MpokZen
class MpokZenBot(BaseLogic):
    def __init__(self):
        self.diamonds = [] #Tempat menyimpan lokasi diamond yg ada
        self.obstacles = set() #Tempat menyimpan rintangan yg ada pada peta

    #fungsi mendapatkan objek peta 
    def get_objects(self, board: Board):
        self.diamonds = [] #Tempat menyimpan diamond yg diambil
        self.obstacles = set() #Set obstacles untuk ditandai

        #Perulangan melihat kondisi/objek pada peta
        for object in board.game_objects:
            if object.type in ["DiamondGameObject", "DiamondButtonGameObject"]: #Jika objek adalah diamon
                self.diamonds.append(object) #Menyimpan posisi diamond 
            elif object.type in ["BotGameObject", "WallGameObject"]: #Jika objek adalah rintangan
                self.obstacles.add((object.position.x, object.eposition.y)) #Menyimpan posisi rintangan

    #Algoritma BFS. Mencari jarak terbaik
    def bfs(self, start: Position, goal: Position, board: Board) -> int:
        visited = set()
        queue = deque([(start.x, start.y, 0)]) 
        visited.add((start.x, start.y))

        #Antrian untuk menjelajahi peta
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

    #Fungsi untuk menentukan langkah bot
    def next_move(self, board_bot: GameObject, board: Board):
        #Mengambil seluruh informasi pada peta
        self.get_objects(board)
 
        #Data bot
        my_pos = board_bot.position #Posisi bot saat ini
        inventory = board_bot.properties.diamonds #Deklarasi untuk menyimpan diamon yg sudah diambil
        capacity = board_bot.properties.inventory_size #Untuk kapasitas tas
        space_left = capacity - inventory #Menghitung sisa kapasitas pada tas
  

        best_target = None
        best_ratio = -1
        best_distance = float('inf')

        #Algoritma ratio 
        for diamond in self.diamonds:
            if diamond.properties.points is not None and diamond.properties.points <= space_left:
                dist = self.bfs(my_pos, diamond.position, board)
                if dist != float('inf'):
                    ratio = diamond.properties.points / dist #Menghitung ratio
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_target = diamond
                        best_distance = dist

        if best_target is None:
            target = board_bot.properties.base #Logika untuk bot kembali pada base
        else:
            target = best_target.position #Logika untuk pergerakan bot menuju diamond terbaik

        dx, dy = 0, 0
        if my_pos.x < target.x:
            dx = 1 #Pergerakan ke kakan
        elif my_pos.x > target.x:
            dx = -1 #Pergerakan ke kiri
        elif my_pos.y < target.y:
            dy = 1 #Pergerakan ke bawah
        elif my_pos.y > target.y:
            dy = -1 #Pergerakan ke atas

        return dx, dy #Mengembalikan arah gerak
