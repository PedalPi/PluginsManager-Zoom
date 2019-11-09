# Instructions

1. Run `retriever/patch_params_save_data.py` to retrieve information about the params;
1. Run `retriever/patch_effects_save_data.py` to retrieve information about the effects;
1. Run `retriever/patch_effects_status_save_data.py` to retrieve information about the effect status;
1. Run `patch_bits_table.py` to generate a table like [zoom-ms-utility multistomp table](https://github.com/g200kg/zoom-ms-utility/blob/master/midimessage.md);

## Table legend

The generated table is a list that each item is other list that represents a byte.
The "byte list" contains eight elements (eight bits), one element inform that information is presented over the bit.
As example, the byte
```
[0 '0tb6' '0p0b6' '0p1b1' '0p1b9' '0p2b4' 0 '0p3b7']
```
informs that:
 * the first bit informs something that I don't unknown;
 * the third bit about a param value
 
The codes legend is:
* `0`: **unknown** - not mapped information
* `EpPbB`: **Param value** - B-th byte that corresponds the param value of the P-th param of the E-th effect
* `AEfOn`: **State** - Bit about the A-th effect that informs the current state (on, off)
* `EtbB`: **Effect** - B-th bit that informs the E-effect
* `volumeV`: **Volume** - V-th bit of the volume data
* `nameLbB`: **Name** - B-th bit of the L-th letter
  