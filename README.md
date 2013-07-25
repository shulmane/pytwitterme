pytwitterme
===========

You can use this as test input for client.py:

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
