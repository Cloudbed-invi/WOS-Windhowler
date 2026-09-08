const LAST_UPDATED = 'September 08, 2026 - 12:54:32';
const EXTRAPOLATE_A = 577.2530710450128;
const EXTRAPOLATE_B = 4.186508406537005;
const TIER_BOUNDARIES = [33];
const BOUNDARY_METADATA = {"33": {"stable": true, "pelt_disagree": true, "pelt_suggestions": [38]}};
const ADJACENT_MISMATCHES = [{"Level Pair": "33 -> 34", "End N": 1571026097, "Start N+1": 1560277739, "Mismatch %": 0.689, "Flagged": false}, {"Level Pair": "45 -> 46", "End N": 5239205819, "Start N+1": 5271756250, "Mismatch %": 0.617, "Flagged": false}, {"Level Pair": "22 -> 23", "End N": 262434268, "Start N+1": 263733911, "Mismatch %": 0.493, "Flagged": false}, {"Level Pair": "42 -> 43", "End N": 4004771401, "Start N+1": 4019358690, "Mismatch %": 0.363, "Flagged": false}, {"Level Pair": "46 -> 47", "End N": 5731845998, "Start N+1": 5747133410, "Mismatch %": 0.266, "Flagged": false}, {"Level Pair": "49 -> 50", "End N": 7397119458, "Start N+1": 7408776394, "Mismatch %": 0.157, "Flagged": false}, {"Level Pair": "28 -> 29", "End N": 771016480, "Start N+1": 772043308, "Mismatch %": 0.133, "Flagged": false}, {"Level Pair": "39 -> 40", "End N": 3009128283, "Start N+1": 3012795109, "Mismatch %": 0.122, "Flagged": false}, {"Level Pair": "41 -> 42", "End N": 3656990551, "Start N+1": 3660540566, "Mismatch %": 0.097, "Flagged": false}, {"Level Pair": "40 -> 41", "End N": 3321551770, "Start N+1": 3324664306, "Mismatch %": 0.094, "Flagged": false}, {"Level Pair": "50 -> 51", "End N": 8023132040, "Start N+1": 8030588026, "Mismatch %": 0.093, "Flagged": false}, {"Level Pair": "32 -> 33", "End N": 1376046040, "Start N+1": 1374803292, "Mismatch %": 0.09, "Flagged": false}, {"Level Pair": "31 -> 32", "End N": 1207271366, "Start N+1": 1206376257, "Mismatch %": 0.074, "Flagged": false}, {"Level Pair": "38 -> 39", "End N": 2725944552, "Start N+1": 2723989318, "Mismatch %": 0.072, "Flagged": false}, {"Level Pair": "44 -> 45", "End N": 4820286103, "Start N+1": 4823692161, "Mismatch %": 0.071, "Flagged": false}, {"Level Pair": "25 -> 26", "End N": 458366468, "Start N+1": 458087907, "Mismatch %": 0.061, "Flagged": false}, {"Level Pair": "30 -> 31", "End N": 1050135250, "Start N+1": 1049537992, "Mismatch %": 0.057, "Flagged": false}, {"Level Pair": "27 -> 28", "End N": 650233599, "Start N+1": 649866656, "Mismatch %": 0.056, "Flagged": false}, {"Level Pair": "21 -> 22", "End N": 209061590, "Start N+1": 209161321, "Mismatch %": 0.048, "Flagged": false}, {"Level Pair": "47 -> 48", "End N": 6258417981, "Start N+1": 6260921183, "Mismatch %": 0.04, "Flagged": false}, {"Level Pair": "48 -> 49", "End N": 6808405534, "Start N+1": 6811019088, "Mismatch %": 0.038, "Flagged": false}, {"Level Pair": "43 -> 44", "End N": 4404538107, "Start N+1": 4405871197, "Mismatch %": 0.03, "Flagged": false}, {"Level Pair": "29 -> 30", "End N": 905101072, "Start N+1": 904986351, "Mismatch %": 0.013, "Flagged": false}, {"Level Pair": "26 -> 27", "End N": 536798049, "Start N+1": 536742898, "Mismatch %": 0.01, "Flagged": false}];
const TIER_FORMULAS = [
  {
    "range": [
      21,
      33
    ],
    "coeffs": [
      187552.5824317598,
      -8351637.568890957,
      148441192.42927882,
      -960601382.2261816
    ],
    "max_error_pct": 2.38,
    "loocv_max_pct": 7.04,
    "n_points": 12,
    "provisional": true
  },
  {
    "range": [
      34,
      59
    ],
    "coeffs": [
      269050.2966981456,
      -20201789.03193678,
      647030823.9878157,
      -7458629967.321186
    ],
    "max_error_pct": 0.79,
    "loocv_max_pct": 2.21,
    "n_points": 18,
    "provisional": false
  }
];
const EXACT_LEVELS = {
  "1": {
    "start": 504,
    "window": 8680,
    "confirmed": false,
    "extrapolated": true
  },
  "2": {
    "start": 9184,
    "window": 40965,
    "confirmed": false,
    "extrapolated": true
  },
  "3": {
    "start": 50149,
    "window": 117082,
    "confirmed": false,
    "extrapolated": true
  },
  "4": {
    "start": 167231,
    "window": 258397,
    "confirmed": false,
    "extrapolated": true
  },
  "5": {
    "start": 425628,
    "window": 487483,
    "confirmed": false,
    "extrapolated": true
  },
  "6": {
    "start": 913111,
    "window": 827882,
    "confirmed": false,
    "extrapolated": true
  },
  "7": {
    "start": 1740993,
    "window": 1303961,
    "confirmed": false,
    "extrapolated": true
  },
  "8": {
    "start": 3044954,
    "window": 1940804,
    "confirmed": false,
    "extrapolated": true
  },
  "9": {
    "start": 4985758,
    "window": 2764128,
    "confirmed": false,
    "extrapolated": true
  },
  "10": {
    "start": 7749886,
    "window": 3800224,
    "confirmed": false,
    "extrapolated": true
  },
  "11": {
    "start": 11550110,
    "window": 5075908,
    "confirmed": false,
    "extrapolated": true
  },
  "12": {
    "start": 16626018,
    "window": 6618476,
    "confirmed": false,
    "extrapolated": true
  },
  "13": {
    "start": 23244494,
    "window": 8455672,
    "confirmed": false,
    "extrapolated": true
  },
  "14": {
    "start": 31700166,
    "window": 10615660,
    "confirmed": false,
    "extrapolated": true
  },
  "15": {
    "start": 42315826,
    "window": 13126994,
    "confirmed": false,
    "extrapolated": true
  },
  "16": {
    "start": 55442820,
    "window": 16018599,
    "confirmed": false,
    "extrapolated": true
  },
  "17": {
    "start": 71461419,
    "window": 19319751,
    "confirmed": false,
    "extrapolated": true
  },
  "18": {
    "start": 90781170,
    "window": 23060061,
    "confirmed": false,
    "extrapolated": true
  },
  "19": {
    "start": 113841231,
    "window": 27269453,
    "confirmed": false,
    "extrapolated": true
  },
  "20": {
    "start": 141110684,
    "window": 31978159,
    "confirmed": false,
    "extrapolated": true
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
    "start": 772043308,
    "window": 133057764,
    "confirmed": true
  },
  "30": {
    "start": 904986351,
    "window": 145148899,
    "confirmed": true
  },
  "31": {
    "start": 1049537992,
    "window": 157733374,
    "confirmed": true
  },
  "32": {
    "start": 1206376257,
    "window": 169669783,
    "confirmed": true
  },
  "33": {
    "start": 1374803292,
    "window": 196222805,
    "confirmed": true
  },
  "34": {
    "start": 1560277739,
    "window": 199034225,
    "confirmed": true
  },
  "35": {
    "start": 1759836443,
    "window": 213292388,
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
    "start": 7408776394,
    "window": 614355646,
    "confirmed": true
  },
  "51": {
    "start": 8030588026,
    "window": 672635538,
    "confirmed": true
  },
  "52": {
    "start": 8703468390,
    "window": 715233276,
    "confirmed": false
  },
  "53": {
    "start": 9418701666,
    "window": 784781006,
    "confirmed": false
  },
  "54": {
    "start": 10203482672,
    "window": 822005214,
    "confirmed": true
  },
  "55": {
    "start": 11065865262,
    "window": 930141475,
    "confirmed": false
  },
  "56": {
    "start": 11996006737,
    "window": 998250352,
    "confirmed": false
  },
  "57": {
    "start": 12994257089,
    "window": 1066709220,
    "confirmed": false
  },
  "58": {
    "start": 14060966309,
    "window": 1135518079,
    "confirmed": false
  },
  "59": {
    "start": 15196484388,
    "window": 374135904,
    "confirmed": true
  },
  "60": {
    "start": 16055040665,
    "window": 1150353037,
    "confirmed": false,
    "extrapolated": true
  },
  "61": {
    "start": 17205393702,
    "window": 1212040543,
    "confirmed": false,
    "extrapolated": true
  },
  "62": {
    "start": 18417434245,
    "window": 1275960608,
    "confirmed": false,
    "extrapolated": true
  },
  "63": {
    "start": 19693394853,
    "window": 1342156369,
    "confirmed": false,
    "extrapolated": true
  },
  "64": {
    "start": 21035551222,
    "window": 1410671093,
    "confirmed": false,
    "extrapolated": true
  },
  "65": {
    "start": 22446222315,
    "window": 1481548171,
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
  },
  {
    "Level": 52,
    "Percent": 5.0,
    "Damage": 8744569531
  },
  {
    "Level": 51,
    "Percent": 58.0,
    "Damage": 8420718627
  },
  {
    "Level": 51,
    "Percent": 9.0,
    "Damage": 8087762144
  },
  {
    "Level": 51,
    "Percent": 0.0,
    "Damage": 8030587129
  },
  {
    "Level": 50,
    "Percent": 57.0,
    "Damage": 7760602853
  },
  {
    "Level": 37,
    "Percent": 60.0,
    "Damage": 2353685544
  },
  {
    "Level": 31,
    "Percent": 14.0,
    "Damage": 71589812
  },
  {
    "Level": 33,
    "Percent": 15.0,
    "Damage": 1404307520
  },
  {
    "Level": 29,
    "Percent": 56.0,
    "Damage": 846529318
  }
];
