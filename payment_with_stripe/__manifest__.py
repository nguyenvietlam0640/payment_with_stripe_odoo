{
    'name': "payment_with_stripe",
	'name_vi_VN': "payment_with_stripe",
    'summary': """
Short (1 phrase/line) summary of the module's purpose, used as
subtitle on modules listing or apps.openerp.com""",
    'summary_vi_VN': """
Mô tả ngắn gọn bằng tiếng Việt (1 câu, 1 dòng) về mục đích của module
""",

    'description': """
What it does
============
Long description of module's purpose

Key Features
============
1. Feature 1

   * Sub-Feature 1
   * Sub-Feature 2

     * Sub-sub-feature 1
     * Sub-sub-feature 2

2. Feature 2

   * Sub-Feature 1
   * Sub-Feature 2

Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,
    'description_vi_VN': """
Ứng dụng này làm gì
===================
Mô tả chi tiết về module

Tính năng chính
===============
1. Tính năng 1

   * Tính năng Phụ 1
   * Tính năng Phụ 2

     * Tính năng Phụ Chi tiết 1
     * Tính năng Phụ Chi tiết 2

2. Tính năng 2

   * Tính năng Phụ 1
   * Tính năng Phụ 2

Ấn bản được Hỗ trợ
==================
1. Ấn bản Community
2. Ấn bản Enterprise

    """,

    'author': "Viindoo",
    'website': "https://viindoo.com",
    'live_test_url': "https://v15demo-int.erponline.vn",
    'live_test_url_vi_VN': "https://v15demo-vn.erponline.vn",
    'support': "apps.support@viindoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/Viindoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],
    

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/order_view.xml',
        'views/stripe_account_view.xml',
        'views/order_line_view.xml',
        'views/products_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': [
        'static/images.png'
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 99.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
