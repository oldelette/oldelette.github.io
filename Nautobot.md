# Nautobot

nautobot github [link](https://github.com/nautobot/nautobot)


v2.0.1 - 2023-10-04

## Install Nautobot

### Poetry

```
pip install poetry
poetry new download_config

poetry shell
source /home/gavin/.cache/pypoetry/virtualenvs/download-config-ckh1PK7B-py3.8/bin/activate.fish
```


![Imgur](https://imgur.com/B2CJhrY.png)




* init 

```
poetry add nautobot
poetry install
```


[Nautobot Documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/administration/installation/nautobot/)


#### Initialize your configuration¶

```
nautobot-server init
```

改動 nautobot_config.py
需要指定 database 的帳號密碼

```python=
import os
import sys

from nautobot.core.settings import *  # noqa F401,F403
from nautobot.core.settings_funcs import is_truthy, parse_redis_connection

#########################
#                       #
#   Required settings   #
#                       #
#########################

# ALLOWED_HOSTS = os.getenv("NAUTOBOT_ALLOWED_HOSTS", "").split(" ")
ALLOWED_HOSTS = "*"

DATABASES = {
    "default": {
        "NAME": os.getenv("NAUTOBOT_DB_NAME", "nautobot"),  # Database name
        "USER": os.getenv("NAUTOBOT_DB_USER", "nautobot"),  # Database username
        "PASSWORD": os.getenv("NAUTOBOT_DB_PASSWORD", "decinablesprewad"),  # Database password
        "HOST": os.getenv("NAUTOBOT_DB_HOST", "127.0.0.1"),  # Database server
        "PORT": os.getenv("NAUTOBOT_DB_PORT", 3306),  # Database port (leave blank for default)
        "CONN_MAX_AGE": int(os.getenv("NAUTOBOT_DB_TIMEOUT", "300")),  # Database timeout
        "ENGINE": "django.db.backends.mysql",
        # "ENGINE": os.getenv(
        #     "NAUTOBOT_DB_ENGINE",
        #     "django_prometheus.db.backends.postgresql" if METRICS_ENABLED else "django.db.backends.postgresql",
        # ),  # Database driver ("mysql" or "postgresql")
    }
}

# Ensure proper Unicode handling for MySQL
#
if DATABASES["default"]["ENGINE"].endswith("mysql"):
    DATABASES["default"]["OPTIONS"] = {"charset": "utf8mb4"}

# This key is used for secure generation of random numbers and strings. It must never be exposed outside of this file.
# For optimal security, SECRET_KEY should be at least 50 characters in length and contain a mix of letters, numbers, and
# symbols. Nautobot will not run without this defined. For more information, see
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = os.getenv("NAUTOBOT_SECRET_KEY", "sth5owyc5%&70#yp41ysl6bb0_omkx(c3v0qkt9acsaj0ea$i4")

INSTALLATION_METRICS_ENABLED = is_truthy(os.getenv("NAUTOBOT_INSTALLATION_METRICS_ENABLED", "True"))

```


#### Prepare the Database



```
poetry add mysqlclient
```


假設安裝 mysqlclient 出錯 (如下圖), 執行下面指令

```
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
```


![Imgur](https://imgur.com/B7xunpb.png)



```
nautobot-server migrate
```

順利完成

![Imgur](https://imgur.com/s1ZPPAM.png)


#### Create a Superuser

建立帳號

```
nautobot-server createsuperuser
```


#### Test the Application

```
nautobot-server runserver 0.0.0.0:8080 --insecure
```

![Imgur](https://imgur.com/TF0l2iL.png)



### Docker Compose

下面為 mysql, adminer, redis 的相關 docker-compose 設定

```yaml=
version: '3.7'

services:
  redis:
    image: redis:7.0.5
    container_name: redis-nautobot
    ports:
      - 6379:6379
    volumes:
      - redis-data:/data
    networks:
      - nautobot_internal
    # network_mode: host  # Use host network mode

  mysql-server:
    image: mysql:8
    container_name: mysql-server
    env_file:
      - "local.env"
    ports:
      - 3306:3306
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - nautobot_internal
    # network_mode: host  # Use host network mode

  nautobot-adminer:
    image: adminer:latest
    container_name: nautobot-adminer
    environment:
      ADMINER_DEFAULT_SERVER: mysql-server
    command: [ "php", "-S", "0.0.0.0:8000", "-t", "/var/www/html" ]
    ports:
      - 28080:8000
    restart: always
    logging:
      driver: none
    networks:
      - nautobot_internal

volumes:
  redis-data: {}
  mysql-data: {}

networks:
  nautobot_internal:
     driver:  bridge
```





## Install Nautobot Plugin

[Plugin Development
](https://docs.nautobot.com/projects/core/en/v1.0.0/plugins/development/)[App Developer Guide - Nautobot Documentation](https://docs.nautobot.com/projects/core/en/stable/development/apps/api/setup/)
[Test-Repo](https://gitlab.com/oldelette1/nautobot-plugin)



### Plugin Structure

[Plugin Structure](https://docs.nautobot.com/projects/core/en/v1.4.7/plugins/development/#plugin-structure)

使用本文檔中描述的所有可用 plugin 功能的 Nautobot plugin 如下圖:


![Imgur](https://imgur.com/9VURBVO.png)


### Start


* pyproject.toml

```toml=
[tool.poetry]
name = "download-config"
version = "0.1.0"
description = ""
authors = ["oldelette <oldelette@gmail.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "3.8.10"


[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```





### Define a PluginConfig



PluginConfig class 是Nautobot 特定的 wrapper, wrapper 是 Django內建的 AppConfig class.
它用於在 Python wrapper中宣告 Nautobot plugin.
每個 plugin 都應該提供自己的子類，定義其名稱、元數據，以及默認和必需的配置參數


```python
__init__.py
from nautobot.extras.plugins import PluginConfig

class DownloadConfig(PluginConfig):
    name = 'download_config'
    verbose_name = 'Download Config'
    description = 'An example plugin for development purposes'
    version = '0.1'
    author = 'mcleezs'
    author_email = 'mcleezs@tsmc.com'
    base_url = 'download-config'
    required_settings = []
    min_version= '2.0.2'
    max_version= '2.0.4'

config = DownloadConfig
```

定義好後, 先執行 poetry install

![Imgur](https://imgur.com/T85eBPy.png)


再把這個 plugin 名稱加入 nautobot nautobot_config.py 檔案中後重啟 nautobot

Once the plugin has been installed, add it to the plugin configuration for Nautobot:
```
PLUGINS = ["nautobot_download_config"]
```


成功看到 plugin 欄位有我們的 plugin

![Imgur](https://imgur.com/jZmeorY.png)



#### How to add plugin

如何新增 opensource 別人寫好的 plugin
使用 [nautobot-device-lifecycle-mgmt](https://github.com/nautobot/nautobot-plugin-device-lifecycle-mgmt) 為例子

定義好 nautobot_config 檔案後

```python!
PLUGINS = ["nautobot_device_lifecycle_mgmt"]
```
按照下面步驟:

```
step1. poetry add nautobot-device-lifecycle-mgmt
step2. nautobot-server migrate
step3. nautobot-server runserver 0.0.0.0:8080 --insecure
```

![Imgur](https://imgur.com/j1OswQB.png)


### Database Models

A model is essentially a Python representation of a database table, with attributes that represent individual columns. Model instances can be created, manipulated, and deleted using queries. Models must be defined within a file named models.py


```pyt=
# models.py
from django.db import models


class DeviceConfig(models.Model):
    """Base model for config."""

    name = models.CharField(max_length=50)
    running_config= models.CharField(max_length=50)
    startup_config= models.CharField(max_length=50)

    def __str__(self):
        return self.name
```

幫 Plugin 定義了 model, 我們需要 migrate new model
migrate 文件基本上是一組指令，用於操作資料庫以支持我們的新 model，或者修改現有的 model

```
nautobot-server makemigrations download_config
nautobot-server migrate download_config
```


假設你新增加了一個 Model, 你需要執行 makemigrations.
但執行完 makemigrations 只是生成了對應的 sql command, 還沒有把真正的改動加入到 database 中, 還需要執行 migrate 才能把改變遷移到 database.

:::success
makemigrations 作用是 Django 會去檢查我們 建立或修改的 database, 如果不合法就會給提示
:::


這邊範例就是我成功新建了一個 DnsZoneModel

![Imgur](https://imgur.com/pU25hjL.png)


然後在 adminer 裡面看到成功新建了 DnsZoneModel 這個 model

![Imgur](https://imgur.com/4wviyGH.png)



#### Django admin 

[Django admin 介紹](https://ithelp.ithome.com.tw/m/articles/10334639)

Django admin 是 Django 框架內建的一個功能，用於建立一個強大的、可自訂的管理後台界面，使開發者和管理者能夠輕鬆管理和維護網站的數據

1. 數據管理: 直接在這邊使用 CRUD 功能，快速新增物件
2. 權限設定: 提供精細的網站權限設定，可以設定哪些用戶組可以訪問哪些特定的網頁
3. 圖形化介面: 可以直接在瀏覽器輸入連結，進入該網站進行設定


```python=
# admin.py
from django.contrib import admin

from .models import DownloadConfig


@admin.register(DownloadConfig)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'running_config', 'startup_config')
```

所以加入 admin.py 後, 可以點到 nautobot admin 頁面, 透過 後台系統新增物件

![Imgur](https://imgur.com/w33UV91.png)

list_display 是一個用於定義管理後台列表顯示的屬性. 允許我們指定在管理後台中展示哪些 modle field 的列表
list_display 輸入的幾項欄位 (這邊就是 name, running_config, startup_config)

![Imgur](https://imgur.com/vMQMTEI.png)


### Web UI Views

* Overview

![Imgur](https://imgur.com/UZ4bkIK.png)

如果我們的 Plugin 程式需要在 Nautobot Web UI 中擁有自己的一個或多個頁面，則需要定義 view


```PYTHON=
# views.py
from django.shortcuts import render
from django.views.generic import View

from .models import DownloadConfig


class RandomConfigView(View):
    """Display a randomly-selected Animal."""

    def get(self, request):
        # config = DownloadConfig.objects.order_by('?').first()
        configs = DownloadConfig.objects.all()
        return render(request, 'nautobot_download_config/download_config.html', {
            'configs': configs,
        })
```

這個 view 中，configs 是從 database 中找 DownloadConfig object 的结果
然後透過 render function 把這些數據傳遞给了 nautobot_download_config/download_config.html 這個 template



#### Extending the Base Template

:::success
Template，在django中即是html檔案，主要用來顯示使用者畫面
:::

Nautobot 提供了一個基本 template 來確保一致的使用者體驗, plugin 程式可以使用自己的內容進行擴充


```
{# templates/nautobot_download_config/download_config.html #}
{% extends 'base.html' %}

{% block title %}Download Configs{% endblock %}

{% block content %}
    <h1>Download Configurations</h1>

    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #dddddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color:
        }
    </style>

    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Running Config</th>
                <th>Startup Config</th>
            </tr>
        </thead>
        <tbody>
            {% for config in configs %}
                <tr>
                    <td>{{ config.name }}</td>
                    <td>{{ config.running_config }}</td>
                    <td>{{ config.startup_config }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
```

xxx.html 的第一行是 {% extends 'base.html' %}
這個標籤用來告訴 Django 使用 base.html 作為母版 (這邊不需要額外定義 base.html, 直接跟 nautobot 共用 )


#### Vscode extension

![Imgur](https://imgur.com/chATi1B.png)

安裝了這個套件後，在開發 Django Template(樣板)時，就可以使用Code Snippets自動產生程式碼片段



#### URL

Finally, to make the view accessible to users, we need to register a URL for it. We do this in urls.py by defining a urlpatterns variable containing a list of paths
為了讓 user 可以看到我們定義的 view, 我們需要為其註冊一個 URL.
我們 urls.py 透過定義一個 urlpatterns 包含 \_\_init\_\_.py 中的 base_url variable 來做到這一點


```python=
# urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('config/', views.RandomConfigView.as_view(), name='download_config'),
]
```

定義好 view, template 跟 url 後, 可以看到已經可以呈現我們的內容了
查看 http://127.0.0.1:8080/plugins/download_config/config/


##### Result

![Imgur](https://imgur.com/DA34G6q.png)



### REST API Endpoints

Plugins can declare custom endpoints on Nautobot's REST API to retrieve or manipulate models or other data

Plugins 可以在 Nautobot 的 REST API 上聲明自訂 endpoint, 用來擷取或操作 model 或其他資料
它們的行為與 view 非常相似, 只不過不是使用模板呈現任意內容m 而是使用 serializers以 JSON 格式傳回資料.

定義 Serializers, 這個目的是把你的資料庫中設定的欄位, 轉換成可以傳輸的模式

```python=
# api/serializers.py
from rest_framework.serializers import ModelSerializer

from .models import DownloadConfig


class ConfigSerializer(ModelSerializer):
    """API serializer for interacting with Animal objects."""

    class Meta:
        model = DownloadConfig
        fields = ('id', 'name', 'running_config', 'startup_config')
```

:::success
queryset :定義了在 ViewSet 中用於檢索數據的查詢 set.
這個屬性指定了需要在 ViewSet 中呈現 的model 數據的來源.
它通常是 model 的查詢 set,例如 MyModel.objects.all(), 指定了要從 database 中檢索的特定 model 數據集合
:::

然後需要更改 view.py 以及 url.py 的寫法
建立一個通用 API view, 允許對 DownloadConfig model 進行基本的 CRUD（建立、讀取、更新和刪除）操作.
這是定義在api/views.py

```python=
# api/views.py
from django.shortcuts import render
from django.views.generic import View
from rest_framework.viewsets import ModelViewSet
from .serializers import ConfigSerializer
from .models import DownloadConfig

class ConfigViewSet(ModelViewSet):
    """API viewset for interacting with DownloadConfig objects."""

    queryset = DownloadConfig.objects.all()
    # queryset = DownloadConfig.objects.order_by('id')[:1]
    serializer_class = ConfigSerializer
    
---

# urls.py
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('config', views.ConfigViewSet)
urlpatterns = router.urls
```

##### Result

有了這三個檔案，我們就可以用 /api/plugins/download_config/config/ 查看所有定義的 DownloadConfig object 的清單

![Imgur](https://imgur.com/9GdoaKi.png)





### Navigation Menu Items


增加 導覽選項清單

To make its views easily accessible to users, a plugin can inject items in Nautobot's navigation menu under the "Plugins" header

填寫的 link 可以去看 plugin 裡面的定義
(跟 \_\_init\_\_.py 裡面定義的 project name 有關)
![Imgur](https://imgur.com/dYdICQN.png)


* navigation.py

```python!
# navigation.py
from nautobot.apps.ui import NavMenuImportButton,NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab

items_operate = [
    NavMenuItem(
        link="plugins:download_config:downloadconfig-list",
        name="Config Overview",
        permissions=[],
        # buttons=(
        #     NavMenuAddButton(
        #         link="plugins:download_config:custom_view",
        #         permissions=[],
        #     ),
        # ), 
    ),
    NavMenuItem(
        link="plugins:download_config:custom_view",
        name="User Define",
        permissions=[],
    )
]

menu_items = (
    NavMenuTab(
        name="Download Config",
        weight=1000,
        groups=(
            NavMenuGroup(name="Manage", weight=100, items=tuple(items_operate)),
            # NavMenuGroup(name="Setup", weight=100, items=tuple(items_setup)),
        ),
    ),
)
```


##### Result


我們在上面的 navigation.py 定義了兩個 button, 結果如下圖

![Imgur](https://imgur.com/aTlx66b.png)



### Extending Core Templates

* template_content

```python!
# template_content
"""Added content to the device model view for config compliance."""
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.urls import reverse
from nautobot.dcim.models import Device
from nautobot.extras.plugins import PluginTemplateExtension
from download_config.models import DownloadConfig


class ConfigDeviceCheck(PluginTemplateExtension):  # pylint: disable=abstract-method
    """Plugin extension class for config compliance."""

    model = "dcim.device"

    def get_device(self):
        """Get device object."""
        return self.context["object"]

    def right_page(self):
        """Content to add to the configuration compliance."""

        return self.render(
            "nautobot_download_config/download_config.html",
        )

    def detail_tabs(self):
        """Add a Configuration Compliance tab to the Device detail view if the Configuration Compliance associated to it."""
        try:
            return [
                {
                    "title": "Configuration Link",
                    "url": "plugins:nautobot_download_config:config",
                }
            ]
        except ObjectDoesNotExist:
            return []


class ConfigDeviceDetails(PluginTemplateExtension):  # pylint: disable=abstract-method
    """Plugin extension class for config compliance."""

    model = "dcim.device"

    def get_device(self):
        """Get device object."""
        return self.context["object"]

    def right_page(self):
        """Content to add to the configuration compliance."""
        device = self.get_device()
        download_config = DownloadConfig.objects.filter(name=device).first()
        extra_context = {
            "device": self.get_device(),  # device,
            "golden_config": download_config,
            "template_type": "device-configs",
        }
        return self.render(
            "nautobot_download_config/download_config.html",
            extra_context=extra_context,
        )



extensions = [ConfigDeviceDetails]
extensions.append(ConfigDeviceCheck)



template_extensions = extensions
```



### Result

![Imgur](https://imgur.com/58hGuPd.png)







## Relationships

[Relationships](https://docs.nautobot.com/projects/core/en/v1.5.6/models/extras/relationship/)

relationships 是定義特定 object 之間的連結，這些連結可能特定於您的網路或資料.

To create a relationship, from the top-level navigation menu select Extensibility > Data Management > Relationships


### Relationship Types


1. ++Many-to-many++
多對多: 兩側的 relationship 可以連接到多個物件. 例如，VLANs 可以連接到多個 device，而 device 也可以擁有多個 VLANs.
where both sides of the relationship connection can be connected to multiple objects. For example, VLANs can be connected to multiple devices and devices will have multiple VLANs.


2. ++One-to-many++
一對多: 連接的一側只能擁有一個物件.
where one side of the connection can only have one object. For example, where a controller has many supplicants like FEX and parent switch. A FEX can be uplinked to one parent switch (in most cases), but the parent switch can have many FEX.

3. ++One-to-one++
一對一: 每側relationship 只能有一個物件.
where there can be only one object on either side of the relationship. For example, an IP address serving as a router-id for a device. Each device has at most one router-id, and each IP address can be a router-id for at most one device.



#### Django Model

[技術筆記：Django(四)](https://medium.com/@leealice033/%E6%8A%80%E8%A1%93%E7%AD%86%E8%A8%98-django-%E4%B8%89-b7a289a52f38)

Django 預設會為每一個 Model 加上 id 欄位, 並將這個欄位設成 primary key（主鍵）,簡稱 pk.
讓每一筆資料都會有一個獨一無二的 ID

Model fields 可為 Django Model 定義不同型態的屬性 
|Model fields | Description |
| --- | --- |
|CharField | 字串欄位, 適合像 title、location 這種有長度限制的字串 |
|TextField | 合放大量文字的欄位 |
|URLField | URL 設計的欄位 |
|DateTimeField | 日期與時間的欄位，使用時會轉成 Python datetime 型別 |
|IntegerField  | 整數欄位 |
|GenericIPAddressField  |  protocol='both', unpack_ipv4=False，ipv4 ipv6位址 protocol 可選擇 ipv4 \| ipv6 \| both |
|EmailField  | max_length=254，檢驗email是否為有效的email |


#### Relationships Plugin


[Developing Nautobot Plugins - Part 2](https://blog.networktocode.com/post/developing-nautobot-plugins-2/)


initial Model DnsZoneModel，並且我們將從 Nautobot 繼承PrimaryModel。這PrimaryModel是一個 Nautobot 特定的類，它提供了功能和繼承的基線，以便更輕鬆地利用 Nautobot 功能




#### Slug Field

[Slug Field](https://docs.nautobot.com/projects/core/en/stable/development/core/best-practices/#slug-field)

:::info
Changed in version 2.0.0
Models should generally not have a slug field, and should use the model's primary key (UUID) in URL patterns for both the UI and the REST API. All models should have a human-friendly natural key, either a single unique field (typically name) or a minimally complex unique-together set of fields (such as DeviceType's (manufacturer, model)).
:::

在舊版的 Django 中, 常常使用 slug 作為一種 natural key 的概念.
但在更新的版本中, natural_key_field_names 可以更靈活地指定一個或多個欄位作為 natural key


#### Registry

[Application Registry](https://docs.nautobot.com/projects/core/en/v2.0.3/development/core/application-registry/?h=registry)

是一種記憶體資料結構，其中包含各種應用程式範圍的參數，例如 enabled plugins (啟用的插件清單)

它不會向使用者公開, 也不會被 Nautobot 核心以外的任何程式碼修改



#### Populating Extensibility


[Populating Extensibility Features](https://docs.nautobot.com/projects/core/en/v1.4.7/plugins/development/#populating-extensibility-features)

```python=
# signals.py
from nautobot.extras.choices import RelationshipTypeChoices

def post_migrate_create_relationships(sender, apps, **kwargs):
    """Create a Device-to-MacTable Relationship if it doesn't already exist."""

    # Use apps.get_model to look up Nautobot core models
    ContentType = apps.get_model("contenttypes", "ContentType")
    Device = apps.get_model("dcim", "Device")
    Device = apps.get_model("dcim", "Device")
    MacTable = sender.get_model("MacTableModel")
    _Relationship = apps.get_model("extras", "Relationship")

    # Ensure that the Relationship exists
    for relationship_dict in [
        {
            "label": "MacTable on Device",
            "key": "device_mactable",
            "type": RelationshipTypeChoices.TYPE_ONE_TO_MANY,
            "source_type": ContentType.objects.get_for_model(MacTable),
            "source_label": "Device that mac address table",
            "destination_type": ContentType.objects.get_for_model(Device),
            "destination_label": "Mac Address Table",
        },
    ]:
        _Relationship.objects.get_or_create(label=relationship_dict["label"], defaults=relationship_dict)
```



加完後還要在 \_\_init\_\_.py 的 PluginConfig ready() function 中, 將此 callback function 連接到 nautobot_database_ready signal


```python=
# __init__.py
from nautobot.extras.plugins import PluginConfig
from nautobot.core.signals import nautobot_database_ready

class DownloadConfig(PluginConfig):
    name = 'download_config'
    verbose_name = 'Download Config'
    description = 'An example plugin for development purposes'
    version = '0.1'
    author = 'mcleezs'
    author_email = 'mcleezs@tsmc.com'
    base_url = 'download_config'
    required_settings = []
    min_version= '2.0.2'
    max_version= '2.0.4'


    def ready(self):
        """Register custom signals."""
        from .signals import post_migrate_create_relationships  # pylint: disable=import-outside-toplevel

        nautobot_database_ready.connect(post_migrate_create_relationships, sender=self)

        super().ready()


config = DownloadConfig
```


編寫此程式碼後, 執行nautobot-server migrate 或 nautobot-server post_upgrade
然後重新啟動 Nautobot 伺服器


![Imgur](https://imgur.com/zUN3zaD.png)

可以看到 自訂的 Relationships 現在已自動建立.

![Imgur](https://imgur.com/Dx02mNB.png)



