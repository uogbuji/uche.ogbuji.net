uche.ogbuji.net
===============

Just my web site

=======
Uses:

 * [Nikola](http://getnikola.com/)
  * [used as a site](http://getnikola.com/creating-a-site-not-a-blog-with-nikola.html)
 * [Bootstrap 3](http://getbootstrap.com/)  <del>[Foundation 4](http://foundation.zurb.com/)</del>

More details:

Customized with bootstrap3-jinja theme and [simplex via Bootswatch](http://bootswatch.com/simplex/)

    pip install requests
    nikola install_theme base-jinja #For some reason need to install the parent chain manually
    nikola install_theme bootstrap-jinja
    nikola install_theme bootstrap3-jinja
    nikola bootswatch_theme -s simplex -p bootstrap3-jinja #Then change from THEME = "bootstrap3" to THEME = "custom"
