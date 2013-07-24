
import fakeredis
from datetime import datetime
from logging import info

G_NEXT_POST_ID = "g:nextPostId"
G_NEXT_USER_ID = "g:nextUserId"
G_TIMELINE = "g:timeline"
G_USERS = "g:users"

POST_LIMIT_IN_FEED = 100

class PyTwitterMeFacade (object):

    def __init__(self):
        # we use simple dummy "in memory" redis client. not persisted. not..
        # for production : replace with client to real redis server
        self.redis = fakeredis.FakeStrictRedis()

    def getRedis(self):
        return self.redis

    def trimFeed(self, feedKey, maxSize=1000):
        self.getRedis().ltrim(feedKey,0,maxSize)

    def createUser(self, userName):
        r = self.getRedis()
        if r.get("u:%s:id"%userName):
            raise Exception( "Username is in use '%s'" %userName)

        currentUserId = r.incr(G_NEXT_USER_ID)
        r.set("u:%s:id" %userName,currentUserId)
        r.sadd(G_USERS,currentUserId)

        info("User %s with id %s has been created" % (userName, currentUserId))
        return currentUserId

    def getUserId(self, userName):
        r = self.getRedis()
        userId  =  r.get("u:%s:id"%userName)
        if not userId:
            raise Exception( "Username is not found  '%s'" %userName)
        return int(userId)



    def postMessage(self, userId, messageText):
        r = self.getRedis()
        currentPostId = r.incr(G_NEXT_POST_ID)
        message  = "%s|%s|%s"% ( userId, datetime.now(), messageText)

        r.set("post:%s" % currentPostId, message)

        followers = r.smembers("uid:%s:followers" % userId)
        if  not followers  :
            followers = set()
        followers.add( userId)

        for follower in followers :
            r.lpush("uid:%s:posts"%follower, currentPostId)

        # Push the post on the timeline, and trim the timeline to the
        # newest 1000 elements.
        r.lpush(G_TIMELINE, currentPostId)
        r.ltrim(G_TIMELINE,0,1000)
        pass




    def follow(self, followingUser, followedUser):
        r = self.getRedis()
        if followingUser == followedUser :
            raise Exception("User try to follow himself")
        r.sadd("uid:%s:followers" % followedUser,  followingUser)
        r.sadd("uid:%s:following" %followingUser,followedUser)




    def unfollow(self, followingUser, unfollowedUser):
        r = self.getRedis()
        if followingUser == unfollowedUser :
            raise Exception("User try to follow himself")
        r.srem("uid:%s:followers" % unfollowedUser,  followingUser)
        r.srem("uid:%s:following" %followingUser,unfollowedUser)





    def getFeed(self, userId, feedMaxSize=POST_LIMIT_IN_FEED):
        r = self.getRedis()
        posts = r.lrange(  "uid:%s:posts"%userId, 0 ,feedMaxSize)
        feed = []
        for post in posts:
            postData = self.getPost(post  )
            if  postData :
                # we can double check that user is still following owner of the post, but for now we keep it simple
                #  ( fetch following = r.smembers("uid:%s:following" % userId)
                # filter by returned ids.
                feed.append( postData )
        return feed


    def getGlobalFeed(self):
        r = self.getRedis()
        posts = r.lrange(  G_TIMELINE, 0 ,POST_LIMIT_IN_FEED)
        feed = []
        for post in posts:
            postData = self.getPost(post )
            if  postData :
                feed.append( postData )
        return feed



    def getPost(self, postId ):
        r = self.getRedis()

        post = r.get("post:%s"%postId)
        if not post:
            return None
        #
        # $aux = explode("|",$postdata);
        # $id = $aux[0];
        # $time = $aux[1];
        # username = r.get("uid:$id:username");
        # $post = join(array_splice($aux,2,count($aux)-2),"|");
        return post




