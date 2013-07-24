
from time import sleep, time
from redis.exceptions import ResponseError
import unittest
from datetime import datetime, timedelta

from facade import PyTwitterMeFacade
import fakeredis

import logging
import logging.config

# we should use logging-test.conf
logging.config.fileConfig('../logging.conf')

class TestFacade(unittest.TestCase):
    def setUp(self):
        self.facade =  PyTwitterMeFacade()

    def tearDown(self):
        #clean db after each test
         self.facade.redis.flushdb()

    def test_createUser(self):
        id = self.facade.createUser("user")
        self.assertEqual( id , self.facade.getUserId("user"))



    def test_initial(self):
        self.__assertSameFeed( [], self.facade.getGlobalFeed() )


    def test_simplePost(self):
        user = "user"
        userId = self.facade.createUser(user)
        testMessage = "TestMessage"
        self.facade.postMessage(userId, testMessage)

        userFeed = self.facade.getFeed(userId)
        global_feed = self.facade.getGlobalFeed()
        self.__assertSameFeed([testMessage ], userFeed )
        self.assertEqual(global_feed ,userFeed)


    def test_simpleFollowUnfollow(self):
        testMessage = "TestMessage"
        testMessage2 = "TestMessage2"
        testMessage3 = "TestMessage3"
        famousUserId = self.facade.createUser("famousUser")
        self.facade.postMessage(famousUserId, testMessage)

        userFeed = self.facade.getFeed(famousUserId)
        self.__assertSameFeed([testMessage ], userFeed )

        simpleUserID = self.facade.createUser("simpleUser")

        self.facade.follow(simpleUserID, famousUserId )

        self.__assertSameFeed([ ], self.facade.getFeed(simpleUserID) )
        self.facade.postMessage(famousUserId, testMessage2)
        self.__assertSameFeed([ testMessage2], self.facade.getFeed(simpleUserID) )

        self.facade.unfollow(simpleUserID, famousUserId )
        self.facade.postMessage(famousUserId, testMessage3)

        self.__assertSameFeed([ testMessage2], self.facade.getFeed(simpleUserID) )

    def __assertSameFeed(self, expected , actual):
        self.assertEquals( [ x.split("|")[2] for x in actual ], expected)


if __name__ == '__main__':
    unittest.main()

