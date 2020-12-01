Here is your help!
(could be outdated....)

------------


- $help - This is already the help

Installation:
------------
1. [Add the bot](https://discord.com/api/oauth2/authorize?client_id=735961860607574096&permissions=8&scope=bot "Add the bot")
2. Set the the commandchannel with: ***$setprvcommandchannel &diams;*** 
3. Set the help file (recommended to enhance user experience): ***$sethelp &quot;pastebin raw link&quot;*** (pastebin works well and is free) [Template Help](https://github.com/Dschogo/Dschogo-s-utilities/blob/master/template_help)
4. Have fun!

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
| let the bot rejoin | **dont kick** the bot!!! --> use instead the command: ***$leavemyserverandiknowwhatiamdoing*** (deletes the Server config) |
| try to init the bot manually (to recreate all files) | command: ***$initbot***    |

More help on this Discord: https://discord.gg/2hNjK54

To use Prvrooms you need to enable this feature with ***$enableprv true*** (disable with: $enableprv false)


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

Get your status of the Prvrooms with ***$status***

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


To use "Fun" you need to enable this feature with ***$enablefun true*** (disable with: $enablefun false)

Fun stuff:
------------
| Command:  | Effect:  |
| ------------ | ------------ |
| $avatar &diams; | Send you the profile picture back as image |
| $createdacc &diams; | Returns the creation date of the user |
| $joined &diams; | Returns the joined date to this guild |
| $choose &diams;&diams;&diams;... | Choose between mentioned Users |
| $number a b | Return a random number between the given Numbers "a" and "b" (including "a" and "b") |

&diams; user / role are mentions --> '@' for roles and users or '#' for channels

Admin stuff
------------
| Command  | Description  |
| ------------ | ------------ |
| $enableprv true/false | enable/disable prv system |
| $enablefun true/false | enable/disable fun system|
| $setfunchannel &diams; | Define the fun channel |
| $showsettings | shows the current config |
| $setlogging true/false | enable/disable logging (role changes) |
| $setlogchannel &diams; | sets the logchannel |
| $setvoicelogging  true/false | enable/disable logging of a specific voicechannel (support channel join notifications)|
| $setvoicelogchannel &diams; | Sets the output channel for voicelogging |
| $setvoiceloggedchannel "ID" | The logged voice channel ***replace ID whit the channel id (rightclick voicechannel)***|
| $embeded &quot;pastebin raw link&quot; | creates a rich-embeded message (explanation at the end)|
| $sethelp &quot;pastebin raw link&quot; | sets the help message|
| $initbot | Initializes the bot (should already be done by joining the server)  |
| $setprvcommandchannel |  Sets the commandchannel (for user commands)  |
| $setprvtimeouttext &quot;minutes&quot; | Sets the timeout for private textchannels |
| $setprvtimeoutvoice &quot;minutes&quot; | Sets the timeout for private voicechannels |
| $setprvpermrole &quot;minutes&quot; | Define a role which is added to any voicechannel and textchannel (music bot) |
| $adminstatus | lists the status from every prvchannel |
| $statusof &diams; | Status of someone |
| $resetprvchannels | Resets the private channels category (only for Admins) |
| $resetprvchannels | Resets the private channels category (only for Admins) |
| $leavemyserverandiknowwhatiamdoing  | Say goodbye to this awesom bot --bot leaves  |

&diams; user / role are mentions --> '@' for roles and users or '#' for channels
