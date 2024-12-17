import copy

WIDTH = 101
HEIGHT = 103


def PrintRobotMap(robotMap: list[list[int]]):
    for line in robotMap:
        print(''.join(['.' if x == 0 else str(x) for x in line]))


def PrintRobotMapForTree(robotMap: list[list[int]]):
    for line in robotMap:
        print(''.join([' ' if x == 0 else '#' for x in line]))


class Robot:
    def __init__(self, position: tuple[int], velocity: tuple[int]):
        self.position = position
        self.velocity = velocity


def Simulate(robots: list[Robot], amount: int):
    for robot in robots:
        y = (robot.position[0] + robot.velocity[0] * amount) % HEIGHT
        x = (robot.position[1] + robot.velocity[1] * amount) % WIDTH
        robot.position = (y, x)


def PutRobotsOnMap(robots: list[Robot], robotMap: list[list[int]]):
    for robot in robots:
        robotMap[robot.position[0]][robot.position[1]] += 1


def CaculateSafety(robotMap: list[list[int]]) -> int:
    heightMiddle = int((HEIGHT - 1) / 2)
    widthMiddle = int((WIDTH - 1) / 2)
    quadrant1 = [robotMap[i][:widthMiddle] for i in range(heightMiddle)]
    quadrant2 = [robotMap[i][widthMiddle + 1:] for i in range(heightMiddle)]
    quadrant3 = [robotMap[i][:widthMiddle] for i in range(heightMiddle + 1, HEIGHT)]
    quadrant4 = [robotMap[i][widthMiddle + 1:] for i in range(heightMiddle + 1, HEIGHT)]
    safetyFactor = 1
    for quadrant in [quadrant1, quadrant2, quadrant3, quadrant4]:
        robotCount = 0
        for i in range(heightMiddle):
            for j in range(widthMiddle):
                robotCount += quadrant[i][j]
        
        safetyFactor *= robotCount

    return safetyFactor


robotMap: list[list[int]] = []
for _ in range(HEIGHT):
    robotMap.append([0] * WIDTH)

robots: list[Robot] = []
for line in open("input14.txt").readlines():
    line = line.strip().split(" v=")
    line[0] = line[0][2:]
    position = list(map(int, line[0].split(",")))
    velocity = list(map(int, line[1].split(",")))
    robots.append(Robot((position[1], position[0]), (velocity[1], velocity[0])))

oRobots = copy.deepcopy(robots)
oRobotMap = copy.deepcopy(robotMap)

Simulate(robots, 100)
PutRobotsOnMap(robots, robotMap)
print(CaculateSafety(robotMap))

# Second part is printing every second, until christmas tree is found. Used website to get approximate answer for where to search. Mine was 7338
seconds = 6999
robots = oRobots
Simulate(robots, seconds)
while True:
    robotMap = copy.deepcopy(oRobotMap)
    PutRobotsOnMap(robots, robotMap)
    PrintRobotMapForTree(robotMap)
    print("This maps iteration: ", seconds)
    Simulate(robots, 1)
    seconds += 1
    input("Press Enter to continue...")