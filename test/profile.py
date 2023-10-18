import requests
import json
from data import user
import auth
import config


image_url_set = [
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMzMg/MDAxNTYzNTI4NTExNDQ2.egzGcQcjqzxrIALtoL6bT7r4FNQcydEjYWjI-_pYEB8g.9fyL6ec8x0_C-lFc2NGrPbjhxXzqJMDuiLWBHobzHPMg.JPEG.alsldi1117/beach-677785_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMjM3/MDAxNTYzNTI4NTExNDkz.iXhm7eU6kc4TIvkPFylNRn7XC9dLforKXwtgUo_-Shgg.Hozn_2rwPntZOjgwQBJVsW7L59jL2JBitCJ4hvSAG-8g.JPEG.alsldi1117/beach-1050225_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMTE5/MDAxNTYzNTI4NTEyMzU4.AU3fYjhUjoJkhcFebAbFsnL8F2giXYKF_BsVLO6e4dQg.J-Opdl52PYz-qJzzoFoKdLjn9rd___fjCZHvuz_iRz4g.JPEG.alsldi1117/person-2471177_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMjk1/MDAxNTYzNTI4NTExMzA2.OvsFIwQuvVonu435bEQNqfvJuGp934JNw3heNK5aXRIg.Qtdv0dWF51qm7MSboBX7nKmUSBDfzo72tP0Mih14oQIg.JPEG.alsldi1117/bicycle-1851497_1280.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfOTYg/MDAxNTYzNTI4NTEyNjAz.QpTwnSrB9QsTlhmlTelYuk2huM0zj0dnDdtgwzWaz5sg.pfWEgtXcMxZSIh5swBQe5aKLH7tiYWpG_4ah8T4GH5sg.JPEG.alsldi1117/flower-4064358_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMjk3/MDAxNTYzNTI4NTExMzAw.pdh1rDbsces3hkNkZ0mGgjNmI7vT0uZnOMp3DYRSpqMg.rsXmkf6CIe_d5S8tiAk75lCvildiA3V4VDAw33sFd78g.JPEG.alsldi1117/blue-2309309_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMjAz/MDAxNTYzNTI4NTEyMDQy.iMgsny6W4yBP7diy6PNo-vAZgITJ5uVOCuoKCuoRkIsg.Q-9KT13lXDHgO0SmcHoZVNbBGzBae0g2MyA2ysz799cg.JPEG.alsldi1117/heart-1986105_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfODUg/MDAxNTYzNTI4NTExNTg1.onwOS2i_tB_Dz-eMJrxiqI9Clxrq4bpDalJ9qUvvH7Qg.51gpupaAJGb51p5Dmtb52Gfm6KvxDp5KtmCj3nn-fskg.JPEG.alsldi1117/blue-2705642_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMTU3/MDAxNTYzNTI4NTExNzk1.SIjKyy6bN-BfAOS65dj1YrS3exgWU05EJGG39Uv96Nwg.UUqdKuieYhK1DX6VuYtqaOP5I0XnVFeE17v29JvwTPkg.JPEG.alsldi1117/cat-691175_1280.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfNjYg/MDAxNTYzNTI4NTEzNTg4.zLQEgWP4P362huRXG6KhdvQSoa9DV5JiflUafdJzPrcg.BYo0CRl67krmSLiCqRF2vj6bGYPppxrA7UGxDLqwZOMg.JPEG.alsldi1117/smile-1374564_1280.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMjYw/MDAxNTYzNTI4NTEzMzA1.mrW2HNJ__n5RCreswA-p4Y-xfCMevJ_V9KujPyasxKIg.d0AyFWJTt790UkJXugv6F17oLL4JVdDYFPEi_0_glqsg.JPEG.alsldi1117/converse-2485685_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMTU4/MDAxNTYzNTI4NTEyNzQ0.aK8_zX_yxh7VW4xpxJQnVmVtT2JEVWTd5GZqUWbxbKgg.UXq3EYP-LU_k5B7dfiJCjFU5Q002AErEsPPpY97lQJYg.JPEG.alsldi1117/ice-cream-parlour-722000_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMTYw/MDAxNTYzNTI4NTEzNDg2.Ar8-Ka5vLDTi5cpp5NYBbBV94iILH5znqi4zXSEXNHkg.oqX52FTcZn39pAmdsRCgYX4zL22KLz9RJe25nRfX8Wcg.JPEG.alsldi1117/icing-sugar-3744757_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfODcg/MDAxNTYzNTI4NTEyNjg5.wffQ8oPztmjZf1DtDvz5wkUtGJHcGoLAZ8EuCDq2c0Mg.s5aaw_3GfVGn7XPJBRDh3J7W8qVc6_RYxcQm5IEJkbMg.JPEG.alsldi1117/love-382533_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMTMg/MDAxNTYzNTI4NTEzNDgz.tj7cJrh8d8WngDSiZMmJ0ixPHLc9bQXldMjTqBYimdYg.nAMcjqrsctxq_yu0glhksiaghBg7xHETcSiV-h3ISfQg.JPEG.alsldi1117/woman-1852907_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMTg3/MDAxNTYzNTI4NTEyNDkx.9jXZMQGEWpUY4GOYA5mhV-kX9RVTfx5jxkXOThJk8DUg.n8HIDGIq7Q8hsLwiZmpgnbTKQlSTtxglwqNkdz8GzG8g.JPEG.alsldi1117/pink-1821381_1280.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA3MTlfMTg2/MDAxNTYzNTI4NTExNjkx.b81kMx5lSSijQdPfTIQaQM-_rClmvxWZkLAM5YhBKX4g.Yfg3NSo2naQzl8gHOj2PLuuZe3ok7uZgilLvbmECwowg.JPEG.alsldi1117/board-3700116_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA4MDRfOTAg/MDAxNTY0OTExNDY0ODYw.ZrmVRvTmmJr83FvgYXvkUbEp6XYpiiBMzkXRRpaLVKkg.wZVO-Y_MfP3uBB343JuAW8w897lzoUWBjGoBf90OZ5sg.JPEG.alsldi1117/travel-3122702_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA4MDRfMTk3/MDAxNTY0OTExNDY0OTQ1.VKfNidLcEwNWuHf9vLeSTc1JXU4vIGb4BBJn7XKsNHQg.W1Gsi5znBkrGPvQP4uenrWJ5UcRuKLqKcKi3s5LYenYg.JPEG.alsldi1117/moon-3894451_1920.jpg?type=w800",
    "https://mblogthumb-phinf.pstatic.net/MjAxOTA4MDRfMjUw/MDAxNTY0OTExNDY1MTAz.2rc3swgpRmlW_iOhLuBqJc-7XygK--Mi3aiO38hQhUIg.1aXB8w2gBwgWDfnM-LXAw2nllCHYisUbqH3d9ms6FqMg.JPEG.alsldi1117/girls-4051339_1920.jpg?type=w800",
]


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:  # Successful HTTP request
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        print(
            f"Failed to download the image. HTTP Status Code: {response.status_code}")


def download_images():
    for i, url in enumerate(image_url_set):
        download_image(url, f"./images/profile/profile_image_{i+1}.jpg")


def upload_file(url, filename):
    with open(filename, 'rb') as file:
        files = {'file': (filename, file)}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print(f"Successfully uploaded {filename}")
    else:
        print(
            f"Failed to upload {filename}. HTTP Status Code: {response.status_code}")


url = f"{config.server_url}/profile"


def create_profile_image(url, user, filename):
    token = auth.login(user)
    with open(filename, 'rb') as file:
        files = {'file': (filename, file)}
        r = requests.post(url, files=files, headers=token)
        print(r.text)


def create_profile_images():
    for i, user_data in enumerate(user.user_data_set):
        create_profile_image(
            url, user_data, f"./images/profile/profile_image_{i+1}.jpg")


if __name__ == "__main__":
    create_profile_images()
