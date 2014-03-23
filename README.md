= uche.ogbuji.net

Just my web site

Stuff used:

 * [Nikola](http://getnikola.com/)
  * [docs](http://getnikola.com/documentation.html)
  * [used as a site](http://getnikola.com/creating-a-site-not-a-blog-with-nikola.html)
  * [jquery.cycle2](http://jquery.malsup.com/cycle2/)
 * [Bootstrap 3](http://getbootstrap.com/)  <del>[Foundation 4](http://foundation.zurb.com/)</del>

More details:

Customized with <del>bootstrap3-jinja theme and</del> [simplex via Bootswatch](http://bootswatch.com/simplex/)

    pip install requests
    nikola bootswatch_theme -n simplex -s simplex # -p bootstrap3-jinja #Then change from THEME = "bootstrap3" to THEME = "simplex"

To deploy:

	rsync -avz output/ ../uogbuji.github.com/

----

Note: 

Code in tools needs Python 2.x and Amara (pip install python-dateutil amara==2)

