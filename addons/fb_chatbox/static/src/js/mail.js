/** @odoo-module **/

import { registerThreadAction } from "@mail/core/common/thread_actions";
import { _t } from "@web/core/l10n/translation";

registerThreadAction("gemini-test", {
  condition: ({ thread }) => thread?.channel_type === "livechat",
  icon: ({ thread, store }) => {
    return thread.chatbox
      ? "fa fa-magic text-success"
      : "fa fa-magic text-muted";
  },
  name: _t("AI Reply"),

  open: async ({ thread, store }) => {
    console.log("CLICK AI", thread.model, thread.id, thread.chatbox, thread);

    // await store.env.services.orm.call("discuss.channel", "run_gemini_api", [
    //   [thread.id],
    //   "test từ UI",
    // ]);

    await store.env.services.orm.call("discuss.channel", "toggle_chatbox", [
      [thread.id],
    ]);
  },

  sequence: 1,
});
