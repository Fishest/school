============================================================
Facebook Graph
============================================================

------------------------------------------------------------
Introduction
------------------------------------------------------------

The graph is rooted at three main endpoints:

* `/me` (if logged in and authorized)
* `/<facebook id>`
* `/<facebook name>`

These return the root json document of the user::

    {
      "id": "123456789",
      "name": "User Name",
      "first_name": "User",
      "last_name": "Name",
      "link": "https://www.facebook.com/user.name",
      "username": "user.name",
      "gender": "male",
      "locale": "en_US",
    }

The graph API can be played with by using the Graph Explorer
tool on the facebook site: `http://developers.facebook.com/tools/explorer`

------------------------------------------------------------
Login, Authorization, Permissions
------------------------------------------------------------

* Facebook Login

  In order to use the facebook graph, you first must login
  using the facebook login service. APIs are included for a
  number of frameworks (js, java, php).

* Authorization

  In order to use someone's data, a user must first allow you
  to granularly use their information. This requires server to
  server flow (if you are not using the supplied toolkits) to
  handle authorization callbacks.

* Permissions

  When asking for authorization, you granularlly ask for specific
  permissions that you need in order to achieve your task. For example:
  access to basic information, post on the users behalf, etc.
  
  It should be noted that even though you may ask for a permission,
  a user may or may not grant it and thus your application should
  be developed to deal with this situation.

* Access Token

  This is a token that is generated for the supplied permissions you
  have been offered. It must be included with every request in order
  to be processed. These expire and must be refreshed occasionally.
  There are also page tokens that allow access to a specific page and
  app tokens that allow access to a single applications data (analytics).

------------------------------------------------------------
Graph Connections
------------------------------------------------------------

In order to see the metadata connections available to a user,
simply use the endpoint `/me?metadata=1`::

    "metadata": {
      "connections": {
        "photos": "https://graph.facebook.com/me/photos",
        ...
       }
     }

Even though a connection is listed, it doesn't mean that any data
is neccessarily present in that node (it could just be an empty set).

When you find a new node, using its id you can query it as well as
the fields it is associated with::

    /<album-node-id>?fields=photots,likes

------------------------------------------------------------
Realtime Updates
------------------------------------------------------------

In order to receive realtime updates, you must host a public
callback server so that for each subscription createad, it
can be verified by facebook and then updates sent.

To verify each subscription, the following is sent as a GET
to your callback URL::

    hub.mode = "subscribe"
    hub.challenge = "a random string"
    hub.verify_token = "the subscription id just made"

The verify token should first be verified and if valid
just the challenge string should be echoed back to the
facebook server.

Next, all updates will be POSTed to your callback URL
as JSON documents containing one or more updates. It
should be noted that the updated values will not be
sent, just the nodes. In order to get the values, you
must query them with the graph api.

The updates are batched and sent every 5 seconds or when
the updates exceed 1000. The response is also validated
by including the SHA1 signature of the json in the
X-Hub-Signature HTTP Header.

------------------------------------------------------------
Field Expansion
------------------------------------------------------------

This is basically linq to the query fields, you can do things
like::

    https://graph.facebook.com/me?fields=name,birthday,photos.limit(10).fields(id, picture)
    https://graph.facebook.com/me?fields=name,birthday,videos.type(tagged).limit(10).fields(id, source)
    https://graph.facebook.com/me?fields=albums.limit(5).fields(name,photos.limit(2).fields(name, picture, tags.limit(2)))
    https://graph.facebook.com/<photo-id>/comments?fields=from.fields(id,
    https://graph.facebook.com/me/friends?limit=10&fields=news.reads.limit(2)

------------------------------------------------------------
Creating a Photo
------------------------------------------------------------

Simply issue a post request to the following URI with a valid
access token with publish_stream permission (this will be added
to a folder for your application id and one will be created if
it does not already exist)::

    @code           = @request['code']
    @app_id         = "YOUR APPLICATION ID"
    @app_secret     = "YOUR APPLICATION SECRET"
    @post_login_uri = "YOUR POST LOGIN URI"

    if (@code.empty()) {
      @login_url = "http://www.facebook.com/dialog/oauth?"
        + "client_id=#{app_id}&"
        + "redirect_uri=#{post_login_uri}&"
        + "scope=publish_stream"
      redirect(@login_url)
    }

    @token_url = "https://graph.facebook.com/oauth/access_token?"
      + "client_id=#{app_id}&"
      + "redirect_uri=#{@post_login_uri}&"
      + "client_secret=#{@app_secret}&"
      + "code=#{@code}"
    @token  = @params['access_token']
    @action = "https://graph.facebook.com/<user-id>/photos?access_token=#{@token}"

    // result is: { "id": "1001207389476" }
    <form enctype="multipart/form-data" action="#{@action}" method="POST">
      <input name="source" type="file" />
      <input name="message" type="text" value="" />
    </form>

Can supply a URL instead of the photo data to publish as well.
