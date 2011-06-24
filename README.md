Serenity is an URL shortener with predictable and constant length URLs. It isn't designed to generate URLs as short as possible (in fact, generated URLs are pretty long), it's designed to give predictable URLs with a constant length. 

#### Why constant length? ####
Shortened URLs can be used as key_name for Google AppEngine entities or Memcache keys. 

#### Why predictable URLs? ####
The client can just issue a POST request and go back at doing what it was doing without waiting for a response, it doesn't even need one! 

#### So, is it just a reverse hash lookup for URLs? ####
Yes and no, it also follows redirects and store the final URL, thus reversing any shortened URL. 

#### That means that a POST request to add an URL is idempotent? What about collisions? ####
Uh, generated URLs are ugly because serenity is using SHA-1, collisions are possible but very rare. 

#### Why SHA-1? ####
A good compromise between performance and security. Easier than URLs to be sent over HTTP, no encoding is required. 
