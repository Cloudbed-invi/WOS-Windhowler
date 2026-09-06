const LAST_UPDATED = 'September 06, 2026 - 23:33:03';
const EXACT_LEVELS = {
  "1": {
    "start": 0,
    "window": 24300
  },
  "23": {
    "start": 263733911,
    "window": 56812891
  },
  "25": {
    "start": 386599879,
    "window": 71766589
  },
  "26": {
    "start": 458087907,
    "window": 78710142
  },
  "27": {
    "start": 536742898,
    "window": 113490701
  },
  "28": {
    "start": 649866656,
    "window": 121149824
  },
  "29": {
    "start": 772045722,
    "window": 133066318
  },
  "30": {
    "start": 904986351,
    "window": 145148899
  },
  "32": {
    "start": 1206376257,
    "window": 169669783
  },
  "34": {
    "start": 1560277739,
    "window": 199034225
  },
  "36": {
    "start": 1973128831,
    "window": 235909825
  },
  "38": {
    "start": 2451976565,
    "window": 273967987
  },
  "39": {
    "start": 2723989318,
    "window": 285138965
  },
  "40": {
    "start": 3012978919,
    "window": 308545826
  },
  "41": {
    "start": 3324664306,
    "window": 332326245
  },
  "42": {
    "start": 3660540566,
    "window": 344230835
  },
  "43": {
    "start": 4020552848,
    "window": 379512961
  },
  "44": {
    "start": 4413593818,
    "window": 405491225
  },
  "45": {
    "start": 4823692161,
    "window": 415513658
  },
  "49": {
    "start": 6813311778,
    "window": 572935651
  }
};
const RAW_DATA = [
  {
    "Level": 17,
    "Percent": 29,
    "Damage": 72423951,
    "Name": "Community"
  },
  {
    "Level": 20,
    "Percent": 8,
    "Damage": 143414658,
    "Name": "Community"
  },
  {
    "Level": 21,
    "Percent": 1,
    "Damage": 173418819,
    "Name": "Community"
  },
  {
    "Level": 22,
    "Percent": 47,
    "Damage": 234200050,
    "Name": "Community"
  },
  {
    "Level": 23,
    "Percent": 47,
    "Damage": 290435970,
    "Name": "Community"
  },
  {
    "Level": 23,
    "Percent": 70,
    "Damage": 303502935,
    "Name": "Community"
  },
  {
    "Level": 24,
    "Percent": 53,
    "Damage": 355707410,
    "Name": "Community"
  },
  {
    "Level": 25,
    "Percent": 9,
    "Damage": 393058820,
    "Name": "Community"
  },
  {
    "Level": 25,
    "Percent": 14,
    "Damage": 397026845,
    "Name": "Community"
  },
  {
    "Level": 25,
    "Percent": 22,
    "Damage": 402311815,
    "Name": "Community"
  },
  {
    "Level": 25,
    "Percent": 67,
    "Damage": 434683450,
    "Name": "Community"
  },
  {
    "Level": 26,
    "Percent": 50,
    "Damage": 497914590,
    "Name": "Community"
  },
  {
    "Level": 27,
    "Percent": 17,
    "Damage": 556221612,
    "Name": "Community"
  },
  {
    "Level": 27,
    "Percent": 20,
    "Damage": 559441034,
    "Name": "Community"
  },
  {
    "Level": 27,
    "Percent": 79,
    "Damage": 626400558,
    "Name": "Community"
  },
  {
    "Level": 28,
    "Percent": 11,
    "Damage": 663193137,
    "Name": "Community"
  },
  {
    "Level": 28,
    "Percent": 16,
    "Damage": 669205486,
    "Name": "Community"
  },
  {
    "Level": 28,
    "Percent": 50,
    "Damage": 710441567,
    "Name": "Community"
  },
  {
    "Level": 29,
    "Percent": 30,
    "Damage": 811950970,
    "Name": "Community"
  },
  {
    "Level": 29,
    "Percent": 57,
    "Damage": 847594114,
    "Name": "Community"
  },
  {
    "Level": 29,
    "Percent": 72,
    "Damage": 867834427,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 3,
    "Damage": 901248419,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 0,
    "Damage": 905376879,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 5,
    "Damage": 912977123,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 11,
    "Damage": 921055692,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 27,
    "Damage": 944092374,
    "Name": "Community"
  },
  {
    "Level": 32,
    "Percent": 22,
    "Damage": 1243209406,
    "Name": "Community"
  },
  {
    "Level": 35,
    "Percent": 25,
    "Damage": 1812831025,
    "Name": "Community"
  },
  {
    "Level": 38,
    "Percent": 37,
    "Damage": 2554494393,
    "Name": "Community"
  },
  {
    "Level": 39,
    "Percent": 27,
    "Damage": 2799865740,
    "Name": "Community"
  },
  {
    "Level": 39,
    "Percent": 65,
    "Damage": 2909355975,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 22,
    "Damage": 3079843839,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 37,
    "Damage": 3126908935,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 40,
    "Damage": 3136414860,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 0,
    "Damage": 3013185586,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 5,
    "Damage": 3026563430,
    "Name": "Community"
  },
  {
    "Level": 41,
    "Percent": 18,
    "Damage": 3385200438,
    "Name": "Community"
  },
  {
    "Level": 41,
    "Percent": 37,
    "Damage": 3445924183,
    "Name": "Community"
  },
  {
    "Level": 41,
    "Percent": 61,
    "Damage": 3538623829,
    "Name": "Community"
  },
  {
    "Level": 41,
    "Percent": 67,
    "Damage": 3546430572,
    "Name": "Community"
  },
  {
    "Level": 42,
    "Percent": 3,
    "Damage": 3670692073,
    "Name": "Community"
  },
  {
    "Level": 42,
    "Percent": 6,
    "Damage": 3681348810,
    "Name": "Community"
  },
  {
    "Level": 42,
    "Percent": 13,
    "Damage": 3704877077,
    "Name": "Community"
  },
  {
    "Level": 42,
    "Percent": 14,
    "Damage": 3709595305,
    "Name": "Community"
  },
  {
    "Level": 43,
    "Percent": 10,
    "Damage": 4058504133,
    "Name": "Community"
  },
  {
    "Level": 43,
    "Percent": 39,
    "Damage": 4168562903,
    "Name": "Community"
  },
  {
    "Level": 44,
    "Percent": 73,
    "Damage": 4709602412,
    "Name": "Community"
  },
  {
    "Level": 44,
    "Percent": 93,
    "Damage": 4790700657,
    "Name": "Community"
  },
  {
    "Level": 45,
    "Percent": 6,
    "Damage": 4846951073,
    "Name": "Community"
  },
  {
    "Level": 45,
    "Percent": 41,
    "Damage": 5003198972,
    "Name": "Community"
  },
  {
    "Level": 49,
    "Percent": 17,
    "Damage": 6910710348,
    "Name": "Community"
  },
  {
    "Level": 49,
    "Percent": 27,
    "Damage": 6968005861,
    "Name": "Community"
  },
  {
    "Level": 56,
    "Percent": 2,
    "Damage": 11934638223,
    "Name": "Community"
  },
  {
    "Level": 26,
    "Percent": 77,
    "Damage": 518646735,
    "Name": "Community"
  },
  {
    "Level": 26,
    "Percent": 16,
    "Damage": 470584620,
    "Name": "Community"
  },
  {
    "Level": 26,
    "Percent": 1,
    "Damage": 458914560,
    "Name": "Community"
  },
  {
    "Level": 27,
    "Percent": 25,
    "Damage": 564865635,
    "Name": "Community"
  },
  {
    "Level": 28,
    "Percent": 22,
    "Damage": 676949194,
    "Name": "Community"
  },
  {
    "Level": 29,
    "Percent": 73,
    "Damage": 869206729,
    "Name": "Community"
  },
  {
    "Level": 29,
    "Percent": 56,
    "Damage": 847118322,
    "Name": "Community"
  },
  {
    "Level": 29,
    "Percent": 20,
    "Damage": 798670082,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 32,
    "Damage": 951557787,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 13,
    "Damage": 923816498,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 12,
    "Damage": 922204957,
    "Name": "Community"
  },
  {
    "Level": 30,
    "Percent": 1,
    "Damage": 906320690,
    "Name": "Community"
  },
  {
    "Level": 31,
    "Percent": 76,
    "Damage": 1169428592,
    "Name": "Community"
  },
  {
    "Level": 32,
    "Percent": 42,
    "Damage": 1277818431,
    "Name": "Community"
  },
  {
    "Level": 32,
    "Percent": 8,
    "Damage": 1220978042,
    "Name": "Community"
  },
  {
    "Level": 32,
    "Percent": 1,
    "Damage": 1207870410,
    "Name": "Community"
  },
  {
    "Level": 33,
    "Percent": 8,
    "Damage": 1390768940,
    "Name": "Community"
  },
  {
    "Level": 33,
    "Percent": 8,
    "Damage": 1390162486,
    "Name": "Community"
  },
  {
    "Level": 34,
    "Percent": 24,
    "Damage": 1608037167,
    "Name": "Community"
  },
  {
    "Level": 34,
    "Percent": 10,
    "Damage": 1580245074,
    "Name": "Community"
  },
  {
    "Level": 34,
    "Percent": 6,
    "Damage": 1572164665,
    "Name": "Community"
  },
  {
    "Level": 36,
    "Percent": 11,
    "Damage": 1999225319,
    "Name": "Community"
  },
  {
    "Level": 36,
    "Percent": 7,
    "Damage": 1989453612,
    "Name": "Community"
  },
  {
    "Level": 36,
    "Percent": 1,
    "Damage": 1975530429,
    "Name": "Community"
  },
  {
    "Level": 38,
    "Percent": 51,
    "Damage": 2591347146,
    "Name": "Community"
  },
  {
    "Level": 38,
    "Percent": 36,
    "Damage": 2550852025,
    "Name": "Community"
  },
  {
    "Level": 38,
    "Percent": 24,
    "Damage": 2517236147,
    "Name": "Community"
  },
  {
    "Level": 39,
    "Percent": 51,
    "Damage": 2869381096,
    "Name": "Community"
  },
  {
    "Level": 39,
    "Percent": 24,
    "Damage": 2792828121,
    "Name": "Community"
  },
  {
    "Level": 39,
    "Percent": 2,
    "Damage": 2729694860,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 23,
    "Damage": 3084268518,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 19,
    "Damage": 3072237542,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 16,
    "Damage": 3062038720,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 14,
    "Damage": 3056518900,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 13,
    "Damage": 3054087273,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 13,
    "Damage": 3052125362,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 11,
    "Damage": 3047049307,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 8,
    "Damage": 3038490601,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 4,
    "Damage": 3025439743,
    "Name": "Community"
  },
  {
    "Level": 40,
    "Percent": 0,
    "Damage": 3010842193,
    "Name": "Community"
  },
  {
    "Level": 45,
    "Percent": 45,
    "Damage": 5003198972,
    "Name": "Community"
  }
];
