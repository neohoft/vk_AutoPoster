from time import sleep

import vk

import config


def write_log(log: str):
    with open('log.log', 'a', encoding='UTF8') as file_log:
        file_log.write(f'{log}\n')


class AutoPoster(object):

    def __init__(self):
        self.vk_api = vk.API(vk.Session(access_token=config.access_token),
                             timeout=10000,
                             v=5.73)

    # получаем пост группы
    def get_posts(self, group_id):
        date: int = 1523741401
        while True:
            try:
                posts = self.vk_api.wall.get(owner_id=group_id, count=2)
                for post in posts['items']:
                    if post['date'] > date:
                        print(post['text'][1:5])
                        self.__post_parse(post)
                        date = post['date']
            except Exception as e:
                write_log(str(e))
                sleep(40)
                continue
            sleep(40)

    # распарсить пост группы
    def __post_parse(self, post: dict):
        attachments = []
        if post.get('attachments') is not None:
            for attachment in post['attachments']:
                if attachment.get('photo') is not None:
                    attachments.append(self.save_photo(attachment['photo']['id'],
                                                       attachment['photo']['owner_id'],
                                                       attachment['photo']['access_key']))
                else:
                    self.__publish_post(post['text'])
                    return
            self.__publish_post(post['text'], attachments)
        else:
            self.__publish_post(post['text'])

    # Публикация поста в группу
    def __publish_post(self, text, attachments=None):
        good_attachments = ''

        if attachments is not None:
            for attachment in attachments:
                attachment = '_'.join(attachment)
                good_attachments += f'{attachment[0:5]}{attachment[6:]},'

            self.vk_api.wall.post(owner_id=config.group_id,
                                  message=text,
                                  attachments=good_attachments,
                                  from_group=1)
        else:
            self.vk_api.wall.post(owner_id=config.group_id,
                                  message=text,
                                  from_group=1)

    # Сохроняем фото в альбом
    def save_photo(self, photo_id, owner_id, access_key):
        attachment = ['photo', '436299907', str(self.vk_api.photos.copy(owner_id=owner_id,
                                                                        photo_id=photo_id,
                                                                        access_key=access_key))]
        return attachment
