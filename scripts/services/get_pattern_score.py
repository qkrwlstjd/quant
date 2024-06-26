import numpy as np
import talib
import json

pattern = {
    "CDL2CROWS": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDL3BLACKCROWS": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDL3INSIDE": {
        "-100": 0,
        "0": 0.4936196650698832,
        "100": 0.6797881533789328
    },
    "CDL3LINESTRIKE": {
        "-100": 0.4674154302346545,
        "0": 0.4987259547201429,
        "100": 0
    },
    "CDL3OUTSIDE": {
        "-100": 0.10996813200945278,
        "0": 0.4959370759652301,
        "100": 0.5938506112899806
    },
    "CDL3STARSINSOUTH": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDL3WHITESOLDIERS": {
        "-100": 0,
        "0": 0.4988226947977817,
        "100": 0.37913122666057714
    },
    "CDLABANDONEDBABY": {
        "-100": 0,
        "0": 0.4986717757036014,
        "100": -0.7116277364163328
    },
    "CDLADVANCEBLOCK": {
        "-100": 0.0034678412327913384,
        "0": 0.49910361607008574,
        "100": 0
    },
    "CDLBELTHOLD": {
        "-100": 0,
        "0": 0.5384402592134112,
        "100": 0.45934396609449324
    },
    "CDLBREAKAWAY": {
        "-100": 0,
        "0": 0.4984117227888087,
        "100": 0.8780623398069776
    },
    "CDLCLOSINGMARUBOZU": {
        "-100": 0,
        "0": 0.26712171878636115,
        "100": 0.91854760924573
    },
    "CDLCONCEALBABYSWALL": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLCOUNTERATTACK": {
        "-100": 0,
        "0": 0.49946643667465257,
        "100": -0.44818088103865944
    },
    "CDLDARKCLOUDCOVER": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLDOJI": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLDOJISTAR": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLDRAGONFLYDOJI": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLENGULFING": {
        "-100": 0,
        "0": 0.5261702745294038,
        "100": 0.3388740078552411
    },
    "CDLEVENINGDOJISTAR": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLEVENINGSTAR": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLGAPSIDESIDEWHITE": {
        "-100": -0.7794836393132908,
        "0": 0.49563992660469075,
        "100": 1.8246923946331308
    },
    "CDLGRAVESTONEDOJI": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLHAMMER": {
        "-100": 0,
        "0": 0.49855357623912755,
        "100": -0.40160642570281135
    },
    "CDLHANGINGMAN": {
        "-100": 0.2008032128514056,
        "0": 0.4985379133692449,
        "100": 0
    },
    "CDLHARAMI": {
        "-100": 0.620039145844437,
        "0": 0.4991189408486927,
        "100": -0.7054628499422596
    },
    "CDLHARAMICROSS": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLHIGHWAVE": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLHIKKAKE": {
        "-100": 0.6200529662069914,
        "0": 0.48039873207056116,
        "100": 0.5432842012308398
    },
    "CDLHIKKAKEMOD": {
        "-100": 0.3040388286105784,
        "0": 0.49876136421105,
        "100": 0.4425795822287745
    },
    "CDLHOMINGPIGEON": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLIDENTICAL3CROWS": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLINNECK": {
        "-100": -0.47235119825592853,
        "0": 0.4993133245674928,
        "100": 0
    },
    "CDLINVERTEDHAMMER": {
        "-100": 0,
        "0": 0.4986490022236628,
        "100": -8.642219436053214
    },
    "CDLKICKING": {
        "-100": 0,
        "0": 0.49867925292479964,
        "100": -1.4126329758318885
    },
    "CDLKICKINGBYLENGTH": {
        "-100": 0,
        "0": 0.49867925292479964,
        "100": -1.4126329758318885
    },
    "CDLLADDERBOTTOM": {
        "-100": 0,
        "0": 0.4975415405949095,
        "100": 0.9758403449467699
    },
    "CDLLONGLEGGEDDOJI": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLLONGLINE": {
        "-100": 0,
        "0": 0.40696600858128895,
        "100": 0.6151190239636308
    },
    "CDLMARUBOZU": {
        "-100": 0,
        "0": 0.42328375465284346,
        "100": 0.8572510237861042
    },
    "CDLMATCHINGLOW": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLMATHOLD": {
        "-100": 0,
        "0": 0.49854980299147855,
        "100": 0.30979146527502566
    },
    "CDLMORNINGDOJISTAR": {
        "-100": 0,
        "0": 0.5001586528833385,
        "100": 0.28747743763177686
    },
    "CDLMORNINGSTAR": {
        "-100": 0,
        "0": 0.5032879247117841,
        "100": 0.3085112658961847
    },
    "CDLONNECK": {
        "-100": -1.0837938705932741,
        "0": 0.499291627346973,
        "100": 0
    },
    "CDLPIERCING": {
        "-100": 0,
        "0": 0.5015839422247405,
        "100": 0.2647813282316067
    },
    "CDLRICKSHAWMAN": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLRISEFALL3METHODS": {
        "-100": 0,
        "0": 0.49878167817640334,
        "100": 0.19168908409874102
    },
    "CDLSEPARATINGLINES": {
        "-100": 0,
        "0": 0.49713775346734074,
        "100": 0.6131837240990161
    },
    "CDLSHOOTINGSTAR": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLSHORTLINE": {
        "-100": 0,
        "0": 0.5002185538880789,
        "100": 0.16889952156198698
    },
    "CDLSPINNINGTOP": {
        "-100": 0,
        "0": 0.4985329368146863,
        "100": 0.3922064777327935
    },
    "CDLSTALLEDPATTERN": {
        "-100": -0.9080428458922928,
        "0": 0.4985667437703979,
        "100": 0
    },
    "CDLSTICKSANDWICH": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLTAKURI": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLTASUKIGAP": {
        "-100": 0.31835434399245405,
        "0": 0.4986708175215344,
        "100": 0
    },
    "CDLTHRUSTING": {
        "-100": 0.1561457538863834,
        "0": 0.5008559038328346,
        "100": 0
    },
    "CDLTRISTAR": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLUNIQUE3RIVER": {
        "-100": 0,
        "0": 0.4985115415277645,
        "100": 1.9316696745285955
    },
    "CDLUPSIDEGAP2CROWS": {
        "-100": 0,
        "0": 0.49853017235992353,
        "100": 0
    },
    "CDLXSIDEGAP3METHODS": {
        "-100": 0.0648327645225579,
        "0": 0.5007401965198599,
        "100": 0
    }
}


pattern123 = {
    "CDL2CROWS": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDL3BLACKCROWS": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDL3INSIDE": {
        "-100": 0,
        "0": 0,
        "100": 0.6797881533789328
    },
    "CDL3LINESTRIKE": {
        "-100": 0.4674154302346545,
        "0": 0,
        "100": 0
    },
    "CDL3OUTSIDE": {
        "-100": 0.10996813200945278,
        "0": 0,
        "100": 0.5938506112899806
    },
    "CDL3STARSINSOUTH": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDL3WHITESOLDIERS": {
        "-100": 0,
        "0": 0,
        "100": 0.37913122666057714
    },
    "CDLABANDONEDBABY": {
        "-100": 0,
        "0": 0,
        "100": -0.7116277364163328
    },
    "CDLADVANCEBLOCK": {
        "-100": 0.0034678412327913384,
        "0": 0,
        "100": 0
    },
    "CDLBELTHOLD": {
        "-100": 0,
        "0": 0,
        "100": 0.45934396609449324
    },
    "CDLBREAKAWAY": {
        "-100": 0,
        "0": 0,
        "100": 0.8780623398069776
    },
    "CDLCLOSINGMARUBOZU": {
        "-100": 0,
        "0": 0,
        "100": 0.91854760924573
    },
    "CDLCONCEALBABYSWALL": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLCOUNTERATTACK": {
        "-100": 0,
        "0": 0,
        "100": -0.44818088103865944
    },
    "CDLDARKCLOUDCOVER": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLDOJI": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLDOJISTAR": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLDRAGONFLYDOJI": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLENGULFING": {
        "-100": 0,
        "0": 0,
        "100": 0.3388740078552411
    },
    "CDLEVENINGDOJISTAR": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLEVENINGSTAR": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLGAPSIDESIDEWHITE": {
        "-100": -0.7794836393132908,
        "0": 0,
        "100": 1.8246923946331308
    },
    "CDLGRAVESTONEDOJI": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLHAMMER": {
        "-100": 0,
        "0": 0,
        "100": -0.40160642570281135
    },
    "CDLHANGINGMAN": {
        "-100": 0.2008032128514056,
        "0": 0,
        "100": 0
    },
    "CDLHARAMI": {
        "-100": 0.620039145844437,
        "0": 0,
        "100": -0.7054628499422596
    },
    "CDLHARAMICROSS": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLHIGHWAVE": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLHIKKAKE": {
        "-100": 0.6200529662069914,
        "0": 0,
        "100": 0.5432842012308398
    },
    "CDLHIKKAKEMOD": {
        "-100": 0.3040388286105784,
        "0": 0,
        "100": 0.4425795822287745
    },
    "CDLHOMINGPIGEON": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLIDENTICAL3CROWS": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLINNECK": {
        "-100": -0.47235119825592853,
        "0": 0,
        "100": 0
    },
    "CDLINVERTEDHAMMER": {
        "-100": 0,
        "0": 0,
        "100": -8.642219436053214
    },
    "CDLKICKING": {
        "-100": 0,
        "0": 0,
        "100": -1.4126329758318885
    },
    "CDLKICKINGBYLENGTH": {
        "-100": 0,
        "0": 0,
        "100": -1.4126329758318885
    },
    "CDLLADDERBOTTOM": {
        "-100": 0,
        "0": 0,
        "100": 0.9758403449467699
    },
    "CDLLONGLEGGEDDOJI": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLLONGLINE": {
        "-100": 0,
        "0": 0,
        "100": 0.6151190239636308
    },
    "CDLMARUBOZU": {
        "-100": 0,
        "0": 0,
        "100": 0.8572510237861042
    },
    "CDLMATCHINGLOW": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLMATHOLD": {
        "-100": 0,
        "0": 0,
        "100": 0.30979146527502566
    },
    "CDLMORNINGDOJISTAR": {
        "-100": 0,
        "0": 0,
        "100": 0.28747743763177686
    },
    "CDLMORNINGSTAR": {
        "-100": 0,
        "0": 0,
        "100": 0.3085112658961847
    },
    "CDLONNECK": {
        "-100": -1.0837938705932741,
        "0": 0,
        "100": 0
    },
    "CDLPIERCING": {
        "-100": 0,
        "0": 0,
        "100": 0.2647813282316067
    },
    "CDLRICKSHAWMAN": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLRISEFALL3METHODS": {
        "-100": 0,
        "0": 0,
        "100": 0.19168908409874102
    },
    "CDLSEPARATINGLINES": {
        "-100": 0,
        "0": 0,
        "100": 0.6131837240990161
    },
    "CDLSHOOTINGSTAR": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLSHORTLINE": {
        "-100": 0,
        "0": 0,
        "100": 0.16889952156198698
    },
    "CDLSPINNINGTOP": {
        "-100": 0,
        "0": 0,
        "100": 0.3922064777327935
    },
    "CDLSTALLEDPATTERN": {
        "-100": -0.9080428458922928,
        "0": 0,
        "100": 0
    },
    "CDLSTICKSANDWICH": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLTAKURI": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLTASUKIGAP": {
        "-100": 0.31835434399245405,
        "0": 0,
        "100": 0
    },
    "CDLTHRUSTING": {
        "-100": 0.1561457538863834,
        "0": 0,
        "100": 0
    },
    "CDLTRISTAR": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLUNIQUE3RIVER": {
        "-100": 0,
        "0": 0,
        "100": 1.9316696745285955
    },
    "CDLUPSIDEGAP2CROWS": {
        "-100": 0,
        "0": 0,
        "100": 0
    },
    "CDLXSIDEGAP3METHODS": {
        "-100": 0.0648327645225579,
        "0": 0,
        "100": 0
    }
}


def get_pattern_score(df):
    candle_names = talib.get_function_groups()['Pattern Recognition']

    # 각 캔들 패턴에 대해 계산하고 데이터프레임에 추가

    for candle in candle_names:
        # getattr 함수를 사용하여 캔들 함수를 동적으로 호출
        pattern_function = getattr(talib, candle)
        df[candle] = pattern_function(df['open'], df['high'], df['low'], df['close'])

    last_obj = json.loads(df.iloc[-1].to_json())
    pattern_score = 0

    for candle in candle_names:
        pattern_value = last_obj[candle] if not np.isnan(last_obj[candle]) else 0
        pattern_value = -100 if pattern_value < 0 else (100 if pattern_value > 0 else 0)
        pattern_score += pattern[candle][str(pattern_value)]

    return pattern_score
