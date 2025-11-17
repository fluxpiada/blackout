
# publishing workflow 
## building in pandoc
⚠️ put older versions of epub > versions!

```
mv build/Blackout_Weak_Signals.epub versions/Blackout_Weak_Signals_OLDERVERSION.epub

pandoc content/manuscript/*.md \
  --resource-path="manuscript:images" \
  --epub-cover-image=content/images/cover.png \
  --epub-metadata=content/epub-metadata.xml \
  --toc \
  -o build/Blackout_Weak_Signals_LATEST.epub
```
H2 DEPRECATED 👇

```
mv build/Blackout_Weak_Signals.epub versions/Blackout_Weak_Signals_OLDERVERSION.epub

pandoc manuscript/*.md \
  --resource-path="manuscript:images" \
  --epub-cover-image=images/cover.png \
  --epub-metadata=epub-metadata.xml \
  --toc \
  -o build/Blackout_Weak_Signals.epub
```
## add it to repo with git

⚠️ replace version number MM.DD with month and date! 

``` git add Blackout_Weak_Signals.epub
git commit -m "Publish v1.MM.DD"
git tag -a v1.MM.DD-m "Release v1.MM.DD"
```
* Then push to latest release NOTE VERSION NUMBER!! Each tag = one archived version.
```
git push origin HEAD
git push origin v1.MM.DD 
```
* Then go to releases page to add the epub binary.
* Attach The Blackout Weak Signals v1.0.epub to the GitHub Release created automatically. 
