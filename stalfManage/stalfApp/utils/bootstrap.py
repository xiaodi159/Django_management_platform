from django import forms

class BootstrapForm(forms.ModelForm):
    # 在此处填写不需要添加样式的label
    bootstrap_exclude_filelds = ['img']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #循环ModelForm中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_filelds:
                continue
            #字段中有属性，保留原来的属性，才增加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }


