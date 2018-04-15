# from threading import Thread
import config
from autoposter import AutoPoster


if __name__ == '__main__':
    auto_post = AutoPoster()
    auto_post.get_posts(config.groups_ids[0])

    # Много поточность
    # for i in range(len(config.groups_ids)):
    #     th = Thread(target=auto_post.get_posts, args=(config.groups_ids[i],))
    #     th.start()
