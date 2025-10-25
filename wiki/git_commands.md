# Git hub commands
## from your local clone
```
git checkout main
git pull
```
* create a new commit that undoes commitname
```
git revert <<SHA>>
```
* if it opens an editor, save & close; resolve any conflicts if prompted
```
git push
```
* That will reinstate the state from c1c873c2… by applying the inverse of the bad commit, preserving history.

