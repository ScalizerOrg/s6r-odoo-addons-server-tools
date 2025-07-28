# Copyright 2025 Scalizer (<https://www.scalizer.fr>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models
from odoo.exceptions import UserError
import io
import base64
from PIL import Image
from pillow_heif import register_heif_opener
register_heif_opener()

import logging
_logger = logging.getLogger(__name__)

def convert_heic_file(datas, target_format='PNG'):
    try:
        heic_data = base64.b64decode(datas)
        image = Image.open(io.BytesIO(heic_data))

        if target_format.upper() == 'JPEG' and image.mode != 'RGB':
            image = image.convert('RGB')

        image_data = io.BytesIO()
        image.save(image_data, format=target_format, quality=95 if target_format.upper() == 'JPEG' else None)
        return base64.b64encode(image_data.getvalue()).decode('utf-8')

    except Exception as e:
        raise UserError(f"Error converting HEIC to {target_format}: {e}")


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            if vals.get('name', False):
                file_name, file_extension = vals.get('name', '').split('.')

                if file_extension.upper() == 'HEIC':
                    image_format = self.env.context.get('image_format', 'PNG')
                    target_format = 'JPEG' if image_format.upper() == 'JPG' else image_format

                    if vals.get('raw', False):
                        vals['datas'] = base64.b64encode(vals.get('raw', b''))
                        vals.pop('raw')

                    if vals.get('datas', False):               
                        try:
                            file_data = convert_heic_file(datas=vals.get('datas'),
                                                               target_format=target_format)
                            vals.update({                
                                'name': f'{file_name}.{image_format.lower()}',
                                'datas': file_data,
                                'mimetype':f'image/{image_format.lower()}',
                            })
                            
                        except Exception as err:
                            _logger.error(f"HEIC conversion to {image_format}: {err}")
                            
        return super(IrAttachment, self).create(vals_list)
