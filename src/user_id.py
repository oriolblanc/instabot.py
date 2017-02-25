#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import json
import random

def get_user_id_if_following (self, username):
    if (self.login_status):
        now_time = datetime.datetime.now()
        log_string = "%s : Get user followings \n%s"%(self.user_login,now_time.strftime("%d.%m.%Y %H:%M"))
        self.write_log(log_string)
        if self.login_status == 1:
            url = 'https://www.instagram.com/%s/'%(username)
            try :
                r = self.s.get(url)
                text = r.text
                finder_text_start = ('<script type="text/javascript">'
                                         'window._sharedData = ')
                finder_text_start_len = len(finder_text_start)-1
                finder_text_end = ';</script>'

                all_data_start = text.find(finder_text_start)
                all_data_end = text.find(finder_text_end, all_data_start + 1)
                json_str = text[(all_data_start + finder_text_start_len + 1) \
                                   : all_data_end]
                all_data = json.loads(json_str)
                                        
                user_info = list(all_data['entry_data']['ProfilePage'])

                user_id = str(user_info[0]['user']['id'])
                followed_by_viewer = user_info[0]['user']['followed_by_viewer']
                requested_by_viewer = user_info[0]['user']['requested_by_viewer']
                following = True if (followed_by_viewer or requested_by_viewer) else False
              	
                log_string="The @%s 's id is %s" % (username, user_id)
                self.write_log(log_string)

                if following:
                    log_string="You are following the user @%s with id %s" % (username, user_id)
                    self.write_log(log_string)
                    return user_id
                else:
                    log_string="You are not following the user @%s" % (username)
                    self.write_log(log_string)
                    return 0    
            except:
                self.media_on_feed = []
                self.write_log("Except on get_user_id!")
                time.sleep(20)
                return 0
        else:
            return 0
