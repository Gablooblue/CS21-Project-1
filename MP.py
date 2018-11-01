def lines():
    f = open('input.txt')

    #In assembly we need to keep the \n
        # That way we can tell if it's the end of
        # a line, but for now we'll keep it
    lines = [i.strip('\n') for i in f.readlines()]
    f.close()
    lines = [i[0:i.find('/')] if i.find('/')!=-1 else i for i in lines]
    lines = [i.strip().split(',') for i in lines]
    lines = [i for i in lines if i==[j for j in i if j]]
    lines = [[j.strip() for j in i] for i in lines]
    return lines

def exponent(n, i):
    out = n
    x = i
    if i == 0:
        return 1
    while i > 1:
        out *= n
        i -= 1
    return out

## Converters
def from_base_converter(n, base):
    n = int(n)
    out = 0;
    i = 0;
    while n > 0:
        curr = n %10
        out += exponent(base, i) * curr
        i += 1
        n = n // 10
    return out

def to_base_converter(n, base, digits = 0):
    out = ""
    symbol = ""
    while n > 0:
        remainder = n % base 
        if remainder > 9:
            symbol = chr(remainder - 10 + 97)
        else:
            symbol = str(remainder)
        n = n // base 
        out = symbol + out

    while(len(out) < digits):
        out = "0" + out

    return out


    

def assemble(instructions, group):
  out = ["0" for i in range (0,12)]
  if (group == "converted"):
    return to_base_converter(from_base_converter(instructions[0], 8), 16, 3)
  elif group == "basic":
    out[0:4] = (basic[instructions[0]]) + "0"
    out[4:12] = (to_base_converter(labels[instructions[1].lower()], 2, 8))
  elif group == "basici":
    out[0:4] = (basic[instructions[0]]) + "1"
    out[4:12] = (to_base_converter(labels[instructions[1].lower()], 2, 8))
  elif group == "opr1":
    out[0:4] = "1110"
    if "NOP" in instructions:
      out[4:12] = "00000000"
    if "CLA" in instructions:
      out[4] = "1"
    if "CLL" in instructions:
      out[5] = "1"
    if "CMA" in instructions:
      out[6] = "1"
    if "CML" in instructions:
      out[7] = "1"
    if "RAR" in instructions or "RTR" in instructions:
      out[8] = "1"
    if "RAL" in instructions or "RTL" in instructions:
      out[9] = "1"
    if "RTR" in instructions or "RTL" in instructions:
      out[10] = "1"
    if "IAC" in instructions:
      out[11] = "1"
  elif group == "opr2":
    out[0:4] = "1111"
    if "NOP" in instructions:
      out[4:12] = "00000000"
    if "CLA" in instructions:
      out[4] = "1"
    if "SMA" in instructions or "SPA" in instructions:
      out[5] = "1"
    if "SNA" in instructions or "SZA" in instructions:
      out[6] = "1"
    if "SNL" in instructions or "SZL" in instructions:
      out[7] = "1"
    if ("SPA" in instructions or "SNL" in instructions 
    or "SZL" in instructions):
      out[8] = "1"
    if "HLT" in instructions:
      out[10] = "1"
  return to_base_converter(from_base_converter("".join(out),2), 16, 3)

def identifygroup(instructions):
  length = len(instructions)
  if instructions[0] in basic:
    if instructions[1] == "I":
      return "basici"
    else:
      return "basic"
      
  opr1group = False
  for j in range(0,length):
    if instructions[j] in OPR1:
      opr1group = True
    else:
      opr1group = False
      break    
  opr2group = False
  for j in range(0,length):
    if instructions[j] in OPR2:
      opr2group = True
    else:
      opr2group = False
      break    

  if opr1group:
    return "opr1"
  elif opr2group:
    return "opr2"
  else:
    return "converted"

def writeoutput(output):
  f = open('output.txt','w')
  text = "v2.0 raw\n"
  text += "\n".join(output)
  f.write(text)
  f.close()

inputlines = lines()
currentadd = 0
labels = {}
# [print(i) for i in inputlines]
basic = {"AND": "000", "TAD": "001", "ISZ" : "010", "DCA": "011", 
        "JMS": "100", "JMP": "101", "OUT": "110"}
OPR1 = {"NOP": 0, "CLA": 1, "CLL": 1, "CMA": 2, "CML": 2, "IAC": 3, "RAR": 4, "RAL": 4, "RTR": 4, "RTL": 4}
OPR2 = {"NOP": "N/A", "HLT": "N/A", "CLA": "N/A", "SKP": "N/A", "SMA": "OR", 
        "SZA": "OR","SNL": "OR", "SPA": "AND", "SNA": "AND", "SZL": "AND"}

for i in inputlines:
  if (i[0][0] == '*'):
    currentadd = from_base_converter(i[0][1:4], 8)
    continue
  elif (len(i) > 1):
    labels[i[0].lower()] = currentadd
  elif (i[0][0] == "$"):
    break
  currentadd += 1

output = ["" for i in range(0, currentadd)]

for i in inputlines:
  if (i[0][0] == '*'):
    # Need to make an octal converter
    currentadd = from_base_converter(i[0][1:4], 8)
    continue
  elif (len(i) > 1):
    instructions = i[1].split(' ')
  else:
    instructions = i[0].split(' ')

  if instructions[0] == "$":
    break
  else:
    output[currentadd] = assemble(instructions, identifygroup(instructions))
  currentadd += 1

writeoutput(output)

