# ocr-backend/ocr_service.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2
import easyocr
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()
reader = easyocr.Reader(['en'])

# ✅ Add this block to allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    results = reader.readtext(img)
    lines = [t[1] for t in results if not re.fullmatch(r"\s*bonus\s*", t[1], re.IGNORECASE)]

    # ✅ Basic index-based mapping
    data = {
        "character": lines[0],
        "level": lines[1],
        "playerID": lines[4],
        "uid": lines[5],

        "basicAtkLvl": lines[6],
        "skillLvl": lines[8],
        "forteCircuitLvl": lines[9],
        "introSkillLvl": lines[15],
        "ultimateLvl": lines[16],

        "weaponName": lines[12],
        "weaponLvl": lines[13],

        "echo1MainStat": lines[17],
        "echo1MainStatNum": lines[22],
        "echo1DefaultStat": lines[27],
        "echo1DefaultStatNum": lines[28],
        "echo1FirstSubstat": lines[37],
        "echo1FirstSubstatNum": lines[38],
        "echo1SecondSubstat": lines[47],
        "echo1SecondSubstatNum": lines[48],
        "echo1ThirdSubstat": lines[57],
        "echo1ThirdSubstatNum": lines[58],
        "echo1FourthSubstat": lines[67],
        "echo1FourthSubstatNum": lines[68],
        "echo1FifthSubstat": lines[77],
        "echo1FifthSubstatNum": lines[78],

        "echo2MainStat": lines[18],
        "echo2MainStatNum": lines[23],
        "echo2DefaultStat": lines[29],
        "echo2DefaultStatNum": lines[30],
        "echo2FirstSubstat": lines[39],
        "echo2FirstSubstatNum": lines[40],
        "echo2SecondSubstat": lines[49],
        "echo2SecondSubstatNum": lines[50],
        "echo2ThirdSubstat": lines[59],
        "echo2ThirdSubstatNum": lines[60],
        "echo2FourthSubstat": lines[69],
        "echo2FourthSubstatNum": lines[70],
        "echo2FifthSubstat": lines[79],
        "echo2FifthSubstatNum": lines[80],

        "echo3MainStat": lines[19],
        "echo3MainStatNum": lines[24],
        "echo3DefaultStat": lines[31],
        "echo3DefaultStatNum": lines[32],
        "echo3FirstSubstat": lines[41],
        "echo3FirstSubstatNum": lines[42],
        "echo3SecondSubstat": lines[51],
        "echo3SecondSubstatNum": lines[52],
        "echo3ThirdSubstat": lines[61],
        "echo3ThirdSubstatNum": lines[62],
        "echo3FourthSubstat": lines[71],
        "echo3FourthSubstatNum": lines[72],
        "echo3FifthSubstat": lines[81],
        "echo3FifthSubstatNum": lines[82],

        "echo4MainStat": lines[20],
        "echo4MainStatNum": lines[25],
        "echo4DefaultStat": lines[33],
        "echo4DefaultStatNum": lines[34],
        "echo4FirstSubstat": lines[43],
        "echo4FirstSubstatNum": lines[44],
        "echo4SecondSubstat": lines[53],
        "echo4SecondSubstatNum": lines[54],
        "echo4ThirdSubstat": lines[63],
        "echo4ThirdSubstatNum": lines[64],
        "echo4FourthSubstat": lines[73],
        "echo4FourthSubstatNum": lines[74],
        "echo4FifthSubstat": lines[83],
        "echo4FifthSubstatNum": lines[84],

        "echo5MainStat": lines[21],
        "echo5MainStatNum": lines[26],
        "echo5DefaultStat": lines[35],
        "echo5DefaultStatNum": lines[36],
        "echo5FirstSubstat": lines[45],
        "echo5FirstSubstatNum": lines[46],
        "echo5SecondSubstat": lines[55],
        "echo5SecondSubstatNum": lines[56],
        "echo5ThirdSubstat": lines[65],
        "echo5ThirdSubstatNum": lines[66],
        "echo5FourthSubstat": lines[75],
        "echo5FourthSubstatNum": lines[76],
        "echo5FifthSubstat": lines[85],
        "echo5FifthSubstatNum": lines[86],

        "stats": []
    }

    data['level'] = data['level'].replace('O', '0')
    digits = re.findall(r"\d+", data["level"])
    data["level"] = "".join(digits)

    data["playerID"] = data["playerID"][10:]
    data["uid"] = data["uid"][4:]

    data['weaponLvl'] = data['weaponLvl'].replace('O', '0')
    digits = re.findall(r"\d+", data["weaponLvl"])
    data["weaponLvl"] = "".join(digits)

    data['echo1DefaultStat'] = data['echo1DefaultStat'].replace('X', '')

    # data['echo3ThirdSubstatNum'] = fix_substat(data['echo3ThirdSubstatNum'])
    percent_fields = [
    "echo1FirstSubstatNum",
    "echo2FirstSubstatNum",
    "echo3FirstSubstatNum",
    "echo4FirstSubstatNum",
    "echo5FirstSubstatNum",
    "echo2SecondSubstatNum",
    "echo3SecondSubstatNum",
    "echo4SecondSubstatNum",
    "echo5SecondSubstatNum",
    "echo1ThirdSubstatNum",
    "echo2ThirdSubstatNum",
    "echo3ThirdSubstatNum",
    "echo4ThirdSubstatNum",
    "echo5ThirdSubstatNum",
    "echo1FourthSubstatNum",
    "echo2FourthSubstatNum",
    "echo3FourthSubstatNum",
    "echo4FourthSubstatNum",
    "echo5FourthSubstatNum",
    "echo1FifthSubstatNum",
    "echo2FifthSubstatNum",
    "echo3FifthSubstatNum",
    "echo4FifthSubstatNum",
    "echo5FifthSubstatNum",
    ]

    for field in percent_fields:
        data[field] = fix_percent_format(data[field])

    data['echo3MainStatNum'] = data['echo3MainStatNum'].replace('O', '0')
    digits = re.findall(r'[0-9.%]+', data["echo3MainStatNum"])
    data["echo3MainStatNum"] = "".join(digits)

    data['echo4MainStatNum'] = data['echo4MainStatNum'].replace('O', '0')
    digits = re.findall(r'[0-9.%]+', data["echo4MainStatNum"])
    data["echo4MainStatNum"] = "".join(digits)

    data['echo5MainStatNum'] = data['echo5MainStatNum'].replace('O', '0')
    digits = re.findall(r'[0-9.%]+', data["echo5MainStatNum"])
    data["echo5MainStatNum"] = "".join(digits)

    if len(lines) > 0:
        data["stats"] = lines[0:]  # Remaining lines = stats

    return JSONResponse(content=data)

def fix_percent_format(value: str) -> str:
    # Check for digit-dot-digit, but missing a '%'
    if re.fullmatch(r'\d+\.\d+', value) and not value.endswith('%'):
        # Convert to float and format with 1 decimal + add %
        return f"{float(value):.1f}%"
    return value