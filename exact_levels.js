const LAST_UPDATED = 'September 07, 2026 - 21:30:47';
const EXTRAPOLATE_A = 594.3256073827774;
const EXTRAPOLATE_B = 4.180014256772481;
const EXACT_LEVELS = {
  "1": {
    "start": 0,
    "window": 24300,
    "confirmed": true
  },
  "2": {
    "start": 514459,
    "window": 1549176,
    "confirmed": false
  },
  "3": {
    "start": 2063635,
    "window": 2592592,
    "confirmed": false
  },
  "4": {
    "start": 4656228,
    "window": 3644707,
    "confirmed": false
  },
  "5": {
    "start": 8300935,
    "window": 4705521,
    "confirmed": false
  },
  "6": {
    "start": 13006455,
    "window": 5775033,
    "confirmed": false
  },
  "7": {
    "start": 18781489,
    "window": 6853244,
    "confirmed": false
  },
  "8": {
    "start": 25634733,
    "window": 7940154,
    "confirmed": false
  },
  "9": {
    "start": 33574887,
    "window": 9035763,
    "confirmed": false
  },
  "10": {
    "start": 42610650,
    "window": 10140071,
    "confirmed": false
  },
  "11": {
    "start": 52750721,
    "window": 11253077,
    "confirmed": false
  },
  "12": {
    "start": 64003797,
    "window": 12374782,
    "confirmed": false
  },
  "13": {
    "start": 76378579,
    "window": 13505186,
    "confirmed": false
  },
  "14": {
    "start": 89883765,
    "window": 14644288,
    "confirmed": false
  },
  "15": {
    "start": 104528054,
    "window": 15792090,
    "confirmed": false
  },
  "16": {
    "start": 120320143,
    "window": 16948590,
    "confirmed": false
  },
  "17": {
    "start": 137268734,
    "window": 18113789,
    "confirmed": false
  },
  "18": {
    "start": 155382523,
    "window": 19287687,
    "confirmed": false
  },
  "19": {
    "start": 174670210,
    "window": 20470284,
    "confirmed": false
  },
  "20": {
    "start": 195140493,
    "window": 21661579,
    "confirmed": false
  },
  "21": {
    "start": 216802072,
    "window": 22861573,
    "confirmed": false
  },
  "22": {
    "start": 239663645,
    "window": 24070266,
    "confirmed": false
  },
  "23": {
    "start": 263733911,
    "window": 56812891,
    "confirmed": true
  },
  "24": {
    "start": 314676194,
    "window": 71923685,
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
    "start": 1050060197,
    "window": 156316060,
    "confirmed": false
  },
  "32": {
    "start": 1206376257,
    "window": 169669783,
    "confirmed": true
  },
  "33": {
    "start": 1376380935,
    "window": 183896804,
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
    "start": 3012978919,
    "window": 308545826,
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
    "start": 4020552848,
    "window": 379512961,
    "confirmed": true
  },
  "44": {
    "start": 4413593818,
    "window": 405491225,
    "confirmed": true
  },
  "45": {
    "start": 4823692161,
    "window": 415513658,
    "confirmed": true
  },
  "46": {
    "start": 5271883455,
    "window": 476722272,
    "confirmed": false
  },
  "47": {
    "start": 5748605727,
    "window": 509497905,
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
    "start": 7393242274,
    "window": 587589379,
    "confirmed": false
  },
  "51": {
    "start": 7980831654,
    "window": 635724145,
    "confirmed": false
  },
  "52": {
    "start": 8616555798,
    "window": 726627482,
    "confirmed": false
  },
  "53": {
    "start": 9343183280,
    "window": 860299392,
    "confirmed": false
  },
  "54": {
    "start": 10203482672,
    "window": 822005214,
    "confirmed": true
  },
  "55": {
    "start": 11452965192,
    "window": -415723212,
    "confirmed": true
  },
  "56": {
    "start": 12529216623,
    "window": 1003910343,
    "confirmed": false
  },
  "57": {
    "start": 13533126966,
    "window": 899709255,
    "confirmed": false
  },
  "58": {
    "start": 14432836221,
    "window": 763648167,
    "confirmed": false
  },
  "59": {
    "start": 15196484388,
    "window": 374135904,
    "confirmed": true
  },
  "60": {
    "start": 16096150355,
    "window": 1151447049,
    "confirmed": false,
    "extrapolated": true
  },
  "61": {
    "start": 17247597404,
    "window": 1213064082,
    "confirmed": false,
    "extrapolated": true
  },
  "62": {
    "start": 18460661486,
    "window": 1276904383,
    "confirmed": false,
    "extrapolated": true
  },
  "63": {
    "start": 19737565870,
    "window": 1343010673,
    "confirmed": false,
    "extrapolated": true
  },
  "64": {
    "start": 21080576542,
    "window": 1411425793,
    "confirmed": false,
    "extrapolated": true
  },
  "65": {
    "start": 22492002335,
    "window": 1482192709,
    "confirmed": false,
    "extrapolated": true
  }
};
const RAW_DATA = [
  {
    "Level": 17,
    "Percent": 29.0,
    "Damage": 72423951,
    "Name": "Community"
  },
  {
    "Level": 20,
    "Percent": 8.0,
    "Damage": 143414658,
    "Name": "Community"
  },
  {
    "Level": 21,
    "Percent": 1.0,
    "Damage": 173418819,
    "Name": "Community"
  },
  {
    "Level": 22,
    "Percent": 47.0,
    "Damage": 234200050,
    "Name": "Community"
  },
  {
    "Level": 23,
    "Percent": 47.0,
    "Damage": 290435970,
    "Name": "Community"
  },
  {
    "Level": 23,
    "Percent": 70.0,
    "Damage": 303502935,
    "Name": "Community"
  },
  {
    "Level": 24,
    "Percent": 53.0,
    "Damage": 355707410,
    "Name": "Community"
  },
  {
    "Level": 25,
    "Percent": 9.0,
    "Damage": 393058820,
    "Name": "Community"
  },
  {
    "Level": 25,
    "Percent": 14.0,
    "Damage": 397026845,
    "Name": "Community"
  },
  {
    "Level": 25,
    "Percent": 22.0,
    "Damage": 402311815,
    "Name": "Community"
  },
  {
    "Level": 25,
    "Percent": 67.0,
    "Damage": 434683450,
    "Name": "Community"
  },
  {
    "Level": 26,
    "Percent": 50.0,
    "Damage": 497914590,
    "Name": "Community"
  },
  {
    "Level": 27,
    "Percent": 17.0,
    "Damage": 556221612,
    "Name": "Community"
  },
  {
    "Level": 27,
    "Percent": 20.0,
    "Damage": 559441034,
    "Name": "Community"
  },
  {
    "Level": 27,
    "Percent": 79.0,
    "Damage": 626400558,
    "Name": "Community"
  },
  {
    "Level": 28,
    "Percent": 11.0,
    "Damage": 663193137,
    "Name": "Community"
  },
  {
    "Level": 28,
    "Percent": 16.0,
    "Damage": 669205486,
    "Name": "Community"
  },
  {
    "Level": 28,
    "Percent": 50.0,
    "Damage": 710441567,
    "Name": "Community"
  },
  {
    "Level": 29,
    "Percent": 30.0,
    "Damage": 811950970,
    "Name": "Community"
  },
  {
    "Level": 29,
    "Percent": 57.0,
    "Damage": 847594114,
    "Name": "Community"
  },
  {
    "Level": 29,
    "Percent": 72.0,
    "Damage": 867834427,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 3.0,
    "Damage": 901248419,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 0.0,
    "Damage": 905376879,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 5.0,
    "Damage": 912977123,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 11.0,
    "Damage": 921055692,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 27.0,
    "Damage": 944092374,
    "Name": "Community"
  },
  {
    "Level": 32,
    "Percent": 22.0,
    "Damage": 1243209406,
    "Name": "Community"
  },
  {
    "Level": 35,
    "Percent": 25.0,
    "Damage": 1812831025,
    "Name": "Community"
  },
  {
    "Level": 38,
    "Percent": 37.0,
    "Damage": 2554494393,
    "Name": "Community"
  },
  {
    "Level": 39,
    "Percent": 27.0,
    "Damage": 2799865740,
    "Name": "Community"
  },
  {
    "Level": 39,
    "Percent": 65.0,
    "Damage": 2909355975,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 22.0,
    "Damage": 3079843839,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 37.0,
    "Damage": 3126908935,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 40.0,
    "Damage": 3136414860,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 0.0,
    "Damage": 3013185586,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 5.0,
    "Damage": 3026563430,
    "Name": "Community"
  },
  {
    "Level": 41,
    "Percent": 18.0,
    "Damage": 3385200438,
    "Name": "Community"
  },
  {
    "Level": 41,
    "Percent": 37.0,
    "Damage": 3445924183,
    "Name": "Community"
  },
  {
    "Level": 41,
    "Percent": 61.0,
    "Damage": 3538623829,
    "Name": "Community"
  },
  {
    "Level": 41,
    "Percent": 67.0,
    "Damage": 3546430572,
    "Name": "Community"
  },
  {
    "Level": 42,
    "Percent": 3.0,
    "Damage": 3670692073,
    "Name": "Community"
  },
  {
    "Level": 42,
    "Percent": 6.0,
    "Damage": 3681348810,
    "Name": "Community"
  },
  {
    "Level": 42,
    "Percent": 13.0,
    "Damage": 3704877077,
    "Name": "Community"
  },
  {
    "Level": 42,
    "Percent": 14.0,
    "Damage": 3709595305,
    "Name": "Community"
  },
  {
    "Level": 43,
    "Percent": 10.0,
    "Damage": 4058504133,
    "Name": "Community"
  },
  {
    "Level": 43,
    "Percent": 39.0,
    "Damage": 4168562903,
    "Name": "Community"
  },
  {
    "Level": 44,
    "Percent": 73.0,
    "Damage": 4709602412,
    "Name": "Community"
  },
  {
    "Level": 44,
    "Percent": 93.0,
    "Damage": 4790700657,
    "Name": "Community"
  },
  {
    "Level": 45,
    "Percent": 6.0,
    "Damage": 4846951073,
    "Name": "Community"
  },
  {
    "Level": 45,
    "Percent": 41.0,
    "Damage": 5003198972,
    "Name": "Community"
  },
  {
    "Level": 49,
    "Percent": 17.0,
    "Damage": 6910710348,
    "Name": "Community"
  },
  {
    "Level": 49,
    "Percent": 27.0,
    "Damage": 6968005861,
    "Name": "Community"
  },
  {
    "Level": 56,
    "Percent": 2.0,
    "Damage": 11934638223,
    "Name": "Community"
  },
  {
    "Level": 26,
    "Percent": 77.0,
    "Damage": 518646735,
    "Name": "Community"
  },
  {
    "Level": 26,
    "Percent": 16.0,
    "Damage": 470584620,
    "Name": "Community"
  },
  {
    "Level": 26,
    "Percent": 1.0,
    "Damage": 458914560,
    "Name": "Community"
  },
  {
    "Level": 27,
    "Percent": 25.0,
    "Damage": 564865635,
    "Name": "Community"
  },
  {
    "Level": 28,
    "Percent": 22.0,
    "Damage": 676949194,
    "Name": "Community"
  },
  {
    "Level": 29,
    "Percent": 73.0,
    "Damage": 869206729,
    "Name": "Community"
  },
  {
    "Level": 29,
    "Percent": 56.0,
    "Damage": 847118322,
    "Name": "Community"
  },
  {
    "Level": 29,
    "Percent": 20.0,
    "Damage": 798670082,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 32.0,
    "Damage": 951557787,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 13.0,
    "Damage": 923816498,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 12.0,
    "Damage": 922204957,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 1.0,
    "Damage": 906320690,
    "Name": "Community"
  },
  {
    "Level": 31,
    "Percent": 76.0,
    "Damage": 1169428592,
    "Name": "Community"
  },
  {
    "Level": 32,
    "Percent": 42.0,
    "Damage": 1277818431,
    "Name": "Community"
  },
  {
    "Level": 32,
    "Percent": 8.0,
    "Damage": 1220978042,
    "Name": "Community"
  },
  {
    "Level": 32,
    "Percent": 1.0,
    "Damage": 1207870410,
    "Name": "Community"
  },
  {
    "Level": 33,
    "Percent": 8.0,
    "Damage": 1390768940,
    "Name": "Community"
  },
  {
    "Level": 33,
    "Percent": 8.0,
    "Damage": 1390162486,
    "Name": "Community"
  },
  {
    "Level": 34,
    "Percent": 24.0,
    "Damage": 1608037167,
    "Name": "Community"
  },
  {
    "Level": 34,
    "Percent": 10.0,
    "Damage": 1580245074,
    "Name": "Community"
  },
  {
    "Level": 34,
    "Percent": 6.0,
    "Damage": 1572164665,
    "Name": "Community"
  },
  {
    "Level": 36,
    "Percent": 11.0,
    "Damage": 1999225319,
    "Name": "Community"
  },
  {
    "Level": 36,
    "Percent": 7.0,
    "Damage": 1989453612,
    "Name": "Community"
  },
  {
    "Level": 36,
    "Percent": 1.0,
    "Damage": 1975530429,
    "Name": "Community"
  },
  {
    "Level": 38,
    "Percent": 51.0,
    "Damage": 2591347146,
    "Name": "Community"
  },
  {
    "Level": 38,
    "Percent": 36.0,
    "Damage": 2550852025,
    "Name": "Community"
  },
  {
    "Level": 38,
    "Percent": 24.0,
    "Damage": 2517236147,
    "Name": "Community"
  },
  {
    "Level": 39,
    "Percent": 51.0,
    "Damage": 2869381096,
    "Name": "Community"
  },
  {
    "Level": 39,
    "Percent": 24.0,
    "Damage": 2792828121,
    "Name": "Community"
  },
  {
    "Level": 39,
    "Percent": 2.0,
    "Damage": 2729694860,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 23.0,
    "Damage": 3084268518,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 19.0,
    "Damage": 3072237542,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 16.0,
    "Damage": 3062038720,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 14.0,
    "Damage": 3056518900,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 13.0,
    "Damage": 3054087273,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 13.0,
    "Damage": 3052125362,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 11.0,
    "Damage": 3047049307,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 8.0,
    "Damage": 3038490601,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 4.0,
    "Damage": 3025439743,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 0.0,
    "Damage": 3010842193,
    "Name": "Community"
  },
  {
    "Level": 45,
    "Percent": 45.0,
    "Damage": 5003198972,
    "Name": "Community"
  },
  {
    "Level": 55,
    "Percent": 11.0,
    "Damage": 11130743954,
    "Name": "Unknown"
  },
  {
    "Level": 55,
    "Percent": 31.0,
    "Damage": 11305019779,
    "Name": "Unknown"
  },
  {
    "Level": 54,
    "Percent": 66.0,
    "Damage": 10746042837,
    "Name": "Unknown"
  },
  {
    "Level": 54,
    "Percent": 45.0,
    "Damage": 10573100534,
    "Name": "Unknown"
  },
  {
    "Level": 54,
    "Percent": 19.0,
    "Damage": 10359674661,
    "Name": "Unknown"
  },
  {
    "Level": 47,
    "Percent": 65.0,
    "Damage": 6078886524,
    "Name": "Unknown"
  },
  {
    "Level": 48,
    "Percent": 27.0,
    "Damage": 6406734869,
    "Name": "Unknown"
  },
  {
    "Level": 48,
    "Percent": 15.0,
    "Damage": 6343805523,
    "Name": "Unknown"
  },
  {
    "Level": 48,
    "Percent": 5.0,
    "Damage": 6288498422,
    "Name": "Unknown"
  },
  {
    "Level": 47,
    "Percent": 57.0,
    "Damage": 6040128124,
    "Name": "Unknown"
  },
  {
    "Level": 49,
    "Percent": 58.0,
    "Damage": 7151017277,
    "Name": "Unknown"
  },
  {
    "Level": 48,
    "Percent": 79.0,
    "Damage": 6693657402,
    "Name": "Unknown"
  },
  {
    "Level": 48,
    "Percent": 31.0,
    "Damage": 6431148202,
    "Name": "Unknown"
  },
  {
    "Level": 48,
    "Percent": 23.0,
    "Damage": 6385632402,
    "Name": "Unknown"
  },
  {
    "Level": 63,
    "Percent": 68.0,
    "Damage": 21055194115,
    "Name": "Admin"
  },
  {
    "Level": 47,
    "Percent": 0.0,
    "Damage": 5748068630,
    "Name": "Unknown"
  },
  {
    "Level": 47,
    "Percent": 55.0,
    "Damage": 6027952006,
    "Name": "Unknown"
  },
  {
    "Level": 47,
    "Percent": 40.0,
    "Damage": 5953603835,
    "Name": "Unknown"
  },
  {
    "Level": 55,
    "Percent": 9.0,
    "Damage": 11711113204,
    "Name": "Unknown"
  },
  {
    "Level": 59,
    "Percent": 32.0,
    "Damage": 15318012829,
    "Name": "Unknown"
  },
  {
    "Level": 59,
    "Percent": 30.0,
    "Damage": 15299108251,
    "Name": "Unknown"
  },
  {
    "Level": 59,
    "Percent": 33.0,
    "Damage": 15327761214,
    "Name": "Unknown"
  }
];
