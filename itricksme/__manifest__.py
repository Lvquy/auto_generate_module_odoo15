# -*- coding: utf-8 -*-
{
    'name': 'Itricks Me',
    'version': '1',
    'category': 'sale',
    'live_test_url': '#',
    'summary': 'Phần mềm quản lý',
    'author': 'Lv Quy',
    'company': 'Itricks',
    'website': 'https://#',
    'depends': ['base_setup',],
    'data': [
    #data
        'data/cronjob.xml',
        'data/sequence.xml',
        # security
        'security/groups.xml',
        'security/ir.model.access.csv',
        # report
        'report/menu.xml',
        'report/report.xml',
        # views
        'views/zalo_oa.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
}
        