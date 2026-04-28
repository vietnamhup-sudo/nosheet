/** @odoo-module **/
import { registry } from "@web/core/registry";

export const cryptoService = {
  start() {
    // cache key để tránh derive nhiều lần (optional nhưng nên có)
    let cachedKey = null;
    let cachedPassword = null;
    let key = null;

    return {
      setKey(value) {
        key = value;
      },

      getKey() {
        return key;
      },

      clearKey() {
        key = null;
      },

      async deriveKey(password, salt = "odoo_salt") {
        if (cachedKey && cachedPassword === password) {
          return cachedKey;
        }

        const enc = new TextEncoder();

        const keyMaterial = await crypto.subtle.importKey(
          "raw",
          enc.encode(password),
          "PBKDF2",
          false,
          ["deriveKey"],
        );

        cachedKey = await crypto.subtle.deriveKey(
          {
            name: "PBKDF2",
            salt: enc.encode(salt),
            iterations: 100000,
            hash: "SHA-256",
          },
          keyMaterial,
          { name: "AES-GCM", length: 256 },
          false,
          ["encrypt", "decrypt"],
        );

        cachedPassword = password;
        return cachedKey;
      },

      async encrypt(plainText, key) {
        if (!key) return false;
        try {
          const enc = new TextEncoder();
          const iv = crypto.getRandomValues(new Uint8Array(12));

          const cipherBuffer = await crypto.subtle.encrypt(
            { name: "AES-GCM", iv },
            key,
            enc.encode(plainText),
          );

          return btoa(
            JSON.stringify({
              iv: Array.from(iv),
              data: Array.from(new Uint8Array(cipherBuffer)),
            }),
          );
        } catch (error) {
          return false;
        }
      },

      async decrypt(cipherText, key) {
        if (!cipherText || !key) return false;

        try {
          const parsed = JSON.parse(atob(cipherText));

          const iv = new Uint8Array(parsed.iv);
          const data = new Uint8Array(parsed.data);

          const plainBuffer = await crypto.subtle.decrypt(
            { name: "AES-GCM", iv },
            key,
            data,
          );

          return new TextDecoder().decode(plainBuffer);
        } catch (e) {
          return false;
        }
      },
    };
  },
};

registry.category("services").add("crypto", cryptoService);
