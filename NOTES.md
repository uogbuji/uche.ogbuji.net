
After update:

```
#sh sync.sh #No longer needed
#ssh g
source $HOME/.local/venv/main/bin/activate
cd ~/dev/uche.ogbuji.net
pip install -U nikola jinja2
nikola build
# Test locally using `nikola serve`
rsync -avz output/* uogbuji.github.com/ #Presuming deployment repo has been cloned to subdir
```

nikola serve     #Start the test server. Site will be at http://127.0.0.1:8000


# Stuff to try

* https://github.com/adrienverge/PhotoCollage
* https://collagerator.en.softonic.com/mac

Look up Responsive Page Scrolling themes for Bootstrap

## Image carousels & such

* [ekko Lightbox for Bootstrap](http://ashleydw.github.io/lightbox/#image-gallery)
* https://tympanus.net/codrops/2011/09/20/responsive-image-gallery/

##Stuff once used

* http://jquery.malsup.com/cycle2/demo/non-image.php

