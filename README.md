# PraccForces

Competitive programming Discord bot!

Praccforces makes practicing for competitive coding easier by providing easy and fast access to codeforces problemset.

Filter problems By tags or score.

Get practice contests.

[![Discord Bots](https://top.gg/api/widget/status/794901156890673162.svg)](https://top.gg/bot/691416325557452861)
[![Discord Bots](https://top.gg/api/widget/servers/794901156890673162.svg)](https://top.gg/bot/691416325557452861)

![Praccforces](https://top.gg/_next/image?url=https%3A%2F%2Fimages.discordapp.net%2Favatars%2F794901156890673162%2F8de21d514c9f90fb9ed09de7d2f2be1c.png%3Fsize%3D128&w=128&q=75)
[Invite me to your server!](https://discord.com/oauth2/authorize?client_id=794901156890673162&permissions=380104993856&scope=bot%20applications.commands)

Support Praccforces by voting for it at [TOP.GG](https://top.gg/bot/794901156890673162/vote)

### Wild tag:

Now you can use the '\*' wild tag to add random tags to your search.

```
!problem -dp -*
PraccForces will respond with a problem including dp and other random tags.
```

### Slash commands are here !

Problem , contest and contests commands are now available in slash command format.

```
/problem rating:2000 tags:-dp

/contest division:3

/contests [optional:all]
```

### !Contest command Is 4x faster now!

```Example :
!contest 3
```

PraccForces will search for a contest with the supplied division (3 in this case ).

### !problem Command Reworked :

Praccforces now responds with a !problem commands 4x Faster than usual !
Make sure to try out the new optimized command !

Its now takes arguments as -tag and -rating.

Example :

```
!problem -dp -two pointers -2000
```

PraccForces will search for a problem with the tags "dp" and "two pointers" with ta rating of "2000" .

!problem command now tries to reply with a problem with the provided tags only, if there is no problem it will reply with a problem that includes said tags.

## PRACCFORCES BOT

Codeforces competitive coding Discord bot!

## Upcoming features :

<ul> <li> SERVER LEADERBORDS(Per server : all members) : solved problems</li> 
     <li> Member stats : solved problems , average difficulty , favorite tags</li></ul>

## Utilizes the whole Codeforces API to provide :

<ul>
  	<li> On demand problems from the entire Codeforces API. </li>
    <li> Problems with user specified tags and difficulty. </li>
 	<li> Alerts for upcoming contests. </li>
    <li> Old contests for training. </li>
 </ul>
 
 ## Commands List :

### Codeforces account link :

```
    !link help : Follow the steps to link you account!
```

    !link 'your codeforces handle' : links you account(follow the instructions)

### Problemset commands :

```
 	!Problem -'tag' -'difficulty'
```

    example : !problem -greedy -1200
    this command returns a random problem with greedy tag and 1200 difficulty.

    Alternative use : <br>

```
 !Problem '-difficulty' :
```

example : !problem -1200<br>
this command returns a random problem with random tag and 1200 difficulty.

```
    !Problem '-tag' :
```

example : !problem -greedy <br>
this command returns a random problem with greedy tag and random difficulty.

### Contests commands :

```
   !contests
```

this command will return the upcoming contests on CodeForces. <br>

### _ **NEW** _

```
    !contest 'Division'
```

example : !contest 2<br>
this command will return the list of problems of a random Division 2 contest.

### Leaderboards :

```
    !leaderboard : display global leaderboards ( still in testing )
```
