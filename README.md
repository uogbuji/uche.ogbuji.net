uche.ogbuji.net
===============

Just my web site

=======
Uses:

 * [Nikola](http://getnikola.com/)
  * [used as a site](http://getnikola.com/creating-a-site-not-a-blog-with-nikola.html)
 * [Bootstrap 3](http://getbootstrap.com/)  <del>[Foundation 4](http://foundation.zurb.com/)</del>

More details:

Customized with <del>bootstrap3-jinja theme and</del> [simplex via Bootswatch](http://bootswatch.com/simplex/)

    pip install requests
    nikola bootswatch_theme -n simplex -s simplex # -p bootstrap3-jinja #Then change from THEME = "bootstrap3" to THEME = "simplex"

To deploy:

	rsync -avz output/ ../uogbuji.github.com/

