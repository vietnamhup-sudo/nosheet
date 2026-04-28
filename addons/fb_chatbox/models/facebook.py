from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from ..gemini import generate, send_facebook_message
import json
import uuid
from odoo.tools import html2plaintext
from ..fb_api import get_fb_page_info, get_fb_user_info


FB_LIVECHAT_CHANNEL = "Facebook"

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    file_data = fields.Binary(string="File data",attachment=True)

    type = fields.Selection(
        string="Product Type",
        help="Goods are tangible materials and merchandise you provide.\n"
             "A service is a non-material product you provide.",
        selection=[
            ('consu', "Goods"),
            ('service', "Service"),
            ('combo', "Combo"),
            ('download', "Download"),
        ],
        required=True,
        default='consu',
    )

class ImLivechatChannel(models.Model):
    _inherit = "im_livechat.channel"

    page_id = fields.Char("page_id")

class MailGuest(models.Model):
    _inherit = "mail.guest"

    sender_recipient_id = fields.Char("sender_recipient_id")

class DiscussChannel(models.Model):
    _inherit = "discuss.channel"

    chatbox = fields.Boolean("Chatbox?", default=False)
    sender_id = fields.Char("sender_id")
    page_id = fields.Char("page_id")

    def toggle_chatbox(self):
        for rec in self:
            rec.write({
                "chatbox": not rec.chatbox
            })

class MailMessage(models.Model):
    _inherit = "mail.message"
    _unique_queue_uuid = models.Constraint(
        'UNIQUE(queue_uuid)', 
        'This queue_uuid is already registered!'
    )

    queue_uuid = fields.Char(
        string="Queue uuid",
    )

    @api.model_create_multi
    def create(self, vals_list):
        result =  super(MailMessage, self).create(vals_list)

        chatbox = self.env.context.get("chatbox", False)
        for record in result:
            channel = self.env["discuss.channel"].browse(record.res_id)
            if record.model != "discuss.channel" or record.message_type != "comment":
                continue
            if not channel.sender_id:
                continue
            if record.author_id and channel.sender_id and not chatbox:
                if channel.chatbox:
                    channel.chatbox = False

                answer = html2plaintext(record.body or "")
                page_id = self.env["facebook.page"].search([("page_id", "=", channel.page_id)], limit=1)
                fb = self.env["facebook.mid"]
                fb.with_delay()._send_facebook_message(channel.sender_id, answer, page_id.access_token)

        return result

class GeiniApi(models.TransientModel):
    _name = 'facebook.gemini.api'
    _description = 'Gemini api'

    name = fields.Char(string='Name')
    api_key = fields.Char(string='API key')

class FacebookPage(models.TransientModel):
    _name = 'facebook.page'
    _description = 'Facebook Page'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name')
    is_active = fields.Boolean(string='Is Active?', default=True)
    page_id = fields.Char(string='Page ID')
    access_token = fields.Char(string='Access token')
    description = fields.Text(string='Description')
    system_instruction = fields.Text(string='System instruction', compute="get_system_instruction")
    prompt = fields.Html(string='Prompt', default="""
<p>Bạn là nhân viên bán quần áo trên Facebook.</p>

<p>Nhiệm vụ: trả lời tin nhắn khách hàng NGẮN GỌN, ĐÚNG TRỌNG TÂM, dễ hiểu.</p>

<p><strong>Quy tắc bắt buộc:</strong></p>
<ul>
    <li>Trả lời trực tiếp vào câu hỏi của khách (giá, size, màu, còn hàng…)</li>
    <li>Không giải thích dài dòng, không lan man</li>
    <li>Mỗi tin nhắn tối đa 2–4 câu</li>
    <li>Không tán gẫu, không nói chuyện ngoài lề</li>
    <li>Ưu tiên thông tin quan trọng trước</li>
</ul>

<p><strong>Cách trả lời:</strong></p>
<ul>
    <li>Ngắn nhưng đủ ý</li>
    <li>Tự nhiên như chat thật</li>
    <li>Có thể dùng 1–2 emoji nếu phù hợp</li>
</ul>

<p><strong>Gợi ý thêm (chỉ khi hợp lý):</strong></p>
<ul>
    <li>Gợi ý size / mẫu phù hợp</li>
    <li>Nhắc nhẹ nếu sản phẩm đang hot hoặc sắp hết</li>
</ul>

<p><strong>Không được:</strong></p>
<ul>
    <li>Viết dài dòng</li>
    <li>Viết kiểu tư vấn chung chung</li>
    <li>Lặp lại thông tin không cần thiết</li>
</ul>
""")

    user_ids = fields.Many2many(
        "res.users", 
        string='Users',
        domain=[("login", "!=", "admin")]
    )

    product_ids = fields.Many2many(
        "product.template",
        string='Products',
        domain=[("sale_ok", "=", True)]
    )

    def get_system_instruction(self):
        for record in self:
            text = f"{record.prompt}\n"
            text += "Sau đây là những mặt hàng bạn có thể tham khảo, để hỗ trợ người hỏi, khi được hỏi đến, hoặc chủ động giới thiệu đến họ nếu cảm thấy họ có nhu cầu:"
            for product in self.product_ids:
                text += f"""
    Tên sản phẩm: {product.name}
    Loại sản phẩm: {product.type}
    Mô tả: {product.description}
    Trạng thái có còn bán?: {'có' if product.is_published else 'Không'}
    Giá bán: {product.list_price} {product.currency_id.name}
    Được dán nhãn: {[tag.name for tag in product.product_tag_ids]}
    Được mô tả trên trang website: {product.description_ecommerce}
    Hạng mục sản phẩm: {[tag.name for tag in product.public_categ_ids]}
    Ribbon: {f'{product.website_ribbon_id.name} loại {product.website_ribbon_id.assign}'}
    --------------------
"""
            record.system_instruction = text

    def get_page_info(self):
        page_info = get_fb_page_info(self.access_token)
        if page_info:
            self.name = page_info.get("page_name", False)
            self.page_id = page_info.get("page_id", False)

    def write(self, vals):
        user_cmds = vals.get("user_ids")
        result = super(FacebookPage, self).write(vals)

        for record in self:
            if not user_cmds:
                continue

            livechat_channel = self.env["im_livechat.channel"].search([("page_id", "=", record.page_id)], limit=1)
            channel = self.env["discuss.channel"].search([("page_id", "=", record.page_id), ("livechat_end_dt", "=", False)], limit=1)
            if not livechat_channel:
                continue

            add_users = []
            remove_users = []
            for cmd in user_cmds:
                if cmd[0] == 4:
                    add_users.append(cmd[1])
                elif cmd[0] == 3:
                    remove_users.append(cmd[1])
            
            channel_partner_ids = [member.partner_id.id for member in channel.channel_member_ids if member.partner_id]

            for user in add_users:
                if user not in livechat_channel.user_ids.ids:
                    livechat_channel.user_ids = [(4, user)]

                user_id = self.env["res.users"].browse(user)
                if user_id.partner_id.id not in channel_partner_ids:
                    channel._add_members(users=user_id)

            for user in remove_users:
                if user in livechat_channel.user_ids.ids:
                    livechat_channel.user_ids = [(3, user)]

                user_id = self.env["res.users"].browse(user)
                if user_id.partner_id.id in channel_partner_ids:
                    channel._action_unfollow(partner=user_id.partner_id)

        return result

class FacebookMid(models.TransientModel):
    _name = 'facebook.mid'
    _description = 'Facebook mid'
    _unique_mid = models.Constraint(
        'UNIQUE(mid)', 
        'This mid is already registered!'
    )

    mid = fields.Char(string='Mid')

    def create_or_get_channel(self, sender_id, page_id=False, full_name="", avatar_1920=False):
        channel = self.env["discuss.channel"].search([("sender_id", "=", sender_id), ("livechat_end_dt", "=", False)], limit=1)
        if not channel and page_id:
            livechat_channel = self.get_livechat_channel(page_id)
            admin = self.get_admin()
            members = self.get_members(page_id)
            guest = self.get_guest(sender_id)
            page_guest = self.get_guest(page_id)
            channel = self.env['discuss.channel'].sudo().create({
                    "name": full_name + " - Facebook Page",
                    "sender_id": sender_id,
                    "page_id": page_id,
                    "chatbox": True,
                    "channel_type": "livechat",
                    "image_128": avatar_1920,
                    "livechat_channel_id": livechat_channel.id,
                    "livechat_operator_id": admin.partner_id.id,
                    # "channel_member_ids": [
                    #     Command.create({"partner_id": admin.partner_id.id}),
                    #     Command.create({"guest_id": guest.id}),
                    # ],
                })
            channel._add_members(users=admin)
            channel._add_members(guests=guest)
            for member in members:
                channel._add_members(users=member)
            if page_guest:
                channel._add_members(guests=page_guest)

        return channel

    def get_guest(self, sender_recipient_id, full_name="", avatar_1920=""):
        guest = self.env["mail.guest"].search([("sender_recipient_id", "=", sender_recipient_id)], limit=1)
        if sender_recipient_id and not guest and full_name:
            guest = self.env["mail.guest"].create({
                "name": full_name, 
                "sender_recipient_id": sender_recipient_id,
                "image_1920": avatar_1920
            })

        return guest

    def get_members(self, page_id):
        page = self.get_page(page_id)

        return page.user_ids

    def get_admin(self):
        return self.env['res.users'].search([("login", "=", "admin")], limit=1)
    
    def get_page(self, page_id):
        return self.env["facebook.page"].search([("page_id", "=", page_id)], limit=1)

    def get_livechat_channel(self, page_id):
        admin = self.get_admin()
        members = self.get_members(page_id)
        page = self.get_page(page_id)

        livechat_channel = self.env["im_livechat.channel"].search([("page_id", "=", page_id)], limit=1)
        if not livechat_channel:
            livechat_channel = self.env["im_livechat.channel"].sudo().create(
                {
                    "name": "FB Page: " + page.name,
                    "page_id": page_id, 
                    "user_ids": [admin.id] + members.ids
                }
            )

        return livechat_channel

    def run_gemini_api(self, sender_id, page_id, text, queue_uuid):
        channel = self.create_or_get_channel(sender_id)
        page = self.get_page(page_id)
        answer = generate(text, page.system_instruction)
        page_guest = self.get_guest(page_id)

        if channel.chatbox:
            message_id = channel.with_context(chatbox=True, guest=page_guest).message_post(
                body=answer,
                author_guest_id=page_guest.id,
                message_type="comment",
                subtype_xmlid="mail.mt_comment",
            )
            message_id.queue_uuid = queue_uuid
        return answer

    def _send_facebook_message(self, sender_id, answer, access_token):
        if sender_id and access_token:
            return send_facebook_message(sender_id, answer, access_token)

    def _send_facebook_message_by_queue_uuid(self, sender_id, queue_uuid, access_token):
        message_id = self.env["mail.message"].search([("queue_uuid", "=", queue_uuid)], limit=1)
        if message_id:
            answer = html2plaintext(message_id.body or "")
            if sender_id and access_token:
                return send_facebook_message(sender_id, answer, access_token)

    def send_as_guest(self, user_info, page_info, text, access_token):
        sender_id = user_info.get("sender_id")
        full_name = user_info.get("full_name")
        avatar_1920 = user_info.get("avatar_1920")

        page_id = page_info.get("page_id")
        page_name = page_info.get("page_name")
        page_avatar_1920 = page_info.get("avatar_1920")

        guest = self.get_guest(sender_id, full_name, avatar_1920)
        self.get_guest(page_id, page_name + " Bot", page_avatar_1920)
        channel = self.create_or_get_channel(sender_id, page_id, full_name, avatar_1920)

        channel.with_context(guest=guest).message_post(
            body=text,
            author_guest_id=guest.id,
            message_type="comment",
            subtype_xmlid="mail.mt_comment",
        )

        queue_uuid = f"uuid_{uuid.uuid4().hex}"
        if not channel.chatbox:
            return

        job = self.delayable().run_gemini_api(sender_id, page_id, text, queue_uuid)
        job2 = self.delayable()._send_facebook_message_by_queue_uuid(sender_id, queue_uuid, access_token)
        job.on_done(job2).delay()
