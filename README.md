# youtube-url-corrector
A Python based Discord bot to redirect YouTube links to Piped.

Example `compose.yml`
```yml
version: '3'

services:
    bot:
      image: git.beans.team/em/yuc:latest
      environment:
        - DISCORD_TOKEN=your_discord_bot_token
        - PIPED_URL=https://your.piped.url/watch?v=
      restart: unless-stopped
```
