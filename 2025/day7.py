def countSplitters(diagram: list[str]) -> int:
  count = 0
  beams: set[int] = set()
  beams.add(diagram[0].find("S"))
  for line in diagram[1:]:
    newBeams: set[int] = set()
    for beam in beams:
      if line[beam] == "^":
        count += 1
        newBeams.add(beam - 1)
        newBeams.add(beam + 1)
      else:
        newBeams.add(beam)

    beams = newBeams

  return count


def countTimelines(diagram: list[str]) -> int:
  timelines: dict[int, int] = {}
  timelines[diagram[0].find("S")] = 1
  for line in diagram[1:]:
    newTimelines: dict[int, int] = {}
    for timeline, timelineCount in timelines.items():
      if line[timeline] == "^":
        newTimelines[timeline - 1] = newTimelines.get(timeline - 1, 0) + timelineCount
        newTimelines[timeline + 1] = newTimelines.get(timeline + 1, 0) + timelineCount
      else:
        newTimelines[timeline] = newTimelines.get(timeline, 0) + timelineCount
    
    timelines = newTimelines
  
  return sum(timelines.values())



diagram = [line.strip() for line in open("input7.txt").readlines()]
print(countSplitters(diagram))
print(countTimelines(diagram))