/** @odoo-module **/
import { Component, xml, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { CharField } from "@web/views/fields/char/char_field";

export class EncryptField extends CharField {
  setup() {
    super.setup();
    this.state = useState({
      key: null,
      display: "",
      isLocked: false,
      isListView: false,
      isEditAble: false,
    });
    onWillStart(async () => {
      const value = this.props.record.data[this.props.name];
      const key = await this.env.services.crypto.getKey();
      if (key && value) {
        this.state.key = key;
        const text = await this.env.services.crypto.decrypt(value, key);
        if (text) {
          this.unlock(text);
        } else {
          this.lock();
        }
      } else if (value) this.lock();

      this.state.isListView = this.env.config.viewType == "list";
      this.state.isEditAble = this.env.config.rawArch.includes("editable");
    });
  }

  async createKey(password = false) {
    if (!password) return false;
    const key = await this.env.services.crypto.deriveKey(password);
    return key;
  }
  async setKey(key = false) {
    if (!key) return false;
    await this.env.services.crypto.setKey(key);
    this.state.key = key;
    return true;
  }

  lock() {
    this.state.isLocked = true;
    this.state.display = "*****";
  }

  unlock(text) {
    this.state.isLocked = false;
    this.state.display = text;
  }

  async onChange(event) {
    try {
      const text = event.target.value;
      if (!text) {
        this.props.record.update({
          [this.props.name]: "",
        });
        this.unlock("");
        return;
      }

      if (!this.state.key) {
        this.env.services.notification.add(
          "Thiếu key, trường encrypt không lưu thành công!",
          {
            type: "danger",
          },
        );
        return;
      }

      const oldValue = this.props.record.data[this.props.name];
      if (oldValue) {
        const oldText = await this.env.services.crypto.decrypt(
          oldValue,
          this.state.key,
        );
        if (!oldText) {
          this.env.services.notification.add(
            "Sai key, trường encrypt không lưu thành công!",
            {
              type: "danger",
            },
          );
          return;
        }
      }

      const value = await this.env.services.crypto.encrypt(
        text,
        this.state.key,
      );

      if (value) {
        this.props.record.update({
          [this.props.name]: value,
        });
        this.unlock(text);
      }
    } catch (error) {
      console.log("error", error);
    }
  }

  async openAskPasswordModel(onClose = async () => {}) {
    await this.env.services.action.doAction("nosheet.action_nosheet_password", {
      onClose: onClose,
    });
  }
  async openPassword() {
    const value = this.props.record.data[this.props.name];
    if (this.state.isLocked && value) {
      if (this.state.key) {
        const text = await this.env.services.crypto.decrypt(
          value,
          this.state.key,
        );
        if (text) {
          this.unlock(text);
          return;
        }
      }
      await this.openAskPasswordModel(async (result) => {
        if (!result) return;
        const password = result.value;
        const key = await this.createKey(password);
        if (!key) return;
        const text = await this.env.services.crypto.decrypt(value, key);
        if (text) {
          this.unlock(text);
          await this.setKey(key);
        }
      });
    } else if (!this.state.isLocked && value) {
      this.lock();
      await this.env.services.crypto.clearKey();
      this.state.key = null;
    } else if (!this.state.isLocked && !value) {
      await this.openAskPasswordModel(async (result) => {
        if (!result) return;
        const password = result.value;
        const key = await this.createKey(password);
        if (!key) return;
        await this.setKey(key);
      });
    }
  }
}

EncryptField.template = xml`
  <div style="display:flex; align-items:center; gap:8px;"
    t-if="state.isListView"
  >
    <span 
        style="cursor:pointer; user-select: none;"
        t-on-click.stop="openPassword"
    >
        <t t-if="state.isLocked">🔒</t>
        <t t-else="">🔓</t>
    </span>
    <input 
        class="encrypt_list_input"
        type="text"
        t-att-value="state.display"
        t-on-change="onChange"
    />
  </div>

  <div style="display:flex; align-items:center; gap:8px;"
    t-if="!state.isListView"
  >
    <input 
      class="o_input"
      type="text"
      t-att-value="state.display"
      t-on-change="onChange"
    />
    <span 
        style="cursor:pointer; user-select: none;"
        t-on-click="openPassword"
    >
        <t t-if="state.isLocked">🔒</t>
        <t t-else="">🔓</t>
    </span>
  </div>
`;

registry.category("fields").add("encrypt_char", {
  component: EncryptField,
  supportedTypes: ["char"],
});
