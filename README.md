# Eighty-Seven

I'm still on the hunt for a password manager that does everything I need:

* Securely store my passwords and let me access them from two computers. 

Vague enough to work, right? Let's flesh that out a bit more: 

* Free Software - I want to deploy my own (looking at you, lastpass)
* Must do encryption of password store *client* side (looking at you, locksmith)
* Multiple clients must be able to make non-conflicting changes that do not
    conflict, e.g. KeePassX + rsync will lose passwords if two copies get out of sync
* Browser integration, a desktop GUI, and a CLI (a.k.a. I want a pony)

The main stumbling block for me is that this is mostly solvable by technology
that I struggle with (JS and various GUI/TUI toolkits). The backend would be
need to be nothing more than a simple interface to a datastore.

Guess I need to suck it up and learn JS :P

## API

Everything changed, will document later
