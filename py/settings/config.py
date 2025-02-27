# 第三方登录--------------------------------
import random
import base64
GOOGLE = 1
FACE_BOOK = 2
SNAPCHAT = 3
FIRE_BASE_PHONE = 4
APPLE = 5

home_page_prefix = 'http://##.cloudfront.net/'

# todo 官方默认的jojor头像
official_default_image = "http://##.cloudfront.net/jojor_icon.png"

# 默认的jojor头像
login_default_image = 'http://##.cloudfront.net/default_picture/jojor_default_picture.png'
login_default_image_male = "http://##.cloudfront.net/default_male_1.png"
login_default_image_female = "http://##.cloudfront.net/default_female_1.png"


eighteenth_years_old = 567648000

get_female_default_head = "http://cdn1.findher.in/##/##/#.jpg"
get_male_default_head = "http://cdn1.findher.in/##/#/#.jpg"
# FACE_BOOK_APP_ID = "###"
# # FACE_BOOK_KEY = "###"
# FACE_BOOK_KEY = "###"

FACE_BOOK_APP_ID = "###"
FACE_BOOK_KEY = "###"


# IP 得到的  国家简码对应的国家全称
IP_MAP_COUNTRY = {'AO': 'Angola', 'AF': 'Afghanistan', 'AL': 'Albania', 'DZ': 'Algeria', 'AD': 'Andorra',
                  'AI': 'Anguilla', 'AG': 'Antigua and Barbuda', 'AR': 'Argentina', 'AM': 'Armenia',
                  ' ': 'Samoa Western', 'AU': 'Australia', 'AT': 'Austria', 'AZ': 'Azerbaijan', 'BS': 'Bahamas',
                  'BH': 'Bahrain', 'BD': 'Bangladesh', 'BB': 'Barbados', 'BY': 'Belarus', 'BE': 'Belgium',
                  'BZ': 'Belize', 'BJ': 'Benin', 'BM': 'Bermuda Is.', 'BO': 'Bolivia', 'BW': 'Botswana', 'BR': 'Brazil',
                  'BN': 'Brunei', 'BG': 'Bulgaria', 'BF': 'Burkina-faso', 'MM': 'Burma', 'BI': 'Burundi',
                  'CM': 'Cameroon', 'CA': 'Canada', 'CF': 'Central African Republic', 'TD': 'Chad', 'CL': 'Chile',
                  'CN': 'China', 'CO': 'Colombia', 'CG': 'Congo', 'CK': 'Cook Is.', 'CR': 'Costa Rica', 'CU': 'Cuba',
                  'CY': 'Cyprus', 'CZ': 'Czech Republic', 'DK': 'Denmark', 'DJ': 'Djibouti', 'DO': 'Dominica Rep.',
                  'EC': 'Ecuador', 'EG': 'Egypt', 'SV': 'EI Salvador', 'EE': 'Estonia', 'ET': 'Ethiopia', 'FJ': 'Fiji',
                  'FI': 'Finland', 'FR': 'France', 'GF': 'French Guiana', 'GA': 'Gabon', 'GM': 'Gambia',
                  'GE': 'Georgia', 'DE': 'Germany', 'GH': 'Ghana', 'GI': 'Gibraltar', 'GR': 'Greece', 'GD': 'Grenada',
                  'GU': 'Guam', 'GT': 'Guatemala', 'GN': 'Guinea', 'GY': 'Guyana', 'HT': 'Haiti', 'HN': 'Honduras',
                  'HK': 'Hongkong', 'HU': 'Hungary', 'IS': 'Iceland', 'IN': 'India', 'ID': 'Indonesia', 'IR': 'Iran',
                  'IQ': 'Iraq', 'IE': 'Ireland', 'IL': 'Israel', 'IT': 'Italy', 'JM': 'Jamaica', 'JP': 'Japan',
                  'JO': 'Jordan', 'KH': 'Kampuchea (Cambodia )', 'KZ': 'Kazakstan', 'KE': 'Kenya', 'KR': 'Korea',
                  'KW': 'Kuwait', 'KG': 'Kyrgyzstan', 'LA': 'Laos', 'LV': 'Latvia', 'LB': 'Lebanon', 'LS': 'Lesotho',
                  'LR': 'Liberia', 'LY': 'Libya', 'LI': 'Liechtenstein', 'LT': 'Lithuania', 'LU': 'Luxembourg',
                  'MO': 'Macao', 'MG': 'Madagascar', 'MW': 'Malawi', 'MY': 'Malaysia', 'MV': 'Maldives', 'ML': 'Mali',
                  'MT': 'Malta', 'MU': 'Mauritius', 'MX': 'Mexico', 'MD': 'Moldova, Republic of', 'MC': 'Monaco',
                  'MN': 'Mongolia', 'MS': 'Montserrat Is', 'MA': 'Morocco', 'MZ': 'Mozambique', 'NA': 'Namibia',
                  'NR': 'Nauru', 'NP': 'Nepal', 'NL': 'Netherlands', 'NZ': 'New Zealand', 'NI': 'Nicaragua',
                  'NE': 'Niger', 'NG': 'Nigeria', 'KP': 'North Korea', 'NO': 'Norway', 'OM': 'Oman', 'PK': 'Pakistan',
                  'PA': 'Panama', 'PG': 'Papua New Cuinea', 'PY': 'Paraguay', 'PE': 'Peru', 'PH': 'Philippines',
                  'PL': 'Poland', 'PF': 'French Polynesia', 'PT': 'Portugal', 'PR': 'Puerto Rico', 'QA': 'Qatar',
                  'RO': 'Romania', 'RU': 'Russia', 'LC': 'St.Lucia', 'VC': 'St.Vincent', 'SM': 'San Marino',
                  'ST': 'Sao Tome and Principe', 'SA': 'Saudi Arabia', 'SN': 'Senegal', 'SC': 'Seychelles',
                  'SL': 'Sierra Leone', 'SG': 'Singapore', 'SK': 'Slovakia', 'SI': 'Slovenia', 'SB': 'Solomon Is',
                  'SO': 'Somali', 'ZA': 'South Africa', 'ES': 'Spain', 'LK': 'Sri Lanka', 'SD': 'Sudan',
                  'SR': 'Suriname', 'SZ': 'Swaziland', 'SE': 'Sweden', 'CH': 'Switzerland', 'SY': 'Syria',
                  'TW': 'Taiwan', 'TJ': 'Tajikstan', 'TZ': 'Tanzania', 'TH': 'Thailand', 'TG': 'Togo', 'TO': 'Tonga',
                  'TT': 'Trinidad and Tobago', 'TN': 'Tunisia', 'TR': 'Turkey', 'TM': 'Turkmenistan', 'UG': 'Uganda',
                  'UA': 'Ukraine', 'AE': 'United Arab Emirates', 'GB': 'United Kiongdom',
                  'US': 'United States of America', 'UY': 'Uruguay', 'UZ': 'Uzbekistan', 'VE': 'Venezuela',
                  'VN': 'Vietnam', 'YE': 'Yemen', 'YU': 'Yugoslavia', 'ZW': 'Zimbabwe', 'ZR': 'Zaire', 'ZM': 'Zambia'}


# class Config(object):
#
#     @property
#     def url_prefix(self):
#         conf = SysConfig.objects(name='url_prefix').first()
#         if conf and conf.section.get('url', ''):
#             return conf.section['url']
#
#         return 'https://test.qmovies.tv:8081/f1'
#
#     @property
#     def is_debug(self):
#         conf = SysConfig.objects(name='env').first()
#         if conf and conf.section.get('test', 1):
#             return True
#
#         return False
#
#     @property
#     def comp_rid_list(self):
#         conf = SysConfig.objects(name='comp_rid_list').first()
#         return conf.section.get('list', []) if conf else []
#
#     @property
#     def hard_decode(self):
#         conf = SysConfig.objects(name='hard_decode').first()
#         return conf.section.get('hard_decode', 1) if conf else 1
#
#
# config_cls = Config()
# 声网踢人配置
agora_appid = "##"

Appid = "##"
plainCredentials =  "##:##"
BaseUrl = "https://api.agora.io/dev/v1"
appCertificate = "##"

# python3
base64Credentials = base64.b64encode(plainCredentials.encode())
base64Credentials = base64Credentials.decode()
#微信APPID
wechatAppId = "##"
wechatAppSecret = "##"

#wechatAppId = "###"
#wechatAppSecret = "####"

#因为只是给kimi一个人登录，所以用户名和密码写道配置文件里面
username="##"
password="##"
uid="###"
rid =##

#的也要写死一个token
y_uid="####"
y_rid=###

uid_list = ["4477051964694204417","4477080290808827905","4483160143530299393","4494789326853378049","4478155010442530817","4491197847086043111"]
andorid_to_uid={
"00000000-4e33-f694-ffff-ffffc13f":"4477051964694204417",
"ffffffff-e81b-8199-ffff-ffffb630":"4477080290808827905",
"ffffffff-e81b-8199-ffff-ffffb632":"4483160143530299393",
"ffffffff-e81b-8199-ffff-ffffb633":"4494789326853378049",
"ffffffff-e81b-8199-ffff-ffffb634":"4478155010442530817"
}

user_to_achor={
   "4477051964694204417":"4491197847086043000",
    "4477080290808827905":"4491197847086043000",
    "4483160143530299393":"4491197847086043000",
    "4494789326853378049":"4491197847086043000",
    "4478155010442530817":"4491197847086043000",
    "4491197847086043111":"4491197847086043000"
}
