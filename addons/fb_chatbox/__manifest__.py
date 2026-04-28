{
    "name": "Facebook Chatbox",
    "version": "1.0",
    "author": "Hieu",
    "summary": "Facebook Chatbox",
    "depends": ["mail", "im_livechat", "website_sale", "queue_job"],
    "data": [
        "security/ir.model.access.csv",
        "views/fb_page.xml",
        "views/groups.xml",
        "views/product_template.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "fb_chatbox/static/src/**",
        ],
    },
    "application": True,
}
