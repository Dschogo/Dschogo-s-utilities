Here is your help!
(could be outdated....)

------------


- $help - This is already the help

Installation:
------------
1. [Add the bot](https://discordapp.com/api/oauth2/authorize?client_id=640587565329678337&permissions=8&scope=bot "Add the bot")
2. Claim the bot (sets you as the owner) with: ***$claim***
3. Set the Admin role with: ***$setrole role &diams;***
4. Set the the commandchannel to the channel your are writing in (for admin commands as well as user commands) with: ***$setrcommandchannel &diams;***  / ***$setadmincommandchannel &diams;***
5. Set timeout for voice / textchannels: ***$settimeouttext &acute;min&acute; *** and ***$settimeoutvoice &acute;min&acute; *** 
6. Set the category for private channels with: ***$setcategory &acute;name&acute;*** 
7. Set the logging channel (recommended even if you dont use this feature): ***$setlogchannel &diams;*** [enable logging with ***$setlogging true***]
7. Have fun!

&diams; user / role are mentions --> '@' for roles and users or '#' for channels

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
| try to init the bot manually (to recreate all files) | command: ***$initbot***    |
| reset the config (only config reset, no restructure of files) | command: ***$resetconfig***    |


More help on this Discord: https://discord.gg/2hNjK54

Private voicechannel commands:
------------
| Command  | Description  |
| ------------ | ------------ |
| $cv  | **C**reates a private **v**oicechannel  |
| $dv |**D**elete your private **v**oicechannel   |
| $rv &quot;new name&quot;   |**R**enames your private **v**oicechannel |
| $mvpu  | **M**akes your private **v**oicechannel **pu**blic  |
| $mvpr | **M**akes your "private"  **v**oicechannel **pr**ivate again  |
| $iuv  | **I**nvite a **U**ser to your **v**oicechannel  |
| $ruv | **R**emove a **U**ser from your **v**oicechannel   |
| $rvd  | **R**eset your **v**oicechannel to **d**efault  |


Private textchannel commands:
------------
| Command  | Description  |
| ------------ | ------------ |
| $ct  | **C**reates a private **t**extchannel  |
| $dt |**D**eletes your private **t**extchannel   |
| $rt &quot;new name&quot;   |**R**enames your private **t**extchannel |
| $mtpu  | **M**akes your private **t**extchannel **pu**blic  |
| $mtpr | **M**akes your &quot;private&quot;  **t**extchannel **pr**ivate again  |
| $iut  | **I**nvite a **U**ser to your **t**extchannel  |
| $rut | **R**emove a **U**ser from your **t**extchannel   |
| $rtd  | **R**eset your **t**extchannel to **d**efault  |

Moderation commands
------------
| Voicechannels:  |   |
| ------------ | ------------ |
| $mcv user &diams;  | **C**reates a private **v**oicechannel for a user  |
| $mdv user &diams;|**D**eletes a private **v**oicechannel  from a user |
| $mrv user &diams;  &quot;new name&quot;   |**R**enames a private **v**oicechannel of a user|
| $mmvpu  user &diams;| **M**akes user's private **v**oicechannel **pu**blic  |
| $mmvpr user &diams;| **M**akes your &quot;private&quot;  **v**oicechannel **pr**ivate again  |
| $miuv  user &diams; user &diams;| **I**nvite **U**ser (2. mention) to the **v**oicechannel of the user (1. mention) |
| $mruv user &diams; user &diams; | **R**emove **U**ser (2. mention) from the **v**oicechannel of the user (1.mention) |
| $mrvd user &diams; | **R**eset the **v**oicechannel to **d**efault of mentioned user  |
| Textchannels:  |   |
| $mct user &diams;  | **C**reates a private **t**extchannel for a user  |
| $mdt user &diams;|**D**eletes a private **t**extchannel  from a user |
| $mrt user &diams;  &quot;new name&quot;   |**R**enames a private **t**extchannel of a user|
| $mmtpu  user &diams;| **M**akes user's private **v**extchannel **pu**blic  |
| $mmtpr user &diams;| **M**akes your &quot;private&quot;  **t**extchannel **pr**ivate again  |
| $miut  user &diams; user &diams;| **I**nvite **U**ser (2. mention) to the **t**extchannel of the user (1. mention) |
| $mrut user &diams; user &diams; | **R**emove **U**ser (2. mention) from the **t**extchannel of the user (1.mention) |
| $mrtd user &diams; | **R**eset the **t**extchannel to **d**efault of mentioned user  |

&diams; user / role are mentions --> '@' for roles and users or '#' for channels

Admin stuff
------------
| Command  | Description  |
| ------------ | ------------ |
| $showsettings | shows the current config |
| $setlogging true/false | enable/discable logging |
| $setlogchannel &diams; | sets the logchannel |
| $embeded &quot;pastebin raw link&quot; | creates a rich-embeded message (explanation at the end)|
| $sethelp &quot;pastebin raw link&quot; | sets the help message|
| $initbot | Initializes the bot (should already be done by joining the server)  |
| $claim | Claims the power of the bot on this server (sets you as master). (only for setup) |
| $claimadd user &diams; | Share your power with someone (only when you have power) |
| $claimremove user&diams; | Steals power from someone (only when you have power) |
| $claimreset | Resets the &quot;claims&quot; &rarr; revert all claimadd&acute;s  &rarr; the first &quot;master&quot; stays (only when you have power) |
| $setrole role &diams; | Sets the Admin role for the bot |
| $setcommandchannel |  Sets the commandchannel (for user commands)  |
| $setadmincommandchannel |  Sets the admincommandchannel W(for admin commands)  |
| $settimeouttext &quot;minutes&quot; | Sets the timeout for private textchannels |
| $settimeoutvoice &quot;minutes&quot; | Sets the timeout for private voicechannels |
| $resetprvchannels | Resets the private channels category (only for Admins) |
| $resetconfig | Resets the config for the server --reconfigure it |
| $leaveserver  | Say goodbye to this awesom bot --bot leaves  |

&diams; user / role are mentions --> '@' for roles and users or '#' for channels
