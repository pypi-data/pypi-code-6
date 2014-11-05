from pycclib.cclib import API


def main():
    data = {
      "id": "ttt",
      "api": {
        "config_vars": [
          "TTT_VARS"
        ],
        "password": "aaa",
        "sso_salt": "aaa",
        "production": {
          "base_url": "https://ttt.cnh-apps.com.com/cloudcontrol/resources/",
          "sso_url": "https://ttt.cnh-apps.com/cloudcontrol/resources/"
        },
        "test": "http://localhost:5000/"
      }
    }

    api = API(register_addon_url='https://cctrl-tokenprovidermiddleware.cloudandheat.com', encode_email=True)
    api.register_addon('P81F65D0611FC4F51B39BDB24E467553B:tw@cloudcontrol.de', '5tlF;a^*+#+:', data)


if __name__ == '__main__':
    main()
