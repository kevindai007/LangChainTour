import json


def main(data: str) -> dict:
    parsed = json.loads(data)
    face = parsed["responses"][0]["faceAnnotations"][0]
    result = {
        "joyLikelihood": face.get("joyLikelihood", "UNKNOWN"),
        "sorrowLikelihood": face.get("sorrowLikelihood", "UNKNOWN"),
        "angerLikelihood": face.get("angerLikelihood", "UNKNOWN"),
        "surpriseLikelihood": face.get("surpriseLikelihood", "UNKNOWN"),
        "underExposedLikelihood": face.get("underExposedLikelihood", "UNKNOWN"),
        "blurredLikelihood": face.get("blurredLikelihood", "UNKNOWN"),
        "headwearLikelihood": face.get("headwearLikelihood", "UNKNOWN"),
    }
    return {"result": json.dumps(result, ensure_ascii=False)}


if __name__ == "__main__":
    json_str = """
    {
    "responses": [
        {
            "faceAnnotations": [
                {
                    "boundingPoly": {
                        "vertices": [
                            {
                                "x": 2
                            },
                            {
                                "x": 167
                            },
                            {
                                "x": 167,
                                "y": 176
                            },
                            {
                                "x": 2,
                                "y": 176
                            }
                        ]
                    },
                    "fdBoundingPoly": {
                        "vertices": [
                            {
                                "x": 24,
                                "y": 29
                            },
                            {
                                "x": 153,
                                "y": 29
                            },
                            {
                                "x": 153,
                                "y": 159
                            },
                            {
                                "x": 24,
                                "y": 159
                            }
                        ]
                    },
                    "landmarks": [
                        {
                            "type": "LEFT_EYE",
                            "position": {
                                "x": 56.859245,
                                "y": 78.8992,
                                "z": 0.0002784673
                            }
                        },
                        {
                            "type": "RIGHT_EYE",
                            "position": {
                                "x": 105.97038,
                                "y": 80.23046,
                                "z": -5.0507264
                            }
                        },
                        {
                            "type": "LEFT_OF_LEFT_EYEBROW",
                            "position": {
                                "x": 41.117928,
                                "y": 64.217926,
                                "z": 6.2727423
                            }
                        },
                        {
                            "type": "RIGHT_OF_LEFT_EYEBROW",
                            "position": {
                                "x": 69.48906,
                                "y": 64.914856,
                                "z": -10.409285
                            }
                        },
                        {
                            "type": "LEFT_OF_RIGHT_EYEBROW",
                            "position": {
                                "x": 91.75912,
                                "y": 66.04412,
                                "z": -12.821731
                            }
                        },
                        {
                            "type": "RIGHT_OF_RIGHT_EYEBROW",
                            "position": {
                                "x": 123.45111,
                                "y": 65.616684,
                                "z": -2.0724394
                            }
                        },
                        {
                            "type": "MIDPOINT_BETWEEN_EYES",
                            "position": {
                                "x": 80.373024,
                                "y": 77.971596,
                                "z": -12.435781
                            }
                        },
                        {
                            "type": "NOSE_TIP",
                            "position": {
                                "x": 78.62158,
                                "y": 106.46393,
                                "z": -26.628225
                            }
                        },
                        {
                            "type": "UPPER_LIP",
                            "position": {
                                "x": 78.00089,
                                "y": 124.15287,
                                "z": -15.665407
                            }
                        },
                        {
                            "type": "LOWER_LIP",
                            "position": {
                                "x": 77.554276,
                                "y": 141.24132,
                                "z": -12.332192
                            }
                        },
                        {
                            "type": "MOUTH_LEFT",
                            "position": {
                                "x": 58.91795,
                                "y": 127.6242,
                                "z": -0.36232522
                            }
                        },
                        {
                            "type": "MOUTH_RIGHT",
                            "position": {
                                "x": 99.84903,
                                "y": 131.59607,
                                "z": -4.852696
                            }
                        },
                        {
                            "type": "MOUTH_CENTER",
                            "position": {
                                "x": 77.7623,
                                "y": 132.53052,
                                "z": -12.14256
                            }
                        },
                        {
                            "type": "NOSE_BOTTOM_RIGHT",
                            "position": {
                                "x": 93.500984,
                                "y": 112.81829,
                                "z": -10.387136
                            }
                        },
                        {
                            "type": "NOSE_BOTTOM_LEFT",
                            "position": {
                                "x": 65.82014,
                                "y": 109.52309,
                                "z": -7.248543
                            }
                        },
                        {
                            "type": "NOSE_BOTTOM_CENTER",
                            "position": {
                                "x": 78.833275,
                                "y": 114.54355,
                                "z": -15.868175
                            }
                        },
                        {
                            "type": "LEFT_EYE_TOP_BOUNDARY",
                            "position": {
                                "x": 56.86882,
                                "y": 73.94824,
                                "z": -2.6983984
                            }
                        },
                        {
                            "type": "LEFT_EYE_RIGHT_CORNER",
                            "position": {
                                "x": 66.226906,
                                "y": 79.71093,
                                "z": -1.0224715
                            }
                        },
                        {
                            "type": "LEFT_EYE_BOTTOM_BOUNDARY",
                            "position": {
                                "x": 56.214745,
                                "y": 82.644226,
                                "z": -0.44718242
                            }
                        },
                        {
                            "type": "LEFT_EYE_LEFT_CORNER",
                            "position": {
                                "x": 46.273506,
                                "y": 78.60358,
                                "z": 5.4811416
                            }
                        },
                        {
                            "type": "RIGHT_EYE_TOP_BOUNDARY",
                            "position": {
                                "x": 106.55662,
                                "y": 75.39208,
                                "z": -7.8497815
                            }
                        },
                        {
                            "type": "RIGHT_EYE_RIGHT_CORNER",
                            "position": {
                                "x": 116.61177,
                                "y": 81.12066,
                                "z": -1.7429307
                            }
                        },
                        {
                            "type": "RIGHT_EYE_BOTTOM_BOUNDARY",
                            "position": {
                                "x": 106.41996,
                                "y": 84.08923,
                                "z": -5.6440682
                            }
                        },
                        {
                            "type": "RIGHT_EYE_LEFT_CORNER",
                            "position": {
                                "x": 97.08959,
                                "y": 81.2962,
                                "z": -4.088446
                            }
                        },
                        {
                            "type": "LEFT_EYEBROW_UPPER_MIDPOINT",
                            "position": {
                                "x": 54.901115,
                                "y": 60.362087,
                                "z": -5.116206
                            }
                        },
                        {
                            "type": "RIGHT_EYEBROW_UPPER_MIDPOINT",
                            "position": {
                                "x": 107.308304,
                                "y": 61.057026,
                                "z": -10.55071
                            }
                        },
                        {
                            "type": "LEFT_EAR_TRAGION",
                            "position": {
                                "x": 31.028221,
                                "y": 91.22389,
                                "z": 63.651474
                            }
                        },
                        {
                            "type": "RIGHT_EAR_TRAGION",
                            "position": {
                                "x": 141.88428,
                                "y": 99.20474,
                                "z": 51.851322
                            }
                        },
                        {
                            "type": "FOREHEAD_GLABELLA",
                            "position": {
                                "x": 80.38413,
                                "y": 65.99169,
                                "z": -13.320901
                            }
                        },
                        {
                            "type": "CHIN_GNATHION",
                            "position": {
                                "x": 76.25661,
                                "y": 164.58003,
                                "z": -5.4745765
                            }
                        },
                        {
                            "type": "CHIN_LEFT_GONION",
                            "position": {
                                "x": 39.15642,
                                "y": 130.18236,
                                "z": 42.55309
                            }
                        },
                        {
                            "type": "CHIN_RIGHT_GONION",
                            "position": {
                                "x": 126.289,
                                "y": 138.6203,
                                "z": 32.861767
                            }
                        },
                        {
                            "type": "LEFT_CHEEK_CENTER",
                            "position": {
                                "x": 45.873676,
                                "y": 109.74065,
                                "z": 5.607759
                            }
                        },
                        {
                            "type": "RIGHT_CHEEK_CENTER",
                            "position": {
                                "x": 114.423584,
                                "y": 112.945885,
                                "z": -1.5186088
                            }
                        }
                    ],
                    "rollAngle": 2.1992936,
                    "panAngle": -5.8344054,
                    "tiltAngle": -0.8062281,
                    "detectionConfidence": 0.921875,
                    "landmarkingConfidence": 0.7317187,
                    "joyLikelihood": "VERY_LIKELY",
                    "sorrowLikelihood": "VERY_UNLIKELY",
                    "angerLikelihood": "VERY_UNLIKELY",
                    "surpriseLikelihood": "VERY_UNLIKELY",
                    "underExposedLikelihood": "VERY_UNLIKELY",
                    "blurredLikelihood": "VERY_UNLIKELY",
                    "headwearLikelihood": "VERY_UNLIKELY"
                }
            ]
        }
    ]
}
    """
    result = main(json_str)
    print(result)
