FROM odoo:19

USER root

RUN pip3 install --no-cache-dir \
    --break-system-packages \
    --ignore-installed \
    google-genai

USER odoo