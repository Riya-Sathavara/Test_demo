# -*- coding: utf-8 -*-
# Copyright (C) iCreative Technologies.
{
    'name': 'Smeets website',
    'version': '1.0',  
    'summary': 'Smeets Trading Theme',
    'description': """
Smeets Trading Theme
====================
        """,
    'author': 'iCreative Technologies',
    'category': 'Website',
    'depends': ['website','website_crm'],
    'installable': True,
    'data': [
            'views/template.xml',
            'views/web_contactus.xml',
            'views/web_aboutus.xml',
#         'views/website_product.xml',
#         'views/website_news.xml',
#         'views/website_contactus.xml',
#         'views/website_blog_view.xml',
#         'views/website_blog.xml',
#         'views/debranding.xml',
#         'views/website_about.xml',
    ],
    'application': True,
}
