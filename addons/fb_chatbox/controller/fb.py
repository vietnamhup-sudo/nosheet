from odoo import http
from odoo.http import request
import json
from ..fb_api import get_fb_page_info, get_fb_user_info


class FacebookWebhookController(http.Controller):

    VERIFY_TOKEN = "my_verify_token_123"  # bạn tự đặt

    # =========================
    # 1. VERIFY WEBHOOK (GET)
    # =========================
    @http.route('/facebook/webhook', type='http', auth='public', methods=['GET'], csrf=False)
    def verify_webhook(self, **kwargs):

        mode = request.params.get('hub.mode')
        token = request.params.get('hub.verify_token')
        challenge = request.params.get('hub.challenge')

        request.env['ir.logging'].sudo().create({
            'name': 'facebook_webhook',
            'type': 'server',
            'dbname': request.env.cr.dbname,
            'level': 'INFO',
            'message': f'User sent message, {mode}, {token}, {challenge}',
            'path': 'facebook.webhook',
            'func': 'receive_message',
            'line': '0',
        })
        # Facebook gọi verify
        if mode == 'subscribe' and token == self.VERIFY_TOKEN:
            return challenge  # QUAN TRỌNG NHẤT

        return request.make_response("Verification failed", status=403)

    @http.route('/facebook/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_message(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data.decode())

            for entry in data.get("entry", []):
                for messaging in entry.get("messaging", []):

                    sender_id = messaging.get("sender", {}).get("id")
                    page_id = messaging.get("recipient", {}).get("id")
                    mid = messaging.get("message", {}).get("mid")
                    text = messaging.get("message", {}).get("text")
                    fb_page = request.env['facebook.page'].sudo().search([("page_id", "=", page_id), ("is_active", "=", True)], limit=1)
                    
                    request.env['ir.logging'].sudo().create({
                        'name': 'fb_callback',
                        'type': 'server',
                        'dbname': request.env.cr.dbname,
                        'level': 'INFO',
                        'message': f'code={fb_page}: {messaging}',
                        'path': 'facebook.callback',
                        'func': 'callback',
                        'line': '0',
                    })
                    if not fb_page:
                        continue

                    user_info = get_fb_user_info(sender_id, fb_page.access_token)
                    page_info = get_fb_page_info(fb_page.access_token)
                    if sender_id:
                        fb = request.env['facebook.mid'].sudo().create({"mid": mid})
                        fb.send_as_guest(user_info, page_info, text, fb_page.access_token)
        except Exception as e:
            request.env['ir.logging'].sudo().create({
                'name': 'fb_callback',
                'type': 'server',
                'dbname': request.env.cr.dbname,
                'level': 'INFO',
                'message': f'code={e}, error=',
                'path': 'facebook.callback',
                'func': 'Error callback',
                'line': '0',
            })
        return request.make_response("ok", status=200)

    @http.route('/facebook/callback', type='http', auth='public', csrf=False)
    def facebook_callback(self, **kwargs):
        code = request.params.get('code')
        error = request.params.get('error')
        print("cool!!!222")

        # Log lại để debug
        request.env['ir.logging'].sudo().create({
            'name': 'fb_callback',
            'type': 'server',
            'dbname': request.env.cr.dbname,
            'level': 'INFO',
            'message': f'code={code}, error={error}',
            'path': 'facebook.callback',
            'func': 'facebook_callback',
            'line': '0',
        })
