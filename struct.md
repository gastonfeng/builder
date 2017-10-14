#架构
## models
###module.py
#### class Module(models.Model):
 >* description_html = fields.Html(string='Description HTML', sanitize=False)
##generators
###      v8.py
#### class GeneratorV8(models.TransientModel):
>* def generate_module(self, zip_file, module):
##utils
 ###jinja2.py
>#### def field_options(options):
 * @todo: 模块build,汉字输出\u格式
###zip.py
####class ZipFile(object):
 * def write_template(self, filename, template, d, **kwargs): ， 根据模版生成文件
 #### class ModuleZipFile(object):
 ##templates
 ###8.0
 ####models
 #####models.py.jinja2
  ####views
  #####[views.xml.jinja2]
#####actions.xml.jinja2
#####macros.jinja2
>        L268 ，         {%- if field.option_ids %} selection={{ field.option_ids|field_options }},{%- endif -%}
 >       macro builder_ir_ui_view(view)
 >       builder_views_form
 >       L370 , builder_views_tree
 >         @todo :builder,视图字段无顺序
>        builder_ir_actions_act_window
>          @todo: builder,action编辑,view_id与view_ids
>        builder_ir_model
>          @todo: builder,模型字段输出无顺序
