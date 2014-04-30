colorTable = bytearray([
0x80,0x80,0x80,
0x81,0x80,0x80,
0x82,0x80,0x80,
0x83,0x80,0x80,
0x84,0x80,0x80,
0x85,0x80,0x80,
0x86,0x80,0x80,
0x87,0x80,0x80,
0x88,0x80,0x80,
0x89,0x80,0x80,
0x8a,0x80,0x80,
0x8b,0x80,0x80,
0x8c,0x80,0x80,
0x8d,0x80,0x80,
0x8e,0x80,0x80,
0x8f,0x80,0x80,
0x90,0x80,0x80,
0x91,0x80,0x80,
0x92,0x80,0x80,
0x93,0x80,0x80,
0x94,0x80,0x80,
0x95,0x81,0x80,
0x96,0x81,0x80,
0x97,0x81,0x80,
0x98,0x81,0x80,
0x99,0x81,0x80,
0x9a,0x82,0x80,
0x9b,0x82,0x80,
0x9c,0x82,0x80,
0x9d,0x83,0x80,
0x9e,0x83,0x80,
0x9f,0x83,0x80,
0xa0,0x84,0x80,
0xa0,0x84,0x80,
0xa1,0x84,0x80,
0xa2,0x85,0x80,
0xa3,0x85,0x80,
0xa4,0x86,0x80,
0xa5,0x86,0x80,
0xa6,0x87,0x80,
0xa7,0x87,0x80,
0xa8,0x87,0x80,
0xa9,0x88,0x80,
0xaa,0x89,0x80,
0xab,0x89,0x80,
0xac,0x8a,0x80,
0xad,0x8a,0x80,
0xae,0x8b,0x80,
0xaf,0x8c,0x80,
0xb0,0x8c,0x80,
0xb1,0x8d,0x80,
0xb2,0x8d,0x80,
0xb3,0x8e,0x80,
0xb4,0x8f,0x80,
0xb5,0x8f,0x80,
0xb6,0x90,0x80,
0xb7,0x91,0x80,
0xb8,0x92,0x80,
0xb9,0x92,0x80,
0xba,0x93,0x80,
0xbb,0x94,0x80,
0xbc,0x95,0x80,
0xbd,0x95,0x80,
0xbe,0x96,0x80,
0xbf,0x97,0x80,
0xc0,0x98,0x80,
0xc1,0x99,0x80,
0xc2,0x99,0x80,
0xc3,0x9a,0x80,
0xc4,0x9b,0x80,
0xc5,0x9c,0x80,
0xc5,0x9d,0x80,
0xc6,0x9e,0x80,
0xc7,0x9f,0x80,
0xc8,0xa0,0x80,
0xc9,0xa1,0x80,
0xca,0xa2,0x80,
0xcb,0xa3,0x80,
0xcc,0xa4,0x80,
0xcd,0xa5,0x80,
0xce,0xa6,0x80,
0xcf,0xa7,0x80,
0xd0,0xa8,0x80,
0xd1,0xa9,0x80,
0xd2,0xaa,0x80,
0xd3,0xab,0x80,
0xd4,0xac,0x80,
0xd5,0xad,0x80,
0xd6,0xaf,0x80,
0xd7,0xb0,0x80,
0xd7,0xb1,0x80,
0xd8,0xb2,0x80,
0xd9,0xb3,0x80,
0xda,0xb4,0x80,
0xdb,0xb6,0x80,
0xdc,0xb7,0x80,
0xdd,0xb8,0x80,
0xde,0xba,0x80,
0xdf,0xbb,0x80,
0xe0,0xbc,0x80,
0xe1,0xbd,0x80,
0xe2,0xbf,0x80,
0xe3,0xc0,0x80,
0xe3,0xc2,0x80,
0xe4,0xc3,0x80,
0xe5,0xc4,0x80,
0xe6,0xc6,0x80,
0xe7,0xc7,0x80,
0xe8,0xc8,0x80,
0xe9,0xca,0x80,
0xea,0xcb,0x80,
0xeb,0xcc,0x80,
0xec,0xce,0x80,
0xed,0xcf,0x80,
0xed,0xd1,0x80,
0xee,0xd2,0x80,
0xef,0xd3,0x80,
0xf0,0xd4,0x80,
0xeb,0xd5,0x80,
0xeb,0xd5,0x80,
0xeb,0xd6,0x80,
0xea,0xd7,0x80,
0xea,0xd7,0x80,
0xea,0xd8,0x80,
0xe9,0xd8,0x80,
0xe9,0xd9,0x80,
0xe9,0xda,0x80,
0xe8,0xda,0x80,
0xe8,0xdb,0x80,
0xe7,0xdc,0x80,
0xe7,0xdd,0x80,
0xe6,0xdd,0x80,
0xe6,0xde,0x80,
0xe5,0xde,0x80,
0xe4,0xdf,0x81,
0xe3,0xdf,0x82,
0xe2,0xdf,0x83,
0xe1,0xdf,0x83,
0xe0,0xdf,0x84,
0xdf,0xdf,0x85,
0xde,0xdf,0x86,
0xdd,0xdf,0x87,
0xdc,0xdf,0x88,
0xdb,0xdf,0x88,
0xda,0xdf,0x89,
0xd9,0xdf,0x8a,
0xd8,0xdf,0x8b,
0xd8,0xdf,0x8c,
0xd7,0xdf,0x8d,
0xd6,0xdf,0x8d,
0xd5,0xdf,0x8e,
0xd4,0xdf,0x8f,
0xd4,0xdf,0x90,
0xd3,0xdf,0x91,
0xd2,0xdf,0x92,
0xd1,0xdf,0x92,
0xd0,0xdf,0x93,
0xd0,0xdf,0x94,
0xcf,0xdf,0x95,
0xce,0xdf,0x96,
0xce,0xdf,0x96,
0xcd,0xdf,0x97,
0xcc,0xdf,0x98,
0xcc,0xdf,0x99,
0xcb,0xdf,0x9a,
0xcb,0xdf,0x9a,
0xca,0xdf,0x9b,
0xc9,0xdf,0x9c,
0xc9,0xdf,0x9d,
0xc8,0xdf,0x9e,
0xc8,0xdf,0x9e,
0xc7,0xdf,0x9f,
0xc7,0xdf,0xa0,
0xc6,0xdf,0xa1,
0xc6,0xdf,0xa2,
0xc5,0xdf,0xa2,
0xc5,0xdf,0xa3,
0xc5,0xdf,0xa4,
0xc4,0xdf,0xa5,
0xc4,0xdf,0xa5,
0xc3,0xdf,0xa6,
0xc3,0xdf,0xa7,
0xc3,0xdf,0xa8,
0xc2,0xdf,0xa8,
0xc2,0xdf,0xa9,
0xc2,0xdf,0xaa,
0xc1,0xdf,0xab,
0xc1,0xdf,0xab,
0xc1,0xdf,0xac,
0xc1,0xdf,0xad,
0xc0,0xdf,0xae,
0xc0,0xdf,0xae,
0xc0,0xdf,0xaf,
0xc0,0xdf,0xb0,
0xbf,0xdf,0xb0,
0xbf,0xdf,0xb1,
0xbf,0xdf,0xb2,
0xbf,0xdf,0xb3,
0xbf,0xdf,0xb3,
0xbf,0xdf,0xb4,
0xbe,0xdf,0xb5,
0xbe,0xdf,0xb5,
0xbe,0xdf,0xb6,
0xbe,0xdf,0xb7,
0xbe,0xdf,0xb8,
0xbe,0xdf,0xb8,
0xbe,0xdf,0xb9,
0xbe,0xdf,0xba,
0xbe,0xdf,0xba,
0xbe,0xdf,0xbb,
0xbe,0xdf,0xbc,
0xbe,0xdf,0xbc,
0xbe,0xdf,0xbd,
0xbe,0xdf,0xbe,
0xbe,0xdf,0xbf,
0xbe,0xdf,0xc0,
0xbe,0xdf,0xc2,
0xc0,0xdf,0xc3,
0xc1,0xdf,0xc4,
0xc2,0xdf,0xc5,
0xc2,0xdf,0xc7,
0xc3,0xdf,0xc8,
0xc4,0xdf,0xc9,
0xc4,0xdf,0xca,
0xc5,0xdf,0xcb,
0xc5,0xdf,0xcc,
0xc6,0xdf,0xcd,
0xc7,0xdf,0xcf,
0xc7,0xdf,0xd0,
0xc8,0xdf,0xd1,
0xc9,0xdf,0xd2,
0xc9,0xdf,0xd3,
0xca,0xdf,0xd4,
0xca,0xdf,0xd5,
0xcb,0xdf,0xd6,
0xcc,0xdf,0xd7,
0xcc,0xdf,0xd8,
0xcd,0xdf,0xd9,
0xcd,0xdf,0xda,
0xce,0xdf,0xdb,
0xcf,0xdf,0xdc,
0xcf,0xdf,0xdd,
0xd0,0xdf,0xdd,
0xd0,0xdf,0xde,
0xd1,0xdf,0xdf,
0xd1,0xdf,0xe0,
0xd2,0xdf,0xe1,
0xd3,0xdf,0xe2,
0xd3,0xdf,0xe3,
0xd4,0xdf,0xe3,
0xd4,0xdf,0xe4,
0xd5,0xdf,0xe5,
0xd5,0xdf,0xe6,
0xd6,0xdf,0xe6,
0xd6,0xdf,0xe7,
0xd7,0xdf,0xe8
])
