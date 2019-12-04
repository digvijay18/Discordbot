How to use bot?

1. Bot can be used using 2 type of commands-
    a. !google <keywords>
    b. !recent <keyword>

2. For multi-word keywords, join the words using "_" as pure spaces are not supported
by the library used. For eg - To search "game of thrones", use "game_of_thrones" as keyword.

3. Currently, Redis cache is unavailable for use as Heroku does not provide it for free.

4. There is no proper and complete Logging implemented.

5. All authentication secrets are included in the repo for the sake of completeness. On production, they should not be part of repo.
