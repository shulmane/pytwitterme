pytwitterme
===========

my inspiration came from Joey, saying to me that twitter uses Redis :)

Design:
    Simple as it can be:
        Server.py  responsible for communication
        pytwitterme/facade.py is in charge for data processing

Data Structure:
    Redis API is core of the data store.
    Currently there is no need for real Redis server, so fakeredis (python module, in memory) is used

Scheme:
    every user is mapped to id ( u:%name%:id )
    all user ids are saved at "g:users"

New User/Post
    to create new user global counter "g:nextUserId" is used
    to create new post global counter "g:nextPostId" is used
    every post is saved by its id,
    global feed is saved at g:timeline
    feeds contains only ids of posts.
Follow /Unfollow:
    every user has map to followed /following users( followed currently not in use)
    on GetFeed we fetch the list of posts by followed users  ( already  exists)
    after that the list of posts is fetched

Known issues:
    There are a lot. Ask me, I tried to keep the implementation small and simple.


You can use this as test input for client.py (reset server first":

GET GetGlobalFeed
GET CreateUser?UserName="CoolTweeterUser"
GET PostMessage?UserId=1&MessageText="Hello"
GET PostMessage?UserId=1&MessageText="I+am+tweeeting"
GET PostMessage?UserId=1&MessageText="I+like+to+tweet"
GET PostMessage?UserId=1&MessageText="I+really+like+to+tweet"
GET GetGlobalFeed
GET GetFeed?ForUserId=1
GET CreateUser?UserName="TweeterFollower"
GET PostMessage?UserId=2&MessageText="I+will+follow+CoolTweeterUser!"
GET GetFeed?ForUserId=1
GET GetFeed?ForUserId=2
GET Follow?FollowingUser=2&FollowedUser=1
GET GetFeed?ForUserId=2
GET PostMessage?UserId=1&MessageText="I+am+famous!"
GET PostMessage?UserId=1&MessageText="Hello+My+followers!I+am+famous!"
GET GetGlobalFeed
GET GetFeed?ForUserId=1
GET GetFeed?ForUserId=2
GET PostMessage?UserId=2&MessageText="enought+of+CoolTweeterUser,+Unfollow!"
GET GetFeed?ForUserId=1
GET GetFeed?ForUserId=2
GET Unfollow?FollwingUser=2&UnfollowedUser=1
GET PostMessage?UserId=1&MessageText="No+body+is+reading+it.."
GET GetFeed?ForUserId=1
GET GetFeed?ForUserId=2
