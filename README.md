Here is your help!
(could be outdated....)

------------


- $help - This is already the help

Installation:
------------
1. [Add the bot](https://discordapp.com/api/oauth2/authorize?client_id=640587565329678337&permissions=8&scope=bot "Add the bot")
2. Claim the bot (sets you as the owner) with: ***$claim***
3. Set the Admin role with: ***$setrole @ admin***
4. Set the the commandchannel to the channel your are writing in (for admin commands as well as user commands) with: ***$setrcommandchannel*** 
5. Set the category for private channels with: ***$setcategory 'name'*** 
6. Have fun!

Things  you can try if the bot has problems:
------------
#### common problem:
###### The database (of all private channels) is not up to date.The database (of all private channels) is not up to date.
#### --> run the command: ***$resetprvchannels***
> side effect: 
All private channels get deleted

| Method  |   |
| ------------ | ------------ |
| let the bot rejoin | **dont kick** the bot!!! --> use instead the command: ***$leavesever*** (deletes the Server config) |
| try to init the bot manually | command: ***$initbot***    |
| reset the config | command: ***$resetconfig***    |




Private voicechannel commands:
------------
| Command  | Description  |
| ------------ | ------------ |
| $cv  | **C**reates a private **v**oicechannel  |
| $dv |**D**elete your private **v**oicechannel   |
| $rv "new name"   |**R**enames your private **v**oicechannel |
| $mvpu  | **M**akes your private **v**oicechannel **pu**blic  |
|  $mvpr | **M**akes your "private"  **v**oicechannel **pr**ivate again  |
|  $iuv  | **I**nvite a **U**ser to your **v**oicechannel  |
|  $ruv | **R**emove a **U**ser from your **v**oicechannel   |
| $rvd  | **R**eset your **v**oicechannel to **d**efault  |


Private textchannel commands:
------------
| Command  | Description  |
| ------------ | ------------ |
| $ct  | **C**reates a private **t**extchannel  |
| $dt |**D**eletes your private **t**extchannel   |
| $rt "new name"   |**R**enames your private **t**extchannel |
| $mtpu  | **M**akes your private **t**extchannel **pu**blic  |
|  $mtpr | **M**akes your "private"  **t**extchannel **pr**ivate again  |
|  $iut  | **I**nvite a **U**ser to your **t**extchannel  |
|  $rut | **R**emove a **U**ser from your **t**extchannel   |
| $rtd  | **R**eset your **t**extchannel to **d**efault  |


Admin stuff
------------
- $embeded "pastebin raw link" - creates an embeded message
- $initbot - Initializes the bot (should already be done by joining the server)
- $claim - Claims the power of the bot on this server. (only for setup)
- $claimadd user - Share your power with someone (only when you have power)
- $claimremove user - Steals power from someone (only when you have power)
- $claimreset - Resets the "claims" --revert all claimadd's (only when you have power)
- $setrole role - Sets the Admin role for the bot
- $setcommandchannel - Sets the commandchannel
- $settimeouttext "minutes" - Sets the timeout for private textchannels
- $settimeoutvoice "minutes" - Sets the timeout for private voicechannels
- $resetprvchannels - Resets the private channels category (only for Admins)
- $resetconfig - Resets the config for the server --reconfigure it
- $leaveserver - Say goodbye to this awesom bot --bot leaves 
