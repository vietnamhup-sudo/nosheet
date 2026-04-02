/** @odoo-module **/

import { Component, xml, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { router } from "@web/core/browser/router";
import { user } from "@web/core/user";

export class Build extends Component {
  setup() {
    this.isDebug = Boolean(odoo.debug);
    this.state = useState({ isNoSheetAdmin: false });

    onWillStart(async () => {
      this.state.isNoSheetAdmin = await user.hasGroup("base.group_system");
    });
  }
  async onClickBuild() {
    await this.env.services.action.doAction("nosheet.action_nosheet_build");
  }

  async onClickGoModel() {
    const currentAction = this.env.services.action.currentController?.action;

    const resModel = currentAction?.res_model;

    const orm = this.env.services.orm;

    const result = await orm.searchRead(
      "ir.model",
      [["model", "=", resModel]],
      ["id"],
    );

    const modelId = result?.[0]?.id;

    if (modelId) {
      await this.env.services.action.doAction({
        type: "ir.actions.act_window",
        res_model: "ir.model",
        res_id: modelId,
        views: [[false, "form"]],
      });
    }
  }

  async onClickBug() {
    let debug = this.isDebug ? 0 : "assets";
    router.pushState({ debug: debug }, { reload: true });
  }
}

Build.template = xml`
<div class="d-flex flex-row" t-if="state.isNoSheetAdmin">
  <button class="btn text-white d-flex align-items-center justify-content-center"
      t-on-click="onClickBug"
      title="Bug"
      t-if="!isDebug"
  >
      <i class="fa fa-lock"/>
  </button>

  <button class="btn text-white d-flex align-items-center"
      t-on-click="onClickGoModel"
      t-if="isDebug"
  >
      <i class="fa fa-folder-open"/>
  </button>

    <button class="btn text-white d-flex align-items-center gap-1"
        t-on-click="onClickBuild"
        t-if="isDebug"
    >
        <i class="fa fa-cogs"/>
        <span>Build</span>
    </button>

</div>
`;

registry.category("systray").add("build_systray", {
  Component: Build,
  sequence: 10,
});
