import os, shutil

module_name = 'itricksme'
def xoa_nhieu_thu_muc(danh_sach_thu_muc):
    for ten_thu_muc in danh_sach_thu_muc:
        try:
            for root, dirs, files in os.walk(ten_thu_muc, topdown=False):
                for file in files:
                    duong_dan_file = os.path.join(root, file)
                    os.remove(duong_dan_file)
                    print(f'File "{duong_dan_file}" đã được xóa.')
                os.rmdir(root)
                print(f'Thư mục "{root}" đã được xóa.')
            print(f'Thư mục "{ten_thu_muc}" đã được xóa thành công.')
        except FileNotFoundError:
            print(f'Thư mục "{ten_thu_muc}" không tồn tại.')

danh_sach_thu_muc_can_xoa = [module_name,module_name+'.zip']
# Gọi hàm để xóa nhiều thư mục
xoa_nhieu_thu_muc(danh_sach_thu_muc_can_xoa)


def tao_thu_muc_va_file(list_tm, new_model, new_class):
    # Tạo thư mục
    os.makedirs(module_name)
    init = os.path.join(os.getcwd(),module_name, '__init__.py')
    manifest = os.path.join(os.getcwd(),module_name, '__manifest__.py')
    with open(init, 'w') as file:
        file.write('# -*- coding: utf-8 -*-\nfrom . import controller, models')
    with open(manifest, 'w') as file:
        file.write(f"""# -*- coding: utf-8 -*-
{{
    'name': 'Itricks Me',
    'version': '1',
    'category': 'sale',
    'live_test_url': '#',
    'summary': 'Phần mềm quản lý',
    'author': 'Lv Quy',
    'company': 'Itricks',
    'website': 'https://#',
    'depends': ['base_setup',],
    'data': [
    #data
        'data/cronjob.xml',
        'data/sequence.xml',
        # security
        'security/groups.xml',
        'security/ir.model.access.csv',
        # report
        'report/menu.xml',
        'report/report.xml',
        # views
        'views/{new_model.replace('.','_')}.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
}}
        """)


    for tm in list_tm:
        path_dir = os.path.join(module_name, tm)
        os.makedirs(path_dir)
        if tm in ['controllers']:
            init = os.path.join(module_name,tm, '__init__.py')
            main = os.path.join(module_name,tm, 'main.py')

            with open(init, 'w') as file:
                file.write('# -*- coding: utf-8 -*-\nfrom . import main')
            with open(main, 'w') as file:
                file.write(f"""# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request\n\n\n
class {new_class}(http.Controller):\n
    @http.route(['/team'], auth='public', website=True)
    def team(self, **kw):
        return request.render('{module_name}.team')
""")
        if tm in ['models']:
            init = os.path.join(module_name,tm, '__init__.py')
            model = os.path.join(module_name,tm, new_model.replace('.', '_') + '.py')
            with open(init, 'w') as file:
                file.write(f"""# -*- coding: utf-8 -*-\nfrom . import {new_model.replace('.', '_')}""")
            with open(model, 'w') as file:
                file.write(f"""# -*- coding: utf-8 -*-\n
from odoo import fields, models, api
from datetime import date, datetime
from odoo.exceptions import UserError\n\n\n
class {new_class}(models.Model): \n
    _name = '{new_model}'
    _description = '{new_model}'
    _rec_name = 'name'
    _order = 'name desc'

    name = fields.Char(string='Name', required=True)
    ma_phieu = fields.Char(string='Mã phiếu',readonly=True, default=lambda self: 'New')
    _sql_constraints = [
        ('name_unique',
         'unique(name)',
         'Đã tồn tại tên này!')
    ]
    
    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New' == 'New'):
            vals['ma_phieu'] = self.env['ir.sequence'].next_by_code('maphieu.code') or 'New'
            res = super({new_class}, self).create(vals)
        return res
""")
        if tm in ['data']:
            cronjob = os.path.join(module_name,tm, 'cronjob.xml')
            sequence = os.path.join(module_name,tm, 'sequence.xml')
            with open(cronjob, 'w') as file:
                file.write(
                    f"""<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="check_overdue_sale" model="ir.cron">
            <field name="name">Check quán hạn thanh toán sale</field>
            <field name="model_id" ref="model_{new_model.replace('.', '_')}"/>
            <field name="state">code</field>
            <field name="code">model._check_overdue()</field>
            <field name="interval_number">1</field>
            <field name="interval_type">days</field>
            <field name="numbercall">-1</field>
            <field name="active" eval="True"/>
            <field name="doall" eval="True"/>
        </record>
    </data>
</odoo>
""")
            with open(sequence, 'w') as file:
                file.write("""<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="seq_maphieu" model="ir.sequence">
        <field name="name">Mã phiếu ứng lương</field>
        <field name="code">maphieu.code</field>
        <field name="prefix">No%(y)s%(month)s-</field>
        <field name="padding">3</field>
        <field name="company_id" eval="True"/>
        </record>
    </data>
</odoo>
""")
        if tm in ['report']:
            report = os.path.join(module_name,tm, 'report.xml')
            menu = os.path.join(module_name,tm, 'menu.xml')
            with open(menu, 'w') as file:
                file.write(f"""<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="action_report_{new_model.replace('.', '_')}" model="ir.actions.report">
            <field name="name">{new_model}</field>
            <field name="model">{new_model}</field>
            <field name="report_type">qweb-pdf</field>
            <field name="report_name">{module_name}.report_{new_model.replace('.', '_')}_action</field>
            <field name="report_file">{module_name}.report_{new_model.replace('.', '_')}_action</field>
            <field name="print_report_name">'%s' % (object.name)</field>
            <field name="binding_model_id" ref="model_{new_model.replace('.', '_')}"/>
            <field name="binding_type">report</field>
        </record>
    </data>
</odoo>
         """)
            with open(report, 'w') as file:
                file.write(f"""<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="report_{new_model.replace('.', '_')}">
        <t t-call="web.basic_layout">
            <t t-foreach="docs" t-as="doc">
                <h2 class="text-center text-success font-weight-bold">REPORT
                </h2>
                <p style="page-break-before:always;"></p>
            </t>
        </t>
    </template>
    
    <template id="report_{new_model.replace('.', '_')}_action">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="doc">
                <t t-call="{module_name}.report_{new_model.replace('.', '_')}"/>
            </t>
        </t>
    </template>
</odoo>
    """)
        if tm in ['security']:
            group = os.path.join(module_name,tm, 'groups.xml')
            access = os.path.join(module_name,tm, 'ir.model.access.csv')
            with open(group, 'w') as file:
                file.write(f"""<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record model="ir.module.category" id="{new_model.replace('.', '_')}">
            <field name="name">{module_name}</field>
            <field name="description">{module_name} Group</field>
            <field name="sequence">30</field>
        </record>
        <record id="{module_name}.group_{new_model.replace('.', '_')}" model="res.groups">
            <field name="name">Truy cập {module_name}</field>
            <field name="category_id" ref="{module_name}.{new_model.replace('.', '_')}"/>
        </record>
    </data>
</odoo>
                """)
            with open(access, 'w') as file:
                file.write(f"""id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n
access_{new_model.replace('.', '_')}_user,{new_model}.user,model_{new_model.replace('.', '_')},base.group_user,1,1,1,1
access_{new_model.replace('.', '_')}_root,{new_model}.root,model_{new_model.replace('.', '_')},base.group_system,1,1,1,1
access_{new_model.replace('.', '_')}_custom_group,{new_model}.root,model_{new_model.replace('.', '_')},base.{new_model.replace('.', '_')},1,1,1,1
                """)
        if tm in ['static']:
            path_des = os.path.join(module_name,tm, 'description')
            path_src = os.path.join(module_name,tm, 'src')
            os.makedirs(path_des)
            os.makedirs(path_src)
        if tm in ['views']:
            view = os.path.join(module_name,tm, f"{new_model.replace('.', '_')}.xml")
            with open(view, 'w') as file:
                file.write(f"""<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="{new_model.replace('.','_')}_form" model="ir.ui.view">
            <field name="name">{new_model}.form</field>
            <field name="model">{new_model}</field>
            <field name="arch" type="xml">
                <form string="{new_class}">
                    <header>
                        <field name="state" widget="statusbar" statusbar_visible="0,1"/>
                    </header>
                    <sheet>
                        <div class="oe_title">
                            <h1>
                                <field name="name"/>
                            </h1>
                        </div>
                        <group>
                            <group>
                                <field name="state"/>
                            </group>
                            <group>
                                <field name="state"/>
                            </group>
                        </group>
                        <notebook>
                            <page name="nhanvien" string="{new_model.replace('.','_')}">
                                <field name="nhan_vien"/>
                            </page>
                        </notebook>
                        <span>Ghi chú:</span>
                        <field name="note"/>
                    </sheet>
                </form>
            </field>
        </record>
        
        <record id="{new_model.replace('.','_')}_tree" model="ir.ui.view">
            <field name="name">{new_model}.tree</field>
            <field name="model">{new_model}</field>
            <field name="arch" type="xml">
                <tree string="{new_class}" decoration-success="state == '1'">
                    <field name="name" optional="show"/>
                    <field name="note" optional="hide"/>
                    <field name="state" optional="show"/>
                </tree>
            </field>
        </record>
        
        <record id="action_view_{new_model.replace('.','_')}" model="ir.actions.act_window">
            <field name="name">{new_class}</field>
            <field name="res_model">{new_model}</field>
            <field name="view_mode">tree,form</field>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    Create a new ...
                </p>
            </field>
        </record>
        
        <menuitem id="menu_{new_model.replace('.','_')}" name="{new_class}" sequence="1"
                  web_icon="{module_name},static/img/icon.png"
                  groups="base.group_system,{module_name}.group_{new_model.replace('.','_')}"/>
        <menuitem id="menu_sub_{new_model.replace('.','_')}" name="{new_class}" parent="menu_{new_model.replace('.','_')}" action="action_view_{new_model.replace('.','_')}"
                  sequence="1" groups="base.group_system,{module_name}.group_{new_model.replace('.','_')}"/>
    </data>
</odoo>
""")


# Thay đổi các giá trị dưới đây theo ý của bạn
ten_thu_muc_moi = ["controllers", 'models', 'data', 'views', 'security', 'static', 'report']


tao_thu_muc_va_file(ten_thu_muc_moi, new_model='zalo.oa', new_class='ZaloOa')

pwd_module = os.path.join(os.getcwd(),module_name)
print(pwd_module)
zip_filename = f'{module_name}'
shutil.make_archive(zip_filename, 'zip', pwd_module)
