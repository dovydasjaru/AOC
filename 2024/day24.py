import copy


INPUT_WIRE_SIZE = 45


def SimulateSingleGate(input1: bool, input2: bool, operation: str) -> bool:
    match operation:
        case "AND":
            return input1 and input2
        case "OR":
            return input1 or input2
        case "XOR":
            return input1 != input2
    
    raise Exception("Received unexected opration")


def SimulateGates(wires: dict[str, bool], gates: list[str]):
    while len(gates) > 0:
        i = 0
        while i < len(gates):
            gate = gates[i].split(" ")
            if wires.get(gate[0], None) != None and wires.get(gate[2], None) != None:
                wires[gate[4]] = SimulateSingleGate(wires[gate[0]], wires[gate[2]], gate[1])
                gates.pop(i)
                i -= 1

            i += 1


def DecodeNumber(wires: dict[str, bool], wireToDecode: str) -> int:
    result = 0
    wireNumber = 0
    decodedWire = wireToDecode + "{:02d}"
    while wires.get(decodedWire.format(wireNumber), None) != None:
        wire = wires[decodedWire.format(wireNumber)]
        result += int(wire) * (2 ** wireNumber)
        wireNumber += 1
    
    return result


def DictionariseGates(gates: list[str]) -> dict[str, list[str]]:
    gatesDict: dict[str, list[str]] = {}
    for gate in gates:
        parts = gate.split(" ")
        gatesDict[parts[0]] = gatesDict.get(parts[0], [])
        gatesDict[parts[0]].append(gate)
        gatesDict[parts[2]] = gatesDict.get(parts[2], [])
        gatesDict[parts[2]].append(gate)
        gatesDict[parts[4]] = gatesDict.get(parts[4], [])
        gatesDict[parts[4]].append(gate)
    
    return gatesDict


def SwapOutputs(gates: dict[str, list[str]], output1: str, output2: str):
    badGate1: str | None = None
    for gate in gates[output1]:
        if gate.split(" ")[4] == output1:
            badGate1 = gate
            break
    badGate2: str | None = None
    for gate in gates[output2]:
        if gate.split(" ")[4] == output2:
            badGate2 = gate
            break

    if badGate1 == None or badGate1 == None:
        raise Exception("Did not find gates with " + output1 + " and " + output2 + " outputs when swapping outputs.")
    
    badGate1Parts = badGate1.split(" ")
    badGate2Parts = badGate2.split(" ")
    gates[output1].remove(badGate1)
    gates[output2].remove(badGate2)
    gates[output2].append(badGate1.split(" -> ")[0] + " -> " + output2)
    gates[output1].append(badGate2.split(" -> ")[0] + " -> " + output1)

    gates[badGate1Parts[0]].remove(badGate1)
    gates[badGate1Parts[0]].append(badGate1.split(" -> ")[0] + " -> " + output2)
    gates[badGate1Parts[2]].remove(badGate1)
    gates[badGate1Parts[2]].append(badGate1.split(" -> ")[0] + " -> " + output2)

    gates[badGate2Parts[0]].remove(badGate2)
    gates[badGate2Parts[0]].append(badGate2.split(" -> ")[0] + " -> " + output1)
    gates[badGate2Parts[2]].remove(badGate2)
    gates[badGate2Parts[2]].append(badGate2.split(" -> ")[0] + " -> " + output1)


def FindGateByOutput(gates: dict[str, list[str]], output: str) -> str:
    for gate in gates[output]:
        parts = gate.split(" ")
        if parts[4] == output:
            return gate
    
    raise Exception("Gate with output " + output + " was not found.")


def FindGateByInputsAndType(gates: dict[str, list[str]], in1: str, in2: str, operation: str) -> str:
    for gate in gates[in1]:
        parts = gate.split(" ")
        if parts[0] in [in1, in2] and parts[2] in [in1, in2] and parts[1] == operation:
            return gate
    
    raise Exception("Gate with inputs " + in1 + " and " + in2 + " and operation " + operation + " was not found.")


def FindGateBySingleInputAndType(gates: dict[str, list[str]], input: str, operation: str) -> str:
    for gate in gates[input]:
        if gate.split(" ")[1] == operation:
            return gate

    raise Exception("Gate with input " + input + " and operation " + operation + " was not found.")


def SwapOutputsInSummation(gates: dict[str, list[str]], wireX: str, wireY: str, wireZ: str, wireCarry: str) -> list[str]:
    swappedWires = []

    zGate = FindGateByOutput(gates, wireZ)
    zGateParts = zGate.split(" ")
    if wireCarry not in [zGateParts[0], zGateParts[2]]:
        badWire = FindGateBySingleInputAndType(gates, wireCarry, "XOR").split(" ")[4]
        swappedWires.append(wireZ)
        swappedWires.append(badWire)
        SwapOutputs(gates, badWire, wireZ)
        zGate = FindGateByOutput(gates, wireZ)
        zGateParts = zGate.split(" ")
    
    inputGate = FindGateByInputsAndType(gates, wireX, wireY, "XOR")
    inputGateParts = inputGate.split(" ")
    if inputGateParts[4] not in [zGateParts[0], zGateParts[2]]:
        badWire = ""
        if wireCarry == zGateParts[0]:
            badWire = zGateParts[2]
        else:
            badWire = zGateParts[0]
        
        swappedWires.append(inputGateParts[4])
        swappedWires.append(badWire)
        SwapOutputs(gates, badWire, inputGateParts[4])

    return swappedWires


def FindSwappedWires(gates: list[str]) -> list[str]:
    gatesDict = DictionariseGates(gates)
    swappedWires: list[str] = []
    # Special zero case
    gate = FindGateByOutput(gatesDict, "z00")
    if gate != "x00 XOR y00 -> z00" and gate != "y00 XOR x00 -> z00":
        swappedWires.append("z00")
        badGate = FindGateByInputsAndType(gatesDict, "x00", "y00", "XOR")
        swappedOutput = badGate.split(" ")[4]
        swappedWires.append(swappedOutput)
        SwapOutputs(gatesDict, "z00", swappedOutput)

    wireCarryIn = FindGateByInputsAndType(gatesDict, "x00", "y00", "AND").split(" ")[4]
    wireX = "x{:02d}"
    wireY = "y{:02d}"
    wireZ = "z{:02d}"
    for wireIndex in range(1, INPUT_WIRE_SIZE):
        swappedWires.extend(SwapOutputsInSummation(gatesDict, wireX.format(wireIndex), wireY.format(wireIndex), wireZ.format(wireIndex), wireCarryIn))
        # Carry part
        inputXorGate = FindGateByInputsAndType(gatesDict, wireX.format(wireIndex), wireY.format(wireIndex), "XOR")
        middleAndGate = FindGateByInputsAndType(gatesDict, inputXorGate.split(" ")[4], wireCarryIn, "AND")
        inputAndGate = FindGateByInputsAndType(gatesDict, wireX.format(wireIndex), wireY.format(wireIndex), "AND")
        inputAndGateParts = inputAndGate.split(" ")
        outputOrGate: str | None = None
        try:
            outputOrGate = FindGateBySingleInputAndType(gatesDict, middleAndGate.split(" ")[4], "OR")
        except:
            outputOrGate = FindGateBySingleInputAndType(gatesDict, inputAndGateParts[4], "OR")
            outputOrGateParts = outputOrGate.split(" ")
            middleAndGateOutput = middleAndGate.split(" ")[4]
            if outputOrGateParts[0] == inputAndGateParts[4]:
                swappedWires.append(outputOrGateParts[2])
                swappedWires.append(middleAndGateOutput)
                SwapOutputs(gatesDict, outputOrGateParts[2], middleAndGateOutput)
            else:
                swappedWires.append(outputOrGateParts[0])
                swappedWires.append(middleAndGateOutput)
                SwapOutputs(gatesDict, outputOrGateParts[0], middleAndGateOutput)
            
            middleAndGate = FindGateByInputsAndType(gatesDict, inputXorGate.split(" ")[4], wireCarryIn, "AND")
        
        outputOrGateParts = outputOrGate.split(" ")

        if inputAndGateParts[4] not in [outputOrGateParts[0], outputOrGateParts[2]]:
            if middleAndGate.split(" ")[4] == outputOrGateParts[0]:
                swappedWires.append(outputOrGateParts[2])
                swappedWires.append(inputAndGateParts[4])
                SwapOutputs(gatesDict, inputAndGateParts[4], outputOrGateParts[2])
            else:
                swappedWires.append(outputOrGateParts[0])
                swappedWires.append(inputAndGateParts[4])
                SwapOutputs(gatesDict, inputAndGateParts[4], outputOrGateParts[0])
            
            inputAndGate = FindGateByInputsAndType(gatesDict, wireX.format(wireIndex), wireY.format(wireIndex), "AND")
            inputAndGateParts = inputAndGate.split(" ")
            
        wireCarryIn = outputOrGate.split(" ")[4]

    # special last case
    if wireCarryIn != wireZ.format(INPUT_WIRE_SIZE):
        swappedWires.append(wireCarryIn)
        swappedWires.append(wireZ.format(INPUT_WIRE_SIZE))
        SwapOutputs(gatesDict, wireCarryIn, wireZ.format(INPUT_WIRE_SIZE))

    return swappedWires


file = open("input24.txt")
line = file.readline()
wires: dict[str, bool] = {}
while line.strip() != "":
    wire = line.strip().split(": ")
    wires[wire[0]] = bool(int(wire[1]))
    line = file.readline()

gates: list[str] = []
for line in file.readlines():
    gates.append(line.strip())

SimulateGates(wires, copy.deepcopy(gates))
print(DecodeNumber(wires, "z"))

swapped = FindSwappedWires(gates)
swapped.sort()
print(",".join(swapped))