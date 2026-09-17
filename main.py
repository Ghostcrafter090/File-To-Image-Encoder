import modules.pytools as pytools
import cv2
import numpy as np
import math
import unireedsolomon as rs

# testData = pytools.IO.getBytes(".\\62839252.jpg")

# Encodes the file in an image
def convertDataToFrame(data: bytes, xMax=320, yMax=480, analogDepth=3, errorCorrectionBlockSize=192, returnBytes=False, encodeColor=False):
    
    # Take original data and encode with error correction
    dataErrorEncoded = b''
    errorHandler = rs.RSCoder(errorCorrectionBlockSize, int(errorCorrectionBlockSize - (errorCorrectionBlockSize / 8)))
    i = 0
    while i < len(data):
        dataErrorEncoded = dataErrorEncoded + errorHandler.encode(data[i:i + int(errorCorrectionBlockSize - (errorCorrectionBlockSize / 8))]).encode(encoding="latin-1") # using latin-1 here bc it maps all 0-255 char characters and decodes without error
        i = i + int(errorCorrectionBlockSize - (errorCorrectionBlockSize / 8))
        
        print("Error Correction Encoding Percent: " + str(int(i / len(data) * 100)))
    
    # Store blockSize and rawChunkSize as 8bit integers at the start of the encoding    
    dataErrorEncoded = chr(errorCorrectionBlockSize).encode(encoding="latin-1") + chr(int(errorCorrectionBlockSize - (errorCorrectionBlockSize / 8))).encode(encoding="latin-1") + dataErrorEncoded
    
    print("Block Size: " + str(ord(dataErrorEncoded.decode(encoding="latin-1")[0])))
    print("Base Block Size: " + str(ord(dataErrorEncoded.decode(encoding="latin-1")[1])))
    
    if not encodeColor:
        print("Image Data Size: " + str((xMax / 2) * (yMax / 2) * analogDepth))
    else:
        print("Image Data Size: " + str((xMax / 2) * (yMax / 12) * analogDepth * 3))
        
    print("Data Size: " + str(len("".join(f"{byte:08b}" for byte in dataErrorEncoded))))
    
    
    # Return raw error encoded data (for debugging)
    if returnBytes:
        out = ""
        for byte in dataErrorEncoded:
            out = out + f"{byte:08b}"
            
        return out
    
    # Blank Image
    encodedImage = np.zeros((xMax, yMax, 3), dtype=np.uint8)
    
    # Seperate data into individual luma codes for each pixel in bin format
    output = [""]
    i = 0
    while (i < len(dataErrorEncoded)):
        byteData = f"{dataErrorEncoded[i]:08b}"
        
        for bit in byteData:
            if len(output[-1]) >= (analogDepth * (1 + (encodeColor * 2))):
                output.append("")
            output[-1] = output[-1] + bit
            
        dataErrorEncoded = dataErrorEncoded[1:]
        
    output[-1] = output[-1] + ("0" * ((analogDepth * (1 + (encodeColor * 2))) - len(output[-1])))

    # Encode each luma code into the image
    # Note: each bit is technically 2x2 pixels instead of just one, greatly improves error handling when compressed or distorted
    x = 0
    y = 0
    while (y < yMax):
        if (int((int(x) + int(math.floor(y / 2) * (xMax))) / 2) < len(output)) or (encodeColor and (int((int(x) + int(math.floor(y / 12) * (xMax))) / 2) < len(output))):
            if not encodeColor:
                encodedImage[x, y] = [(int(output[int((int(x) + int(math.floor(y / 2) * (xMax))) / 2)], 2) * int(256 / (2 ** analogDepth))) + int(256 / (2 ** analogDepth) / 2)] * 3
            else:
                try:
                    encodedImage[x, y] = [(int(output[int((int(x) + int(math.floor(y / 12) * (xMax))) / 2)][0:analogDepth], 2) * int(256 / (2 ** analogDepth))) + int(256 / (2 ** analogDepth) / 2), (int(output[int((int(x) + int(math.floor(y / 12) * (xMax))) / 2)][analogDepth:analogDepth * 2], 2) * int(256 / (2 ** analogDepth))) + int(256 / (2 ** analogDepth) / 2), (int(output[int((int(x) + int(math.floor(y / 12) * (xMax))) / 2)][analogDepth * 2:analogDepth * 3], 2) * int(256 / (2 ** analogDepth))) + int(256 / (2 ** analogDepth) / 2)]
                except:
                    print(output[int((int(x) + int(math.floor(y / 12) * (xMax))) / 2)])
        x = x + 1
        if x >= xMax:
            x = 0
            y = y + 1

    return encodedImage

# Decodes image/frame back into file
# analogDepth and blockSize are manually passed rn for testing, will change and include analog depth in initial header encoding
def convertFrameToData(inputImageFileName, analogDepth, errorCorrectionBlockSize=192, returnBytes=False):
    encodedImage = cv2.imread(inputImageFileName)
    dictData = {}
    
    # Take each pixel, and store in dictionary of lists containing the 4 2x2 pixels of each bit. Avergaging the rgb channels to get as close to the original luma value as possible
    x = 0
    y = 0
    while (y < encodedImage.shape[1]):
        
        if int((int(x) + int(math.floor(y / 2) * (encodedImage.shape[0]))) / 2) not in dictData:
            dictData[int((int(x) + int(math.floor(y / 2) * (encodedImage.shape[0]))) / 2)] = []
            
        dictData[int((int(x) + int(math.floor(y / 2) * (encodedImage.shape[0]))) / 2)].append(sum(encodedImage[x, y][0:2].astype(int)) / len(encodedImage[x, y][0:2].astype(int)))
        x = x + 1
        if x >= encodedImage.shape[0]:
            x = 0
            y = y + 1
    
    # Take the resulting dictionary and average the 4 entries for each bit to get even closer to the original luma value, then attempt to convert back to raw bin data
    binData = ""
    for n in sorted(dictData.keys()):
        numberValue = sum(dictData[n]) / len(dictData[n])
        numberValue = math.floor(numberValue / int(256 / (2 ** analogDepth)))
        strValue = ("0" * (analogDepth - len(bin(numberValue).split('b')[1]))) + bin(numberValue).split('b')[1]
        
        binData = binData + strValue
    
    # Remove trailing zeros, may still be causing issues in some cases
    while binData[-1] == "0":
        binData = binData[:-1]
    
    # restore trailing zeros removed in end byte
    if (len(binData) % 8) != 0:
        binData = binData + ("0" * (8 - (len(binData) % 8)))
    
    # Return raw error encoded data, used for debugging
    if returnBytes:
        return binData
    
    out = ""
    
    # error correction decoder init
    errorHandler = rs.RSCoder(errorCorrectionBlockSize, int(errorCorrectionBlockSize - (errorCorrectionBlockSize / 8)))
    
    fullDecode = bytes(int(binData[16:][i:i+8], 2) for i in range(0, len(binData[16:]), 8)).decode(encoding="latin-1")
    
    # Correct errors and ommitted data, then spit out the original data
    i = 0
    while i < len(fullDecode):
        out = out + errorHandler.decode(fullDecode[i:i + errorCorrectionBlockSize])[0]
        i = i + errorCorrectionBlockSize
    
    return out