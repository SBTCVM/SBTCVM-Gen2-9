## SBTCVM Tilemap graphics plan:



#### initial screen mode:

 - 486 __(18 27x27 tiles)__ by 378 __(14 27x27 tiles)__ _**MAY BE TOO BIG**_
 - 243 __(9 27x27 tiles)__ by 189 __(7 27x27 tiles)__ _**START WITH THIS ONE**_


#### Technical details:

 - 27x27 pixel tiles (1-trit mono/3-trit RGB)
 - tiles loaded via DMA into indirect memory. (converted and preupscaled as well)
 - 5-trit tile IDs (243 tiles)
 - loading a tile on an existing tileid will override it.
 - tilemap is 4-trits by 4-trits. 81 by 81
 - tilemap accessible via 4-trit by 4-trit IO-accessed indirect memory pool.
 - maximum 9 sprites __tilemap ID based, no alpha channel__
 - scroll offset is controlled via 0-26 x and y pixel offsets, 
    and separate x and y tile offsets.
 - sprite positions are screen-locked x and y pixel offsets.
 
