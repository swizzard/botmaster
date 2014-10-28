# BotMaster
Twitter bots are fun! They don't have to be hard.

## What IT Is
`botmaster` contains some helpers to make building Twitter bots easier.
It's really just some sugar built on top of the excellent
[Twitter](http://mike.verdone.ca/twitter/) library.

## What Is Up
`botmaster.py` contains four functions. The first two (with `auth`
in the name) are wrappers around `twitter.OAuth`. The latter two (with
`tweet` in the name) are decorators that turn regular functions into tweet bots.

(Before you ask, yes, I do feel a little bad for not splitting it into `auth.py`
  and `tweet.py`, but it's only 4 little functions.)

`_auth` is pretty simple--it takes four strings and gives you back an `OAuth` object

`env_auth` is a little more nuanced, but also more helpful. As the
name suggests, it creates an `OAuth` object from values stored as
environment variables. It takes strings, too, but the strings you
pass it are the names of the variables containing the relevant
credentials. It defaults to "access_token", "access_secret",
"api_key", and "api_secret", because those make sense to me.
(See below for more information on OAuth.)

`tweet` and `gen_tweet` do the real work. They're both decorators, but
they decorate different things. `tweet` takes a function that returns
a string; `gen_tweet` takes a [generator](https://wiki.python.org/moin/Generators).
The decorators both take the same arguments:
  * auth: a `twitter.OAuth` object, e.g. as returned by `_auth` or `env_auth` :wink:
    * defaults to `env_auth`
  * interval: the interval (in seconds) to wait between tweets.
    * defaults to `1800` (seconds, i.e., 30 minutes)

Behold:  

    # screambot.py
    from random import randint

    import botmaster

    my_auth = botmaster.env_auth("mytoken", "mysecret", "myapikey", "myapisecret")

    # use my_auth for authorization, tweet once every hour
    @botmaster.tweet(auth=my_auth, interval=3600)
    def screambot():
        return "{a}hhh!".format(a="a" * randint(1, 100))


    if __name__ == "__main__":
        screambot()


Congratulations! You've just made a Twitter bot that screams into the
empty void once an hour! It's a little too on-the-nose, but it's a good start.

## What Is What
There are two things you need before you can launch your little buddy
into the Twittersphere and start raking in the ~~big bucks~~ ~~world-wide acclaim~~ favs:
  * Get authenticated
  * Get hosted

### Authentication
This is not as easy as it used to be, because Twitter's locked down its App
auth process, requiring a cell phone number(!) for each app that wants
read/write access. This number has to be unique, so unless you're a character
on *The Wire*, you're basically limited to one read/write app. BUT!
It's not impossible. Check out [this blog post](http://dghubble.com/blog/posts/twitter-app-write-access-and-bots/),
and then `gem install twurl` and sign up for an app on [apps.twitter.com](https://apps.twitter.com).

NB: You need at least two accounts: your personal/"real" account, and your bot account.
Sign in with your real account to register your app (I call mine `swizzard_botmaster`,
because I'm almost *too* good at naming things.) Sign out, and then sign in with your
bot account before clicking on the link `twurl` will generate for you. This can get
a little confusing, but you'll figure it out.

### Hosting
I personally really like [Heroku](http://www.heroku.com) for hosting this kind of thing.
`env_auth` comes out of using their config system, which provides, IMHO, a really clean
and easy way of managing credentials without worrying about accidentally exposing sensitive
creds via an errant `git push`. If you go the Heroku route, I suggest running your bot as
a worker process, since you're not really *serving* anything (except wisdom/sick burns/flawless puns/divine madness/etc.)

However! There's nothing Heroku-specific about any of this stuff. Use `botmaster` to write
a bot and plop that bad boy on Dreamhost or an Apache server or a Raspberry Pi running your
own artisanal Haskell port of nginx. My feelings won't be hurt. Shoot, if you have a computer
you don't really care about, hook it up to the interwebs and cop a copy of Python and run your
automaton from the command-line! Go nuts!

## Etc.
PRs and such more than welcome! In particular, I'd really like help with two things:
  * Testing: There are no tests right now. This code is all based on stuff I've used
  [before](https://github.com/swizzard/sys_bot), and I tried it on the command line,
  so it *should* work. I'm just not sure how best to mock out the Twitter API.
  * Packaging: I'm planning to roll this bad boy into the [cheeseshop](https://pypi.python.org)
  sometime in the next few days. I've never packaged anything up before, and could use tips.

License: [WTFPL](http://www.wtfpl.net/), because it rules.
