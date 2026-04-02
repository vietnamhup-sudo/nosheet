{
    "name": "NoSheet",
    "version": "1.0",
    "author": "Hieu",
    "summary": "NoSheet",
    "depends": ["mail", "base_automation"],
    "data": [
        "security/role.xml",
        "security/ir.model.access.csv",
        "views/build.xml",
        "views/app.xml",
        "views/act_window.xml",
        "views/ir_ui_menu.xml",
        "views/ir_ui_view.xml",
        "views/ir_actions_server.xml",
        "views/res_groups.xml",
        "views/ir_model.xml",
        "views/menu.xml",
        # "views/header.xml",
    ],
    "application": True,
    "assets": {
        "web.assets_backend": [
            "nosheet/static/src/**",
        ],
    },
}
