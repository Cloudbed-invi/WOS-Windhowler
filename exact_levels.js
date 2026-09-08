const LAST_UPDATED = 'September 08, 2026 - 10:08:18';
const EXTRAPOLATE_A = 591.446648842496;
const EXTRAPOLATE_B = 4.1807398778742275;
const TIER_BOUNDARIES = [29, 38, 46];
const TIER_FORMULAS = [
  {
    "range": [
      21,
      29
    ],
    "coeffs": [
      511217.6959781208,
      -31959867.718906775,
      718818604.0508679,
      -5526202708.430213
    ],
    "max_error_pct": 1.22,
    "n_points": 8
  },
  {
    "range": [
      30,
      38
    ],
    "coeffs": [
      135888.65676232055,
      -5839735.851024878,
      133173400.611999,
      -1358061300.5758991
    ],
    "max_error_pct": 0.06,
    "n_points": 6
  },
  {
    "range": [
      39,
      46
    ],
    "coeffs": [
      276631.62338248524,
      -21773222.02828776,
      736503929.7195789,
      -9006677943.855988
    ],
    "max_error_pct": 0.27,
    "n_points": 8
  },
  {
    "range": [
      47,
      59
    ],
    "coeffs": [
      -362736.8129279515,
      77187833.36525813,
      -4336224090.366043,
      77216452943.53954
    ],
    "max_error_pct": 0.11,
    "n_points": 6
  }
];
const EXACT_LEVELS = {
  "1": {
    "start": 0,
    "window": 24300,
    "confirmed": true
  },
  "2": {
    "start": 441416,
    "window": 1322417,
    "confirmed": false
  },
  "3": {
    "start": 1763833,
    "window": 2200673,
    "confirmed": false
  },
  "4": {
    "start": 3964506,
    "window": 3076184,
    "confirmed": false
  },
  "5": {
    "start": 7040690,
    "window": 3948949,
    "confirmed": false
  },
  "6": {
    "start": 10989640,
    "window": 4818969,
    "confirmed": false
  },
  "7": {
    "start": 15808609,
    "window": 5686244,
    "confirmed": false
  },
  "8": {
    "start": 21494852,
    "window": 6550773,
    "confirmed": false
  },
  "9": {
    "start": 28045625,
    "window": 7412556,
    "confirmed": false
  },
  "10": {
    "start": 35458181,
    "window": 8271595,
    "confirmed": false
  },
  "11": {
    "start": 43729776,
    "window": 9127888,
    "confirmed": false
  },
  "12": {
    "start": 52857663,
    "window": 9981435,
    "confirmed": false
  },
  "13": {
    "start": 62839098,
    "window": 10832237,
    "confirmed": false
  },
  "14": {
    "start": 73671336,
    "window": 11680294,
    "confirmed": false
  },
  "15": {
    "start": 85351630,
    "window": 12525605,
    "confirmed": false
  },
  "16": {
    "start": 97877235,
    "window": 13368171,
    "confirmed": false
  },
  "17": {
    "start": 111245406,
    "window": 14207992,
    "confirmed": false
  },
  "18": {
    "start": 125453398,
    "window": 15045067,
    "confirmed": false
  },
  "19": {
    "start": 140498465,
    "window": 15879397,
    "confirmed": false
  },
  "20": {
    "start": 156377862,
    "window": 16710981,
    "confirmed": false
  },
  "21": {
    "start": 173088843,
    "window": 35972747,
    "confirmed": true
  },
  "22": {
    "start": 209161321,
    "window": 53272947,
    "confirmed": true
  },
  "23": {
    "start": 263733911,
    "window": 56812891,
    "confirmed": true
  },
  "24": {
    "start": 322862469,
    "window": 63737410,
    "confirmed": false
  },
  "25": {
    "start": 386599879,
    "window": 71766589,
    "confirmed": true
  },
  "26": {
    "start": 458087907,
    "window": 78710142,
    "confirmed": true
  },
  "27": {
    "start": 536742898,
    "window": 113490701,
    "confirmed": true
  },
  "28": {
    "start": 649866656,
    "window": 121149824,
    "confirmed": true
  },
  "29": {
    "start": 772045722,
    "window": 133066318,
    "confirmed": true
  },
  "30": {
    "start": 904986351,
    "window": 145148899,
    "confirmed": true
  },
  "31": {
    "start": 1049555539,
    "window": 157727701,
    "confirmed": true
  },
  "32": {
    "start": 1206376257,
    "window": 169669783,
    "confirmed": true
  },
  "33": {
    "start": 1376981186,
    "window": 183296553,
    "confirmed": false
  },
  "34": {
    "start": 1560277739,
    "window": 199034225,
    "confirmed": true
  },
  "35": {
    "start": 1758916168,
    "window": 214212663,
    "confirmed": false
  },
  "36": {
    "start": 1973128831,
    "window": 235909825,
    "confirmed": true
  },
  "37": {
    "start": 2203854584,
    "window": 248121981,
    "confirmed": false
  },
  "38": {
    "start": 2451976565,
    "window": 273967987,
    "confirmed": true
  },
  "39": {
    "start": 2723989318,
    "window": 285138965,
    "confirmed": true
  },
  "40": {
    "start": 3012795109,
    "window": 308756661,
    "confirmed": true
  },
  "41": {
    "start": 3324664306,
    "window": 332326245,
    "confirmed": true
  },
  "42": {
    "start": 3660540566,
    "window": 344230835,
    "confirmed": true
  },
  "43": {
    "start": 4019358690,
    "window": 385179417,
    "confirmed": true
  },
  "44": {
    "start": 4405871197,
    "window": 414414906,
    "confirmed": true
  },
  "45": {
    "start": 4823692161,
    "window": 415513658,
    "confirmed": true
  },
  "46": {
    "start": 5271756250,
    "window": 460089748,
    "confirmed": true
  },
  "47": {
    "start": 5747133410,
    "window": 511284571,
    "confirmed": true
  },
  "48": {
    "start": 6260921183,
    "window": 547484351,
    "confirmed": true
  },
  "49": {
    "start": 6811019088,
    "window": 586100370,
    "confirmed": true
  },
  "50": {
    "start": 7404407377,
    "window": 619881997,
    "confirmed": true
  },
  "51": {
    "start": 8043861060,
    "window": 667204546,
    "confirmed": false
  },
  "52": {
    "start": 8711065606,
    "window": 713644255,
    "confirmed": false
  },
  "53": {
    "start": 9424709861,
    "window": 778772811,
    "confirmed": false
  },
  "54": {
    "start": 10203482672,
    "window": 822005214,
    "confirmed": true
  },
  "55": {
    "start": 11059658685,
    "window": 930992049,
    "confirmed": false
  },
  "56": {
    "start": 11990650733,
    "window": 1002204214,
    "confirmed": false
  },
  "57": {
    "start": 12992854947,
    "window": 1069812509,
    "confirmed": false
  },
  "58": {
    "start": 14062667456,
    "window": 1133816932,
    "confirmed": false
  },
  "59": {
    "start": 15196484388,
    "window": 374135904,
    "confirmed": true
  },
  "60": {
    "start": 16065839233,
    "window": 1149485205,
    "confirmed": false,
    "extrapolated": true
  },
  "61": {
    "start": 17215324439,
    "window": 1211011659,
    "confirmed": false,
    "extrapolated": true
  },
  "62": {
    "start": 18426336098,
    "window": 1274758865,
    "confirmed": false,
    "extrapolated": true
  },
  "63": {
    "start": 19701094963,
    "window": 1340769520,
    "confirmed": false,
    "extrapolated": true
  },
  "64": {
    "start": 21041864483,
    "window": 1409086447,
    "confirmed": false,
    "extrapolated": true
  },
  "65": {
    "start": 22450950930,
    "window": 1479752589,
    "confirmed": false,
    "extrapolated": true
  }
};
const RAW_DATA = [
  {
    "Level": 17,
    "Percent": 29.0,
    "Damage": 72423951
  },
  {
    "Level": 20,
    "Percent": 8.0,
    "Damage": 143414658
  },
  {
    "Level": 21,
    "Percent": 1.0,
    "Damage": 173418819
  },
  {
    "Level": 22,
    "Percent": 47.0,
    "Damage": 234200050
  },
  {
    "Level": 23,
    "Percent": 47.0,
    "Damage": 290435970
  },
  {
    "Level": 23,
    "Percent": 70.0,
    "Damage": 303502935
  },
  {
    "Level": 24,
    "Percent": 53.0,
    "Damage": 355707410
  },
  {
    "Level": 25,
    "Percent": 9.0,
    "Damage": 393058820
  },
  {
    "Level": 25,
    "Percent": 14.0,
    "Damage": 397026845
  },
  {
    "Level": 25,
    "Percent": 22.0,
    "Damage": 402311815
  },
  {
    "Level": 25,
    "Percent": 67.0,
    "Damage": 434683450
  },
  {
    "Level": 26,
    "Percent": 50.0,
    "Damage": 497914590
  },
  {
    "Level": 27,
    "Percent": 17.0,
    "Damage": 556221612
  },
  {
    "Level": 27,
    "Percent": 20.0,
    "Damage": 559441034
  },
  {
    "Level": 27,
    "Percent": 79.0,
    "Damage": 626400558
  },
  {
    "Level": 28,
    "Percent": 11.0,
    "Damage": 663193137
  },
  {
    "Level": 28,
    "Percent": 16.0,
    "Damage": 669205486
  },
  {
    "Level": 28,
    "Percent": 50.0,
    "Damage": 710441567
  },
  {
    "Level": 29,
    "Percent": 30.0,
    "Damage": 811950970
  },
  {
    "Level": 29,
    "Percent": 57.0,
    "Damage": 847594114
  },
  {
    "Level": 29,
    "Percent": 72.0,
    "Damage": 867834427
  },
  {
    "Level": 30,
    "Percent": 3.0,
    "Damage": 901248419
  },
  {
    "Level": 30,
    "Percent": 0.0,
    "Damage": 905376879
  },
  {
    "Level": 30,
    "Percent": 5.0,
    "Damage": 912977123
  },
  {
    "Level": 30,
    "Percent": 11.0,
    "Damage": 921055692
  },
  {
    "Level": 30,
    "Percent": 27.0,
    "Damage": 944092374
  },
  {
    "Level": 32,
    "Percent": 22.0,
    "Damage": 1243209406
  },
  {
    "Level": 35,
    "Percent": 25.0,
    "Damage": 1812831025
  },
  {
    "Level": 38,
    "Percent": 37.0,
    "Damage": 2554494393
  },
  {
    "Level": 39,
    "Percent": 27.0,
    "Damage": 2799865740
  },
  {
    "Level": 39,
    "Percent": 65.0,
    "Damage": 2909355975
  },
  {
    "Level": 40,
    "Percent": 22.0,
    "Damage": 3079843839
  },
  {
    "Level": 40,
    "Percent": 37.0,
    "Damage": 3126908935
  },
  {
    "Level": 40,
    "Percent": 40.0,
    "Damage": 3136414860
  },
  {
    "Level": 40,
    "Percent": 0.0,
    "Damage": 3013185586
  },
  {
    "Level": 40,
    "Percent": 5.0,
    "Damage": 3026563430
  },
  {
    "Level": 41,
    "Percent": 18.0,
    "Damage": 3385200438
  },
  {
    "Level": 41,
    "Percent": 37.0,
    "Damage": 3445924183
  },
  {
    "Level": 41,
    "Percent": 61.0,
    "Damage": 3538623829
  },
  {
    "Level": 41,
    "Percent": 67.0,
    "Damage": 3546430572
  },
  {
    "Level": 42,
    "Percent": 3.0,
    "Damage": 3670692073
  },
  {
    "Level": 42,
    "Percent": 6.0,
    "Damage": 3681348810
  },
  {
    "Level": 42,
    "Percent": 13.0,
    "Damage": 3704877077
  },
  {
    "Level": 42,
    "Percent": 14.0,
    "Damage": 3709595305
  },
  {
    "Level": 43,
    "Percent": 10.0,
    "Damage": 4058504133
  },
  {
    "Level": 43,
    "Percent": 39.0,
    "Damage": 4168562903
  },
  {
    "Level": 44,
    "Percent": 73.0,
    "Damage": 4709602412
  },
  {
    "Level": 44,
    "Percent": 93.0,
    "Damage": 4790700657
  },
  {
    "Level": 45,
    "Percent": 6.0,
    "Damage": 4846951073
  },
  {
    "Level": 45,
    "Percent": 41.0,
    "Damage": 5003198972
  },
  {
    "Level": 49,
    "Percent": 17.0,
    "Damage": 6910710348
  },
  {
    "Level": 49,
    "Percent": 27.0,
    "Damage": 6968005861
  },
  {
    "Level": 56,
    "Percent": 2.0,
    "Damage": 11934638223
  },
  {
    "Level": 26,
    "Percent": 77.0,
    "Damage": 518646735
  },
  {
    "Level": 26,
    "Percent": 16.0,
    "Damage": 470584620
  },
  {
    "Level": 26,
    "Percent": 1.0,
    "Damage": 458914560
  },
  {
    "Level": 27,
    "Percent": 25.0,
    "Damage": 564865635
  },
  {
    "Level": 28,
    "Percent": 22.0,
    "Damage": 676949194
  },
  {
    "Level": 29,
    "Percent": 73.0,
    "Damage": 869206729
  },
  {
    "Level": 29,
    "Percent": 56.0,
    "Damage": 847118322
  },
  {
    "Level": 29,
    "Percent": 20.0,
    "Damage": 798670082
  },
  {
    "Level": 30,
    "Percent": 32.0,
    "Damage": 951557787
  },
  {
    "Level": 30,
    "Percent": 13.0,
    "Damage": 923816498
  },
  {
    "Level": 30,
    "Percent": 12.0,
    "Damage": 922204957
  },
  {
    "Level": 30,
    "Percent": 1.0,
    "Damage": 906320690
  },
  {
    "Level": 31,
    "Percent": 76.0,
    "Damage": 1169428592
  },
  {
    "Level": 32,
    "Percent": 42.0,
    "Damage": 1277818431
  },
  {
    "Level": 32,
    "Percent": 8.0,
    "Damage": 1220978042
  },
  {
    "Level": 32,
    "Percent": 1.0,
    "Damage": 1207870410
  },
  {
    "Level": 33,
    "Percent": 8.0,
    "Damage": 1390768940
  },
  {
    "Level": 33,
    "Percent": 8.0,
    "Damage": 1390162486
  },
  {
    "Level": 34,
    "Percent": 24.0,
    "Damage": 1608037167
  },
  {
    "Level": 34,
    "Percent": 10.0,
    "Damage": 1580245074
  },
  {
    "Level": 34,
    "Percent": 6.0,
    "Damage": 1572164665
  },
  {
    "Level": 36,
    "Percent": 11.0,
    "Damage": 1999225319
  },
  {
    "Level": 36,
    "Percent": 7.0,
    "Damage": 1989453612
  },
  {
    "Level": 36,
    "Percent": 1.0,
    "Damage": 1975530429
  },
  {
    "Level": 38,
    "Percent": 51.0,
    "Damage": 2591347146
  },
  {
    "Level": 38,
    "Percent": 36.0,
    "Damage": 2550852025
  },
  {
    "Level": 38,
    "Percent": 24.0,
    "Damage": 2517236147
  },
  {
    "Level": 39,
    "Percent": 51.0,
    "Damage": 2869381096
  },
  {
    "Level": 39,
    "Percent": 24.0,
    "Damage": 2792828121
  },
  {
    "Level": 39,
    "Percent": 2.0,
    "Damage": 2729694860
  },
  {
    "Level": 40,
    "Percent": 23.0,
    "Damage": 3084268518
  },
  {
    "Level": 40,
    "Percent": 19.0,
    "Damage": 3072237542
  },
  {
    "Level": 40,
    "Percent": 16.0,
    "Damage": 3062038720
  },
  {
    "Level": 40,
    "Percent": 14.0,
    "Damage": 3056518900
  },
  {
    "Level": 40,
    "Percent": 13.0,
    "Damage": 3054087273
  },
  {
    "Level": 40,
    "Percent": 13.0,
    "Damage": 3052125362
  },
  {
    "Level": 40,
    "Percent": 11.0,
    "Damage": 3047049307
  },
  {
    "Level": 40,
    "Percent": 8.0,
    "Damage": 3038490601
  },
  {
    "Level": 40,
    "Percent": 4.0,
    "Damage": 3025439743
  },
  {
    "Level": 40,
    "Percent": 0.0,
    "Damage": 3010842193
  },
  {
    "Level": 45,
    "Percent": 45.0,
    "Damage": 5003198972
  },
  {
    "Level": 54,
    "Percent": 66.0,
    "Damage": 10746042837
  },
  {
    "Level": 54,
    "Percent": 45.0,
    "Damage": 10573100534
  },
  {
    "Level": 54,
    "Percent": 19.0,
    "Damage": 10359674661
  },
  {
    "Level": 47,
    "Percent": 65.0,
    "Damage": 6078886524
  },
  {
    "Level": 48,
    "Percent": 27.0,
    "Damage": 6406734869
  },
  {
    "Level": 48,
    "Percent": 15.0,
    "Damage": 6343805523
  },
  {
    "Level": 48,
    "Percent": 5.0,
    "Damage": 6288498422
  },
  {
    "Level": 47,
    "Percent": 57.0,
    "Damage": 6040128124
  },
  {
    "Level": 49,
    "Percent": 58.0,
    "Damage": 7151017277
  },
  {
    "Level": 48,
    "Percent": 79.0,
    "Damage": 6693657402
  },
  {
    "Level": 48,
    "Percent": 31.0,
    "Damage": 6431148202
  },
  {
    "Level": 48,
    "Percent": 23.0,
    "Damage": 6385632402
  },
  {
    "Level": 63,
    "Percent": 68.0,
    "Damage": 21055194115
  },
  {
    "Level": 47,
    "Percent": 0.0,
    "Damage": 5748068630
  },
  {
    "Level": 47,
    "Percent": 55.0,
    "Damage": 6027952006
  },
  {
    "Level": 47,
    "Percent": 40.0,
    "Damage": 5953603835
  },
  {
    "Level": 59,
    "Percent": 32.0,
    "Damage": 15318012829
  },
  {
    "Level": 59,
    "Percent": 30.0,
    "Damage": 15299108251
  },
  {
    "Level": 59,
    "Percent": 33.0,
    "Damage": 15327761214
  },
  {
    "Level": 51,
    "Percent": 2.0,
    "Damage": 8044266039
  },
  {
    "Level": 50,
    "Percent": 44.0,
    "Damage": 7675380688
  },
  {
    "Level": 50,
    "Percent": 78.0,
    "Damage": 7887973347
  },
  {
    "Level": 50,
    "Percent": 48.0,
    "Damage": 7703667480
  },
  {
    "Level": 21,
    "Percent": 1.0,
    "Damage": 173466445
  },
  {
    "Level": 21,
    "Percent": 60.0,
    "Damage": 194675240
  },
  {
    "Level": 21,
    "Percent": 56.0,
    "Damage": 193211476
  },
  {
    "Level": 22,
    "Percent": 15.0,
    "Damage": 217152565
  },
  {
    "Level": 22,
    "Percent": 34.0,
    "Damage": 227119270
  },
  {
    "Level": 21,
    "Percent": 35.0,
    "Damage": 185782488
  },
  {
    "Level": 31,
    "Percent": 2.0,
    "Damage": 1052887122
  },
  {
    "Level": 31,
    "Percent": 0.0,
    "Damage": 1049555537
  },
  {
    "Level": 47,
    "Percent": 28.0,
    "Damage": 5889369081
  },
  {
    "Level": 47,
    "Percent": 26.0,
    "Damage": 5877585858
  },
  {
    "Level": 47,
    "Percent": 6.0,
    "Damage": 5777473938
  },
  {
    "Level": 43,
    "Percent": 84.0,
    "Damage": 4344192684
  },
  {
    "Level": 44,
    "Percent": 2.0,
    "Damage": 4414204787
  },
  {
    "Level": 44,
    "Percent": 8.0,
    "Damage": 4438187159
  },
  {
    "Level": 43,
    "Percent": 5.0,
    "Damage": 4040117019
  },
  {
    "Level": 40,
    "Percent": 19.0,
    "Damage": 3070065426
  },
  {
    "Level": 44,
    "Percent": 0.0,
    "Damage": 4406378496
  },
  {
    "Level": 31,
    "Percent": 14.0,
    "Damage": 1071589812
  },
  {
    "Level": 43,
    "Percent": 60.0,
    "Damage": 4250301738
  },
  {
    "Level": 43,
    "Percent": 45.0,
    "Damage": 4191763476
  },
  {
    "Level": 43,
    "Percent": 22.0,
    "Damage": 4102922915
  },
  {
    "Level": 46,
    "Percent": 29.0,
    "Damage": 5405181732
  },
  {
    "Level": 46,
    "Percent": 25.0,
    "Damage": 5388896960
  },
  {
    "Level": 46,
    "Percent": 13.0,
    "Damage": 5331567494
  }
];
