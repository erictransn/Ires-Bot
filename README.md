# Ires-Bot

A discord bot for my own personal use and testing using the Discord api along with Discord.py to interact with users and discord.

Commands:
- !flip
  - inital basic command that returns head or tails
- !youtube
  - uses user input to search youtube and return the first video found from youtube and paste the link to the video in the channel in
    which the command was called in
- !karma
  - returns the user's score from upvotes and downvotes reactions

Events:
- on_member_join
  - Direct messages a member upon joining the discord server telling them to assign their roles
- on_raw_reaction_add
  - when a user uses a reaction, the bot checks if the reaction is an upvote or downvote to increment or decrement the author of the
    message score
  - Also assigned a role to the reactor when used on a message in the assign-role channel in the discord
- on_raw_reaction_remove
  - when a user uses a reaction, the bot checks if the reaction is an upvote or downvote to increment or decrement the author of the
    message score
  - Also remove a role to the reactor when used on a message in the assign-role channel in the discord
